all:
	gcc pmp.c -lm -lpthread -g -Wall -fopenmp -O2 -o pmp-testbench
	gcc rapl.c -o rapl -lm

clean:
	rm -f rapl pmp-testbench
