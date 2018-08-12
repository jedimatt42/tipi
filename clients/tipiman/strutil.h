#ifndef _STRUTIL_H
#define _STRUTIL_H 1

void getstr(int x, int y, char* var, int limit);
int strcmp(const char* a, const char* b);
int indexof(const char* str, char c);
int basicToCstr(const char* str, char* buf);

#endif