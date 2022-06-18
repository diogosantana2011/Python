# Problem: Calculating Dopler shift

# Variable: speed of light (3x10e8)
speed_of_light = 300000000

# Variable: Bool for direction of car
is_towards = True

# Variable: My number XYZ
my_number = 1.01581

# Variable: velocity * 
velocity = 15 * my_number

# Variable: frequency (in Hz)
transmission_frequency = 2300000000

def calculate_doppler_shift(velocity, transmission_frequency, is_towards):
    """ Function which calculates doppler shift
        based on is_towards variable which indicates
        if source is moving towards(True), or away(False) from base station.
    """
        
    # Formula for doppler shift
    doppler_shift =  velocity * transmission_frequency / speed_of_light
    
    ## Test: Calculation is returned correctly.
    ## return doppler_shift

    
    # If condition to calculate
    ## depending on which direction the car is travelling
    if is_towards == True:
        transmission_frequency = transmission_frequency + doppler_shift
    elif is_towards == False:
        transmission_frequency = transmission_frequency - doppler_shift 
    return round(transmission_frequency, 2) / 1000000

if is_towards == True:
    print(f'The doppler shift while moving towards base station, based on transmission power {transmission_frequency / 1000000} MHz and velocity {round(velocity, 2)}/ms results in transmission of: ', calculate_doppler_shift(velocity, transmission_frequency, is_towards), 'MHz')
elif is_towards == False:
    print(f'The doppler shift while moving away from base station, based on transmission power {transmission_frequency / 1000000} MHz and velocity {round(velocity, 2)}/ms results in transmission of: ', calculate_doppler_shift(velocity, transmission_frequency, is_towards), 'MHz')
