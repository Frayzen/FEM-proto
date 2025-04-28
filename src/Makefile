CC=gcc
CFLAGS= -std=c99 -pedantic -Werror -Wall -Wextra -Wvla
LDFLAGS= 
OUT= out
SRCS = $(shell find $(SRC_DIR) -name '*.c' -a ! -path '*/tests/*')
OBJS = $(SRCS:.c=.o)

all: $(OBJS) cygen
	$(CC) $(LDFLAGS) -o $(OUT) $(OBJS)

clean:
	$(RM) -rf $(OUT) $(shell find . -name '*.o') cython

cygen:
	cygen -o cython $$(find cpp -name "*.hh") 

.PHONY: clean all

