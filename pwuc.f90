! list all available constants and derived values

PROGRAM pwuc
  USE kinds, ONLY : DP
  USE constants

  implicit none
  integer :: narg, stat
  character(len=256) :: argkind, argval
  real (DP) :: inval, outval

  call get_command(status=stat)
  if (stat /= 0) then
    call print_help()
    stop
  end if

  narg = command_argument_count()
  if (narg /= 2) then
    call print_help()
    stop
  end if

  call get_command_argument(1, argkind)
  call get_command_argument(2, argval)
  read(argval, *) inval
  if (argkind == 'ry2ev') then
    outval = inval * RYTOEV
  elseif (argkind == 'ev2ry') then
    outval = inval / RYTOEV
  elseif (argkind == 'au2ev') then
    outval = inval * AUTOEV
  elseif (argkind == 'ev2au') then
    outval = inval / AUTOEV
  elseif (argkind == 'b2a') then
    outval = inval * BOHR_RADIUS_ANGS
  elseif (argkind == 'a2b') then
    outval = inval / BOHR_RADIUS_ANGS
  else
    call print_help()
    stop
  end if

  write(*,'(G24.17)') outval

! WRITE (*,'(A18,G24.17)') 'pi:',pi
! WRITE (*,'(A18,G24.17)') 'tpi:',tpi
! WRITE (*,'(A18,G24.17)') 'fpi:',fpi
! WRITE (*,'(A18,G24.17)') 'sqrtpi:',sqrtpi
! WRITE (*,'(A18,G24.17)') 'sqrtpm1:',sqrtpm1
! WRITE (*,'(A18,G24.17)') 'sqrt2:',sqrt2
! WRITE (*,'(A18,G24.17)') 'H_PLANCK_SI:',H_PLANCK_SI
! WRITE (*,'(A18,G24.17)') 'K_BOLTZMANN_SI:',K_BOLTZMANN_SI
! WRITE (*,'(A18,G24.17)') 'ELECTRON_SI:',ELECTRON_SI
! WRITE (*,'(A18,G24.17)') 'ELECTRONVOLT_SI:',ELECTRONVOLT_SI
! WRITE (*,'(A18,G24.17)') 'ELECTRONMASS_SI:',ELECTRONMASS_SI
! WRITE (*,'(A18,G24.17)') 'HARTREE_SI:',HARTREE_SI
! WRITE (*,'(A18,G24.17)') 'RYDBERG_SI:',RYDBERG_SI
! WRITE (*,'(A18,G24.17)') 'BOHR_RADIUS_SI:',BOHR_RADIUS_SI
! WRITE (*,'(A18,G24.17)') 'AMU_SI:',AMU_SI
! WRITE (*,'(A18,G24.17)') 'C_SI:',C_SI
! WRITE (*,'(A18,G24.17)') 'MUNOUGHT_SI:',MUNOUGHT_SI
! WRITE (*,'(A18,G24.17)') 'EPSNOUGHT_SI:',EPSNOUGHT_SI
! WRITE (*,'(A18,G24.17)') 'K_BOLTZMANN_AU:',K_BOLTZMANN_AU
! WRITE (*,'(A18,G24.17)') 'K_BOLTZMANN_RY:',K_BOLTZMANN_RY
! WRITE (*,'(A18,G24.17)') 'AUTOEV:',AUTOEV
! WRITE (*,'(A18,G24.17)') 'RYTOEV:',RYTOEV
! WRITE (*,'(A18,G24.17)') 'AMU_AU:',AMU_AU
! WRITE (*,'(A18,G24.17)') 'AMU_RY:',AMU_RY
! WRITE (*,'(A18,G24.17)') 'AU_SEC:',AU_SEC
! WRITE (*,'(A18,G24.17)') 'AU_PS:',AU_PS
! WRITE (*,'(A18,G24.17)') 'AU_GPA:',AU_GPA
! WRITE (*,'(A18,G24.17)') 'RY_KBAR:',RY_KBAR
! WRITE (*,'(A18,G24.17)') 'DEBYE_SI:',DEBYE_SI
! WRITE (*,'(A18,G24.17)') 'AU_DEBYE:',AU_DEBYE
! WRITE (*,'(A18,G24.17)') 'eV_to_kelvin:',eV_to_kelvin
! WRITE (*,'(A18,G24.17)') 'ry_to_kelvin:',ry_to_kelvin
! WRITE (*,'(A18,G24.17)') 'EVTONM:',EVTONM
! WRITE (*,'(A18,G24.17)') 'RYTONM:',RYTONM
! WRITE (*,'(A18,G24.17)') 'C_AU:',C_AU
! WRITE (*,'(A18,G24.17)') 'eps4:',eps4
! WRITE (*,'(A18,G24.17)') 'eps6:',eps6
! WRITE (*,'(A18,G24.17)') 'eps8:',eps8
! WRITE (*,'(A18,G24.17)') 'eps12:',eps12
! WRITE (*,'(A18,G24.17)') 'eps14:',eps14
! WRITE (*,'(A18,G24.17)') 'eps16:',eps16
! WRITE (*,'(A18,G24.17)') 'eps24:',eps24
! WRITE (*,'(A18,G24.17)') 'eps32:',eps32
! WRITE (*,'(A18,G24.17)') 'gsmall:',gsmall
! WRITE (*,'(A18,G24.17)') 'e2:',e2
! WRITE (*,'(A18,G24.17)') 'degspin:',degspin
! WRITE (*,'(A18,G24.17)') 'BOHR_RADIUS_CM:',BOHR_RADIUS_CM
! WRITE (*,'(A18,G24.17)') 'BOHR_RADIUS_ANGS:',BOHR_RADIUS_ANGS
! WRITE (*,'(A18,G24.17)') 'ANGSTROM_AU:',ANGSTROM_AU
! WRITE (*,'(A18,G24.17)') 'DIP_DEBYE:',DIP_DEBYE
! WRITE (*,'(A18,G24.17)') 'AU_TERAHERTZ:',AU_TERAHERTZ
! WRITE (*,'(A18,G24.17)') 'AU_TO_OHMCMM1:',AU_TO_OHMCMM1
! WRITE (*,'(A18,G24.17)') 'RY_TO_THZ:',RY_TO_THZ
! WRITE (*,'(A18,G24.17)') 'RY_TO_GHZ:',RY_TO_GHZ
! WRITE (*,'(A18,G24.17)') 'RY_TO_CMM1:',RY_TO_CMM1

END PROGRAM pwuc

subroutine print_help()
    implicit none
    character (len=1024) :: help_info
    help_info = 'Quantum ESPRESSO unit conversion tool' // NEW_LINE('a') // &
    & NEW_LINE('a') // &
    &'Usage: pwuc arg1 arg2' // NEW_LINE('a') // &
    &'arg2: real value' // NEW_LINE('a') // &
    &'arg1:' // NEW_LINE('a') // &
    &'    ry2ev: Rydberg to electron volt' // NEW_LINE('a') // &
    &'    ev2ry: electron volt to Rydberg' // NEW_LINE('a') // &
    &'    au2ev: atomic unit to electron volt' // NEW_LINE('a') // &
    &'    ev2au: electron volt to atomic unit' // NEW_LINE('a') // &
    &'    b2a  : bohr to angstrom' // NEW_LINE('a') //&
    &'    a2b  : angstrom to bohr' // NEW_LINE('a')

    write(*, '(a)', ADVANCE='no') help_info
    write(*, '(a)') ''
end subroutine print_help

