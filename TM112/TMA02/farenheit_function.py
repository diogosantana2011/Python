# Farneheit converter function

# Input
celsius_values = [20, 18, 22, 33]

def farenheit(celsius):
    """
    Conversion from °C to °F (((°C * 9)/5) + 32)
    """
    return ((9 * celsius) / 5) + 32

def farenheit_list(celsius_list):
    """
    Convert a list of temperatures in Celsius,
    to Farenheit
    """
    for i in range(0, len(celsius_list)):
        celsius_list[i] = farenheit(celsius_list[i])
    return celsius_list
    
print(farenheit_list(celsius_values))