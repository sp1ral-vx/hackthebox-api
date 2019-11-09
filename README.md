# HackTheBox API

* Unofficial python wrapper for hackthebox.eu API.
* Simple CLI application.

## Installation

`pip install hackthebox-api`

## Usage

```
$ hackthebox.py
Please set HTB API key to your environ
$ export HTB_API_KEY='...' ## https://www.hackthebox.eu/home/settings
$ hackthebox.py -h
usage: hackthebox.py [-h] [-l] [-n NAME] [--reset] [-f flag] [-d difficulty]
                     [--shout message] [--aggressive]

HackTheBox CLI

optional arguments:
  -h, --help            show this help message and exit
  -l                    list available machines
  -n NAME               filter machine by name
  --reset               reset machine
  -f flag, --flag flag  Submit flag
  -d difficulty         Rate difficulty
  --shout message       Write message to shoutbox
  --aggressive          Monitor shoutbox for machine resets and automatically
                        cancel them
```
