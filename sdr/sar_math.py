# MATH.PY
# Secondary functions for the SDR Solution

def calculate_range_resolution(bandwidth):
    # Speed of light in meters per second
    speed_of_light = 3e8
    
    # Calculate range resolution using the formula: ΔR = c / (2 * B)
    range_resolution = speed_of_light / (2 * bandwidth)
    
    return range_resolution


def calculate_chirp_rate(bandwidth, pulse_duration):
    # Calculate chirp rate using the formula: β = B / Tp
    chirp_rate = bandwidth / pulse_duration
    return chirp_rate
