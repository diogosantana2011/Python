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
    to Farenheit - v2.
    """
    farenheit_list = []
    for celsius_temp in celsius_list:
        farenheit_temp = farenheit(celsius_temp)
        farenheit_list = farenheit_list + [farenheit_temp]
    return farenheit_list

# Output
print(farenheit_list(celsius_values))