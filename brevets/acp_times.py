"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

LIMITS = [
    (0, 200, 15, 34),
    (200, 400, 15, 32),
    (400, 600, 15, 30),
    (600, 1000, 11.428, 28),
    (1000, 1300, 13.333, 26)]

# Only used once, but holds race-dependent information
CLOSE_TIMES = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    current_dist = min(control_dist_km, brevet_dist_km)
    current_time = 0

    for lower, upper, min_speed, max_speed in LIMITS:
        if current_dist > lower:
            distance_covered = min(current_dist, upper) - lower
            current_time += distance_covered / max_speed

    return brevet_start_time.shift(minutes=round(current_time * 60))



def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    control_dist_km = round(control_dist_km)
    current_dist = min(control_dist_km, brevet_dist_km)
    current_time = 0

    if current_dist >= brevet_dist_km:
        return brevet_start_time.shift(hours=CLOSE_TIMES.get(brevet_dist_km, 0))

    for lower, upper, min_speed, max_speed in LIMITS:
        if current_dist > lower:
            distance_covered = min(current_dist, upper) - lower
            current_time += distance_covered / min_speed

    if control_dist_km <= 60:
        current_time = max(current_time, control_dist_km / 20 + 1)

    return brevet_start_time.shift(hours=current_time)