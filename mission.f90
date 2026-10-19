program mission
    use iso_fortran_env, only: real64
    implicit none
    real(real64), parameter :: speed = 24000.0_real64
    integer :: day
    print '(A)', 'MISSION DISTANCE REPORT'
    do day = 1, 5
        print '(A,I0,A,F12.0,A)', &
            'Day ', day, ': ', distance_km(speed, day), ' km'
    end do
contains
    function distance_km(speed_kmh, day) result(distance)
        real(real64), intent(in) :: speed_kmh
        integer, intent(in) :: day
        real(real64) :: distance
        distance = speed_kmh * real(day, real64) * 24.0_real64
    end function distance_km
end program mission
