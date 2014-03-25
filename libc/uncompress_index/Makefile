CC=gcc
CCFLAGS=-O2 -std=c99

UncompressIndexTest: UncompressIndexTest.o UncompressIndex.o ../Vector.o
	$(CC) -o $@ $^ $(CCFLAGS)
	$(CC) -shared -fPIC UncompressIndex.c $(CCFLAGS) -o UncompressIndex.so

UncompressIndex.o: UncompressIndex.c UncompressIndex.h
	$(CC) -c UncompressIndex.c $(CCFLAGS)
UncompressIndexTest.o: UncompressIndexTest.c UncompressIndex.h
	$(CC) -c UncompressIndexTest.c $(CCFLAGS)
