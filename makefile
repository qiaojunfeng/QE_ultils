F90=gfortran

default: constants kinds
	$(F90) -o pwuc pwuc.f90
	./pwuc ry2ev 1
	./pwuc ev2ry 1
	./pwuc au2ev 1
	./pwuc ev2au 1
	./pwuc b2a 1
	./pwuc a2b 1
	./pwuc ls
	./pwuc

constants: kinds
	$(F90) -c constants.f90

kinds:
	$(F90) -c kind.f90

clean:
	rm *.o *.mod
	rm pwuc
