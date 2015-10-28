CC=gcc
CFLAGS="-Wall"
DEPS="../other_tools"

debug:clean
	$(CC) $(CFLAGS) -g -o can_sniffer_v2 cansniffer.c -I$(DEPS)
stable:clean
	$(CC) $(CFLAGS) -o can_sniffer_v2 cansniffer.c -I$(DEPS)
clean:
	rm -vfr *~ can_sniffer_v2
