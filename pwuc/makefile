F90=gfortran

default: constants kinds
	$(F90) -o pwuc.x pwuc.f90
	./pwuc.x ry2ev 1
	./pwuc.x ev2ry 1
	./pwuc.x au2ev 1
	./pwuc.x ev2au 1
	./pwuc.x b2a 1
	./pwuc.x a2b 1
	./pwuc.x ls
	./pwuc.x

constants: kinds
	$(F90) -c constants.f90

kinds:
	$(F90) -c kind.f90

clean:
	rm *.o *.mod
	rm pwuc.x
