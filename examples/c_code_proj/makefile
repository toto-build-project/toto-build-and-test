CC = g++
CFLAGS = -g -Wall

default: test

all: test

install:  
	cp test test2
	tar -cvf create_test2_exe.tar test2 addr_seed

test: counter.o main.o
	$(CC) -o test counter.o main.o

main.o: counter.o main.cpp
	$(CC) $(CFLAGS) -w -fpermissive -v -c main.cpp

counter.o: counter.h
	$(CC) $(CFLAGS) -c counter.cpp

clean:
	rm -f  test test2 *.o *.tar
