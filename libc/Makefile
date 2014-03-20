CC=gcc
CCFLAGS=-O2 -std=c99

VectorTest: Vector.o VectorTest.o
	$(CC) -o $@ $^ $(CCFLAGS)

Vector.o: Vector.c Vector.h
	$(CC) -c Vector.c $(CCFLAGS)
VectorTest.o: VectorTest.c Vector.h
	$(CC) -c VectorTest.c $(CCFLAGS)
