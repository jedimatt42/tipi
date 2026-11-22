# Running TIPI locally for emulators

Emulators that support TIPI (MAME, js99er.net and others) connect to TIPI's
services over a websocket. Those services normally run on a Raspberry PI, or
in the QEMU PI image described in [../README.md](../README.md). The scripts in
this folder run the same services directly on a Mac (or a Linux PC), with no
PI or virtual machine.

What runs:

- the TIPI service (`services/tipi.sh`), with the emulator websocket at
  `ws://localhost:9901/tipi`
- the web UI (`htdocs/app_run.sh`) at http://localhost:9900
- the file monitor (`htdocs/tipimon.sh`) that keeps the web UI's file
  cache current

## Requirements

- Python 3 (on a Mac, Homebrew's `python3` works; tested with 3.15)
- git, and a C compiler (on a Mac, the Xcode command line tools)

## Setup

Run once, and again after updating this checkout:

```bash
emulation/local/setup.sh
```

This creates the Python environments `services/ENV` and `htdocs/ENV`, builds
the websocket library, and clones [xdt99](https://github.com/endlos99/xdt99)
into `$TIPI_HOME/xdt99`. Set `PYTHON` to use a different Python, for example
`PYTHON=python3.13 emulation/local/setup.sh`.

## Running

```bash
emulation/local/run.sh
```

Stop it with Ctrl-C. Each service is restarted if it exits, as systemd does
on the PI. Their output goes to `$TIPI_HOME/log/*.out`, and the TIPI service's
own log to `$TIPI_HOME/log/tipi.log`.

Then point the emulator's TIPI setting at `localhost` (port 9901).

## Where files live

Everything that lives under `/home/tipi` on a PI lives under `$TIPI_HOME`,
which defaults to `~/tipi`:

| Path | Contents |
|---|---|
| `tipi_disk/` | the TIPI. device's files |
| `tipi.config` | settings, as edited by TIPICFG or the web UI |
| `tipi.uuid` | this TIPI's id, created on the first run |
| `.emulation` | emulation mode settings |
| `.tipivars/`, `.tipiweb.db`, `web-tmp/` | runtime state |
| `log/` | logs |
| `xdt99/` | tools for BASIC programs and disk images |

To use an existing folder of TIPI files, point `TIPI_HOME` at a folder that
holds it as `tipi_disk`, for both scripts:

```bash
TIPI_HOME=~/my-tipi emulation/local/setup.sh
TIPI_HOME=~/my-tipi emulation/local/run.sh
```

The first run copies TIPICFG and the other programs from `setup/bin` into
`tipi_disk`, without replacing files already there.

## Not available locally

These need the PI's operating system and are ignored, with a message from
`run.sh`: WiFi and timezone settings, upgrade, reboot and shutdown, and backup
and restore. PDF printing and tidbit (BASIC listing renumbering in the web UI)
aren't set up.

## How it works

The services find their files through two environment variables, which
`run.sh` sets:

- `TIPI_HOME`: the PI's `/home/tipi` (the default when it isn't set)
- `TIPI_REPO`: this checkout, `/home/tipi/tipi` on the PI

`run.sh` also sets `TIPI_WEBSOCK`, which selects the websocket instead of the
PI's GPIO port, and stands in for `TipiSuper.py` by restarting the TIPI service
when the web UI asks.
