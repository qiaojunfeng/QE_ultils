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
    if (narg == 1) then
        call get_command_argument(1, argkind)
        if (argkind == 'ls') then
            call ls_const()
            stop
        else
            call print_help()
            stop
        end if
    elseif (narg /= 2) then
        call print_help()
        stop
    end if

    call get_command_argument(1, argkind)
    call get_command_argument(2, argval)
    read(argval, *) inval

    select case(argkind)
    case('ry2ev')
        outval = conv(argkind, inval)
    case('ev2ry')
        outval = conv(argkind, inval)
    case('au2ev')
        outval = conv(argkind, inval)
    case('ev2au')
        outval = conv(argkind, inval)
    case('b2a')
        outval = conv(argkind, inval)
    case('a2b')
        outval = conv(argkind, inval)
    case default
        call print_help()
        stop
    end select

    write(*,'(G24.17)') outval

contains
real (DP) function conv(argkind, inval)
    USE kinds, ONLY : DP
    USE constants
    implicit none
    character(len=256), intent(in) :: argkind
    real (DP), intent(in) :: inval

    if (argkind == 'ry2ev') then
        conv = inval * RYTOEV
    elseif (argkind == 'ev2ry') then
        conv = inval / RYTOEV
    elseif (argkind == 'au2ev') then
        conv = inval * AUTOEV
    elseif (argkind == 'ev2au') then
        conv = inval / AUTOEV
    elseif (argkind == 'b2a') then
        conv = inval * BOHR_RADIUS_ANGS
    elseif (argkind == 'a2b') then
        conv = inval / BOHR_RADIUS_ANGS
    else
        stop
    end if
end function conv

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
    &'    b2a  : bohr to angstrom' // NEW_LINE('a') // &
    &'    a2b  : angstrom to bohr' // NEW_LINE('a') // &
    &'    ls   : list all constant in QE'

    write(*, '(a)', ADVANCE='no') help_info
    write(*, '(a)') ''
end subroutine print_help

subroutine ls_const()
! code generated by qe-6.0/Modules/constants.f90
    USE kinds, ONLY : DP
    USE constants
    implicit none

    write(*,'(A18,G24.17)') 'pi:',pi
    write(*,'(A18,G24.17)') 'tpi:',tpi
    write(*,'(A18,G24.17)') 'fpi:',fpi
    write(*,'(A18,G24.17)') 'sqrtpi:',sqrtpi
    write(*,'(A18,G24.17)') 'sqrtpm1:',sqrtpm1
    write(*,'(A18,G24.17)') 'sqrt2:',sqrt2
    write(*,'(A18,G24.17)') 'H_PLANCK_SI:',H_PLANCK_SI
    write(*,'(A18,G24.17)') 'K_BOLTZMANN_SI:',K_BOLTZMANN_SI
    write(*,'(A18,G24.17)') 'ELECTRON_SI:',ELECTRON_SI
    write(*,'(A18,G24.17)') 'ELECTRONVOLT_SI:',ELECTRONVOLT_SI
    write(*,'(A18,G24.17)') 'ELECTRONMASS_SI:',ELECTRONMASS_SI
    write(*,'(A18,G24.17)') 'HARTREE_SI:',HARTREE_SI
    write(*,'(A18,G24.17)') 'RYDBERG_SI:',RYDBERG_SI
    write(*,'(A18,G24.17)') 'BOHR_RADIUS_SI:',BOHR_RADIUS_SI
    write(*,'(A18,G24.17)') 'AMU_SI:',AMU_SI
    write(*,'(A18,G24.17)') 'C_SI:',C_SI
    write(*,'(A18,G24.17)') 'MUNOUGHT_SI:',MUNOUGHT_SI
    write(*,'(A18,G24.17)') 'EPSNOUGHT_SI:',EPSNOUGHT_SI
    write(*,'(A18,G24.17)') 'K_BOLTZMANN_AU:',K_BOLTZMANN_AU
    write(*,'(A18,G24.17)') 'K_BOLTZMANN_RY:',K_BOLTZMANN_RY
    write(*,'(A18,G24.17)') 'AUTOEV:',AUTOEV
    write(*,'(A18,G24.17)') 'RYTOEV:',RYTOEV
    write(*,'(A18,G24.17)') 'AMU_AU:',AMU_AU
    write(*,'(A18,G24.17)') 'AMU_RY:',AMU_RY
    write(*,'(A18,G24.17)') 'AU_SEC:',AU_SEC
    write(*,'(A18,G24.17)') 'AU_PS:',AU_PS
    write(*,'(A18,G24.17)') 'AU_GPA:',AU_GPA
    write(*,'(A18,G24.17)') 'RY_KBAR:',RY_KBAR
    write(*,'(A18,G24.17)') 'DEBYE_SI:',DEBYE_SI
    write(*,'(A18,G24.17)') 'AU_DEBYE:',AU_DEBYE
    write(*,'(A18,G24.17)') 'eV_to_kelvin:',eV_to_kelvin
    write(*,'(A18,G24.17)') 'ry_to_kelvin:',ry_to_kelvin
    write(*,'(A18,G24.17)') 'EVTONM:',EVTONM
    write(*,'(A18,G24.17)') 'RYTONM:',RYTONM
    write(*,'(A18,G24.17)') 'C_AU:',C_AU
    write(*,'(A18,G24.17)') 'eps4:',eps4
    write(*,'(A18,G24.17)') 'eps6:',eps6
    write(*,'(A18,G24.17)') 'eps8:',eps8
    write(*,'(A18,G24.17)') 'eps12:',eps12
    write(*,'(A18,G24.17)') 'eps14:',eps14
    write(*,'(A18,G24.17)') 'eps16:',eps16
    write(*,'(A18,G24.17)') 'eps24:',eps24
    write(*,'(A18,G24.17)') 'eps32:',eps32
    write(*,'(A18,G24.17)') 'gsmall:',gsmall
    write(*,'(A18,G24.17)') 'e2:',e2
    write(*,'(A18,G24.17)') 'degspin:',degspin
    write(*,'(A18,G24.17)') 'BOHR_RADIUS_CM:',BOHR_RADIUS_CM
    write(*,'(A18,G24.17)') 'BOHR_RADIUS_ANGS:',BOHR_RADIUS_ANGS
    write(*,'(A18,G24.17)') 'ANGSTROM_AU:',ANGSTROM_AU
    write(*,'(A18,G24.17)') 'DIP_DEBYE:',DIP_DEBYE
    write(*,'(A18,G24.17)') 'AU_TERAHERTZ:',AU_TERAHERTZ
    write(*,'(A18,G24.17)') 'AU_TO_OHMCMM1:',AU_TO_OHMCMM1
    write(*,'(A18,G24.17)') 'RY_TO_THZ:',RY_TO_THZ
    write(*,'(A18,G24.17)') 'RY_TO_GHZ:',RY_TO_GHZ
    write(*,'(A18,G24.17)') 'RY_TO_CMM1:',RY_TO_CMM1

end subroutine ls_const
