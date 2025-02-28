#!/bin/sh

####### FLAGS

CC      = gcc
CFLAGS  = -O2 -Wall -g -ansi
LIBS    = -lm

# Source and Object Files
SOURCES = construction.c
OBJECTS = $(SOURCES:.c=.o)

####### Build Rules

# Default target
all: construction

# Build the generator
construction: $(OBJECTS)
	$(CC) -o construction $(OBJECTS) $(CFLAGS) $(LIBS)

# Clean up build files
clean:
	rm -f *.o *.bak *~ core construction

# Very clean removes all auxiliary files
veryclean: clean
	rm -f construction_output.txt

lint:
	lclint -booltype Bool $(SOURCES) 2> lint_output.txt

# DO NOT DELETE

