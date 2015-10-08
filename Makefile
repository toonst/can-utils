CC=gcc
CFLAGS="-Wall"

debug:clean
	$(CC) $(CFLAGS) -g -o can_sniffer_v2 cansniffer.c
stable:clean
	$(CC) $(CFLAGS) -o can_sniffer_v2 cansniffer.c
clean:
	rm -vfr *~ can_sniffer_v2
