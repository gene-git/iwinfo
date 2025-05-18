#
# Makefile for iwinfo, a wrapper for iwinfo.py
# which provides the needed capabilities:
# 	cap_net_raw, cap_net_admin
# Use small C-program to maximize security.
#

CFLAGS := -march=x86-64-v3 -mtune=generic -mshstk -O2 
CFLAGS += -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=3 
CFLAGS += -Wformat -Werror=format-security -fstack-clash-protection 
CFLAGS += -fcf-protection -std=gnu18

LF = -Wl,-z,now,-z,shstk,-z,cet-report=error
CF = $(CFLAGS) -Wall

.PHONY: iwinfo

iwinfo: ambient_cap_net.c
	@echo "On install: sudo setcap cap_setpcap,cap_net_raw,cap_net_admin+eip $@"
	gcc $(CF) -Wl,--no-as-needed $(LF) -lcap-ng -lc -o $@ $<

