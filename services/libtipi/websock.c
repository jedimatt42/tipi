/* 
  websock.c - Websocket server for tipiports

  Copyright (C) 2020  Pete Eberlein

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


/*
  Creates a simple HTTPD server on "http://localhost:9901/"
  Accepts one websocket connection on "ws://localhost:9901/tipi"
  
  Websocket server is started by env variable "TIPI_WEBSOCK"
  which is set to the web root directory, where file requests are 
  searched.

  Websocket sends/receives register changes formatted as "Rx=nnn"
  where "Rx" is one of: TD TC RD RC
  and "nnn" is decimal byte value

  Except the above protocol introduces too much latency to be usable.
  Instead we send whole messages as binary websocket frames.
  The length of the message doesn't need to encoded - there is one message
  per websocket frame, so it is the length of the websocket frame.

  In addtion, the following text messages are used:
  "RESET" will exit the server and restart (when the TI emulation is RESET)
  "SYNC" at the start of each message (when TC=0xf1 and RC=0xf1)
  "MOUSE buttons dx dy" will accumulate mouse motion and relay when requested

  See https://github.com/jedimatt42/tipi/blob/master/hardware/dsr/tipi-io.a99
  for latched register addresses in DSR, reproduced here:
  
TDOUT	EQU	>5FFF		; TI Data (output)
TCOUT	EQU	>5FFD		; TI Control Signal (output)
RDIN	EQU	>5FFB		; PI Data (input)
RCIN	EQU	>5FF9		; PI Control Signal (input)
*/

#include <Python.h>

#ifndef _GNU_SOURCE
#define _GNU_SOURCE       /* for asprintf */
#endif
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <poll.h>
#include <ctype.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <limits.h>
#include <sys/sendfile.h>
#include <stdarg.h>

#include "sha1/sha1.h"

#define ARRAY_SIZE(x) (sizeof(x)/sizeof(x[0]))

#define PORT 9901

#define SEL_RC 0
#define SEL_RD 1
#define SEL_TC 2
#define SEL_TD 3
static unsigned char regs[4] = {};
static const char *reg_names[4] = {"RC","RD","TC","TD"};

static const char *web_root = NULL;
static int web_root_len;
static int client_fd = -1; // websocket client socket
static struct {
	char *path;
	off_t size;
} files[1024];
static unsigned int file_count = 0;

//#define LOG
#ifdef LOG
static void log_printf(const char *fmt, ...)
{
	static FILE *log = NULL;

	if (!log)
		log = fopen("/var/log/tipi/websock.log", "w");

	va_list ap;
	va_start(ap, fmt);
	vfprintf(log, fmt, ap);
	va_end(ap);
	fflush(log);
}
#else

#define log_printf(...) do{}while(0)

#endif

static int scan_filter(const struct dirent *d)
{
	static char subdir[PATH_MAX] = "";
	switch (d->d_type) {
	case DT_DIR:
		if (strcmp(d->d_name, "..") == 0 || strcmp(d->d_name, ".") == 0)
			break;
		strcat(subdir, "/");
		strcat(subdir, d->d_name);
		{
			struct dirent **namelist = NULL;
			char *dirp = NULL;
			asprintf(&dirp, "%s/%s", web_root, subdir);
			scandir(dirp, &namelist, scan_filter, NULL);
			free(dirp);
		}
		char *slash = strrchr(subdir, '/');
		if (slash)
			*slash = 0;
		break;
	case DT_REG: {
		char *path = NULL;
		struct stat st;
		if (file_count >= ARRAY_SIZE(files))
			break;

		asprintf(&path, "%s%s/%s", web_root, subdir, d->d_name);
		stat(path, &st);

		files[file_count].path = path;
		files[file_count].size = st.st_size;
		file_count++;

		//printf("found %s %ld\n", path, st.st_size);

		break;
	}
	default:
		break;
	}
	return 0;
}

void websocket_init(const char *path_to_web_root)
{
	struct dirent **namelist = NULL;
	web_root = path_to_web_root;
        web_root_len = strlen(web_root);
	log_printf("scanning %s\n", web_root);
	scandir(web_root, &namelist, scan_filter, NULL);
        log_printf("found %d files\n", file_count);
}



static int ends_with(const char *str, const char *ext)
{
    int off = strlen(str) - strlen(ext);
    if (off < 0)
        return 0;
    return strcasecmp(str + off, ext) == 0;
}

static char *trim(char *s)
{
	while (isspace(*s))
		s++;
	char *end = s + strlen(s);
	while (end != s && isspace(end[-1]))
		end--;
	*end = 0;
	return s;
}



static char *mime_type(const char *str)
{
	if (ends_with(str, ".html") || ends_with(str, ".htm"))
		return "text/html";
	if (ends_with(str, ".js"))
		return "application/x-javascript";
	if (ends_with(str, ".json"))
		return "application/json";
	if (ends_with(str, ".png"))
		return "image/png";
	if (ends_with(str, ".jpg") || ends_with(str, ".jpeg"))
		return "image/jpeg";
	if (ends_with(str, ".css"))
		return "text/css";
	if (ends_with(str, ".txt"))
		return "text/plain";
        // unknown or binary types
	return "application/octet-stream";
}



// decode %xx chars in s, in-place
// (string will always become shorter, so no buffer overruns)
static void uri_decode(char *s)
{
	while ((s = strchr(s, '%'))) {
		if (!isxdigit(s[1]) || !isxdigit(s[2])) {
			char hex[] = {s[1], s[2], 0};
			s[0] = strtol(hex, NULL, 16);
			strcpy(s+1, s+3);
		}
		s++;
	}
}

// return nul-terminated base64 malloced string
static char* base64_encode(const unsigned char *src, unsigned int len)
{
	unsigned int pad = 2 - ((len + 2) % 3);
	unsigned int out = 4 * ((len + 2) / 3);
	char *dest = malloc(out+1);

	char map[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	unsigned int i;
	for (i = 0; i < out; i++) {
		unsigned int j = i * 6 / 8;
		//printf("j=%d shift=%d\n", j, 8-i*6%8);
		unsigned char bits = (((j < len ? src[j] : 0)<<8) | (j+1 < len ? src[j+1] : 0)) >> (10-(i * 6 % 8));
		dest[i] = map[bits & 0x3f];
	}
	memset(dest+out-pad, '=', pad);
	dest[out] = 0;
	return dest;
}


static int read_again(int fd, unsigned char *data, int len)
{
  int n = 0;
  while (n < len) {
    int rc = read(fd, data + n, len - n);
    if (rc > 0)
      n += rc;
    else if (errno != EAGAIN)
      return -1;
  }
  return len;
}


enum {
	OPCODE_CONTINUATION = 0,
	OPCODE_TEXT = 1,
	OPCODE_BINARY = 2,
	OPCODE_CLOSE = 8,
	OPCODE_PING = 0x9,
	OPCODE_PONG = 0xa,
};

static PyObject *readMsg = NULL;

// read one websocket frame up to data_size, returning actual size
static int websocket_read(int fd, int *opcode, unsigned char *data, int data_size)
{
  unsigned char buf[8];
  int len;
  int mask;

  int rc = read(fd, buf, 2);
  if (rc < 2) return -1;

  *opcode = buf[0] & 0xf;
  len = buf[1] & 0x7f;
  mask = buf[1] & 0x80 ? 1 : 0;

  log_printf("opcode=%d len=%d   %02x %02x rc=%d\n", *opcode, len, buf[0], buf[1], rc);

  if (len == 126) {
    // 16-bit len
    if (read(fd, buf, 2) < 2) return -1;
    len = (buf[0] << 8) | buf[1];
  } else if (len == 127) {
    // 64-bit len
    if (read(fd, buf, 8) < 8) return -1;
    uint64_t payload_len =
      ((uint64_t)buf[0] << 56) | ((uint64_t)buf[1] << 48) |
      ((uint64_t)buf[2] << 40) | ((uint64_t)buf[3] << 32) |
      (buf[4] << 24) | (buf[5] << 16) |
      (buf[6] << 8)  |  buf[7];
    if (payload_len > INT_MAX)
      return -1;
    len = payload_len;
  }
  if (mask) {
    if (read(fd, buf, 4) < 4) return -1;
  }
  if (*opcode == OPCODE_BINARY) {
    Py_buffer buffer;

    if (readMsg == NULL)
      readMsg = PyByteArray_FromStringAndSize("", 0);
    PyByteArray_Resize(readMsg, len);
    if (PyObject_GetBuffer(readMsg, &buffer, PyBUF_CONTIG) < 0)
      return -1;
    data = buffer.buf;

  } else if (len > data_size) {
    return -1;
  }

  if (read_again(fd, data, len) < 0)
    return -1;

  if (mask) {
    int i;
    for (i = 0; i < len; i++)
      data[i] ^= buf[i&3];
  }
  return len;
}

// write one websocket frame with opcode and mask(if nonzero)
static void websocket_write(int fd, int opcode, unsigned int mask, unsigned char *data, int len)
{
  unsigned char header[32];
  unsigned int header_len = 2;

  if (opcode != OPCODE_CONTINUATION &&
      opcode != OPCODE_TEXT &&
      opcode != OPCODE_BINARY &&
      opcode != OPCODE_CLOSE &&
      opcode != OPCODE_PING &&
      opcode != OPCODE_PONG)
	  return;

  header[0] = 0x80 /*FIN=1*/ | opcode;
  header[1] = (mask ? 0x80 : 0x00) |
      ((len <= 125) ? len :
       len <= 0xffff ? 126 : 127);
  if (len > 125) {
    if (len <= 0xffff) {
      header[header_len++] = (len >> 8) & 0xff;
      header[header_len++] = len & 0xff;
    } else {
      uint64_t payload_len = len;
      header[header_len++] = (payload_len >> 56) & 0xff;
      header[header_len++] = (payload_len >> 48) & 0xff;
      header[header_len++] = (payload_len >> 40) & 0xff;
      header[header_len++] = (payload_len >> 32) & 0xff;
      header[header_len++] = (payload_len >> 24) & 0xff;
      header[header_len++] = (payload_len >> 16) & 0xff;
      header[header_len++] = (payload_len >> 8) & 0xff;
      header[header_len++] = payload_len & 0xff;
    }
  }
  if (mask) {
    unsigned char *mask_key = header + header_len;
    header[header_len++] = (mask >> 24) & 0xff;
    header[header_len++] = (mask >> 16) & 0xff;
    header[header_len++] = (mask >> 8) & 0xff;
    header[header_len++] = mask & 0xff;
    int i;
    for (i = 0; i < len; i++) {
      data[i] ^= mask_key[i&3];
    }
  }
  log_printf("%02x %02x hdr_len=%d len=%d\n", header[0], header[1], header_len, len);
  write(fd, header, header_len);
  write(fd, data, len);
}

static void set_reg_from_string(char *s)
{
  unsigned int i;
  for (i = 0; i < ARRAY_SIZE(regs); i++) {
    if (s[0] == reg_names[i][0] &&
        s[1] == reg_names[i][1] &&
        s[2] == '=') {
      regs[i] = atoi(s+3);
      log_printf("%s=%d   %s\n", reg_names[i], regs[i], s);
      break;
    }
  }
}



static int buttons = 0, dx = 0, dy = 0;


// move mouse message format "MOUSE buttons dx dy"
static void move_mouse(char *s)
{
  s = strchr(s, ' '); // before buttons
  if (!s) return;

  //log_printf("%s: %s\n", __func__, s);

  buttons = atoi(++s);

  s = strchr(s, ' '); // before dx
  if (!s) return;
  dx += atoi(++s);

  s = strchr(s, ' '); // before dy
  if (!s) return;
  dy += atoi(++s);
}

static void websocket_serveReg(int reg)
{
  log_printf("%s value=%d reg=%d client_fd=%d\n", __func__, regs[reg], reg, client_fd);
  if (client_fd != -1) {
    char buf[32];
    int len = sprintf(buf, "%s=%d", reg_names[reg], regs[reg]);
    websocket_write(client_fd, OPCODE_TEXT, 0/*mask*/, (unsigned char*)buf, len);
  }
}

static int server_create(void)
{
	struct sockaddr_in addr;
	int opt = 1;
	int addrlen = sizeof(addr);
	int fd;

	if ((fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
		perror("socket");
		goto err;
	}

	if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR|SO_REUSEPORT, &opt, sizeof(opt))) {
		perror("setsockopt SO_REUSEADDR|SO_REUSEPORT");
		//goto err;
	}

	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = INADDR_ANY;
	addr.sin_port = htons(PORT);

	if (bind(fd, (struct sockaddr*)&addr, addrlen) < 0) {
		perror("bind");
		goto err;
	}

	if (listen(fd, 3) < 0) {
		perror("listen");
		goto err;
	}
	return fd;
err:
	if (fd != -1)
		close(fd);
	return -1;
}

static int resetSync = 0;

// open the server socket, accept any pending connection, perform upgrade, poll open websocket
static int websocket_serve(void)
{
	static int srv_fd = -1; // server socket

	if (srv_fd == -1) {
		srv_fd = server_create();
		if (srv_fd == -1)
			goto shutdown;
		log_printf("server started fd=%d\n", srv_fd);
	}

	struct pollfd pfd[] = {
		{ .fd = srv_fd, .events = POLLIN },
		{ .fd = client_fd, .events = POLLIN },
	};

	int ms = 100; // milliseconds
	int rc = poll(pfd, ARRAY_SIZE(pfd), ms);
	if (rc <= 0)
		return -1;

	// read any data from the websocket
	if (client_fd != -1 && (pfd[1].revents & POLLIN)) {
		unsigned char data[128];
		int opcode = 0;
		int len = websocket_read(client_fd, &opcode, data, sizeof(data));
		if (len == -1 || opcode == OPCODE_CLOSE) {
			// websocket closed
			if (opcode == OPCODE_CLOSE)
				websocket_write(client_fd, OPCODE_CLOSE, 0, NULL, 0);
			log_printf("websocket closed len=%d\n", len);
			close(client_fd);
			client_fd = -1;

		} else if (opcode == OPCODE_TEXT && len >= 4) {
			char *str = (char*)data;
			str[len] = 0;
			if (strcmp(str, "RESET") == 0) {
				log_printf("RESET received\n");
				goto shutdown;

			} else if (strcmp(str, "SYNC") == 0) {
				resetSync = 1;
			} else if (strncmp(str, "MOUSE ", 6) == 0) {
				move_mouse(str);
			} else {
				set_reg_from_string(str);
			}
		} else if (opcode == OPCODE_PING) {
			websocket_write(client_fd, OPCODE_PONG, 0/*mask*/, data, len);
		}
	}

	// read any requests from the HTTP server socket
	if ((pfd[0].revents & POLLIN) == 0)
		return 0;

	struct sockaddr_in addr;
	unsigned int addrlen = sizeof(addr);
	int fd = accept(srv_fd, (struct sockaddr *)&addr, (socklen_t*)&addrlen);
	if (fd < 0)
		return 0;

	char buffer[4096];
	rc = read(fd, buffer, sizeof(buffer)-1);
	if (rc <= 0)
		return 0;
	buffer[rc] = 0;
	//printf("%s\n", buffer);

	if (strncmp(buffer, "GET /", 5) != 0)
		goto badrequest;
	char *filename = buffer + 4;
	char *http = strstr(filename, " HTTP/");
	if (!http)
		goto badrequest;
	http[0] = 0; // terminate filename

	uri_decode(filename); // in-place

	char *headers[20];
	unsigned int header_count = 0;
	{
		unsigned int i = http - buffer;
		unsigned int len = rc;

		while (i < len) {
			if (buffer[i] == '\n' || buffer[i] == '\r') {
				if (buffer[i+1] != '\n' && buffer[i+1] != '\r') {
					headers[header_count++] = buffer+i+1;
					if (header_count >= ARRAY_SIZE(headers))
						break;
				}
				buffer[i] = 0;
			}
			i++;
		}

		//log_printf("filename = %s\n", filename);
		//for (i = 0; i < header_count; i++)
		//	log_printf("%s\n", headers[i]);

		for (i = 0; i < header_count; i++) {
			if (strcasecmp(headers[i], "Upgrade: websocket") == 0 &&
				strcmp(filename, "/tipi") == 0)
				goto upgrade_websocket;
		}
	}


	if (strcmp(filename, "/") == 0)
		filename = "/index.html"; // hardcoded

	unsigned int i;
	for (i = 0; i < file_count; i++) {
		//printf("%s %s\n", filename, files[i].path+web_root_len);
		if (strcmp(filename, files[i].path+web_root_len) != 0)
			continue;
		char *content_type = mime_type(filename);
		char resp[1024];
		int src_fd;
		off_t size = files[i].size;

		src_fd = open(files[i].path, O_RDONLY);
		log_printf("%s %d %s\n\n\n", files[i].path, src_fd, content_type);

		if (src_fd == -1)
			goto notfound;

		int hdr_len = sprintf(resp, 
			"HTTP/1.0 200 OK\r\n"
			"Connection: close\r\n"
			"Content-Length: %ld\r\n"
			"%s%s%s"
			"\r\n",
			size,
			content_type ? "Content-Type: " : "",
			content_type ? content_type : "",
			content_type ? "\r\n" : "");
		write(fd, resp, hdr_len);
		while (size > 0) {
			int rc = sendfile(fd, src_fd, NULL, size);
			if (rc < 0)
				break;
			size -= rc;
		}
		close(src_fd);
		close(fd);
		return 0;
	}

notfound:
	{
		char resp[] = 
			"HTTP/1.1 404 Not found\r\n"
			"Connection: close\r\n"
			"Content-Type: text/plain\r\n"
			"\r\n"
			"Not found\r\n";
		write(fd, resp, sizeof(resp));
		close(fd);
	}
	return 0;

badrequest:
	{
		char resp[] = 
			"HTTP/1.1 400 Bad request\r\n"
			"Connection: close\r\n"
			"Content-Type: text/plain\r\n"
			"\r\n"
			"Bad request\r\n";
		write(fd, resp, sizeof(resp));
		close(fd);
	}
	return 0;

upgrade_websocket:
	{
		char *protocol = "Sec-WebSocket-Protocol:",
		     *websocket_key = "Sec-WebSocket-Key:",
		     *version = "Sec-WebSocket-Version:",
		     *guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11",
		     *key = NULL;

		unsigned int i;
		// find the key
		for (i = 0; i < header_count; i++) {
			if (strncmp(headers[i], websocket_key, strlen(websocket_key)) == 0) {
				char *tmp = trim(headers[i] + strlen(websocket_key));
				key = malloc(strlen(tmp) + strlen(guid) + 1);
				strcpy(key, tmp);
				strcat(key, guid);
				break;
			} else if (strncmp(headers[i], protocol, strlen(protocol)) == 0 ||
				   strncmp(headers[i], version, strlen(version)) == 0) {
				log_printf("%s\n", headers[i]);
			}
		}
		if (!key) goto badrequest;

		SHA1_CTX sha;
		uint8_t results[20];
		SHA1Init(&sha);
		SHA1Update(&sha, (uint8_t*)key, strlen(key));
		SHA1Final(results, &sha);

		char *accept = base64_encode(results, sizeof(results));

		char resp[200];
		int hdr_len = sprintf(resp, 
			"HTTP/1.1 101 Switching Protocols\r\n"
			"Upgrade: websocket\r\n"
			"Connection: Upgrade\r\n"
			"Sec-WebSocket-Accept: %s\r\n"
			"\r\n",
			accept);
		log_printf("%d %s", hdr_len, resp);
		write(fd, resp, hdr_len);

		if (client_fd != -1) {
			close(client_fd);  // close existing client
		}
		client_fd = fd;
	}
	return 0;

shutdown:
	if (srv_fd != -1) {
		close(srv_fd);
		srv_fd = -1;
	}
	if (client_fd != -1) {
		websocket_write(client_fd, OPCODE_CLOSE, 0, NULL, 0);
		close(client_fd);
		client_fd = -1;
		log_printf("websocket closed, restarting tipiservice\n");
	}
	exit(0); // restart service since websocket closed
}



/* These functions will be called from tipiports.c */

unsigned char websocket_readByte(int reg)
{
  websocket_serve();
  return regs[reg];
}


void websocket_writeByte(unsigned char value, int reg)
{
  regs[reg] = value;
  websocket_serveReg(reg);
}

static int resetProtocol(void)
{
  while (!resetSync)
    if (websocket_serve() < 0)
      return -1;
  resetSync = 0;
  return 0;
}

PyObject* websocket_sendMsg(unsigned char *data, int len)
{
  if (resetProtocol() < 0)
    return NULL;
  websocket_write(client_fd, OPCODE_BINARY, 0/*mask*/, data, len);
  Py_INCREF(Py_None);
  return Py_None;
}

PyObject* websocket_readMsg(void)
{
  if (resetProtocol() < 0)
    return NULL;
  while (!readMsg)
    if (websocket_serve() < 0)
      return NULL;
  PyObject *rc = readMsg;
  readMsg = NULL;
  return rc;
}

PyObject* websocket_sendMouseEvent(void)
{
  // send [dx, -dy, buttons]
  signed char msg[] = {
    dx < -128 ? -128 : dx > 127 ? 127 : dx,
    dy < -128 ? -128 : dy > 127 ? 127 : dy,
    buttons};
  dx -= msg[0];
  dy -= msg[1];
  //log_printf("%s: %d %d %d\n", __func__, msg[0], msg[1], msg[2]);
  return websocket_sendMsg((unsigned char*)msg, 3);
}



