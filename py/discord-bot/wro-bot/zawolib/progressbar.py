"""  Progress Bar Normal Progress Bar  """
""" /  normal devide """
""" // int only devide """

import math

def progress_bar (value, minvalue=0, maxvalue=100, prefix = '', suffix = ' ', decimals = 1, length = 20, fill='▓', nofill='░', showUnits=False, unit=''):#chars:⠀,░,█,▓
    #iteration = min(iteration, total)
    percent = ("{0:." + str(decimals) + "f}").format(100 * ((value-minvalue) / float(maxvalue-minvalue)))
    filledLength = max(0, min(int(round(length * (value-minvalue) / (maxvalue-minvalue), 0)), length))
    bar = fill * filledLength + nofill * (length - filledLength)

    returnstr = f'\r{prefix}{bar}{suffix}'

    if showUnits:
        if unit == '%': 
            returnstr += f'{percent}{unit} '
        else: 
            returnstr += f'{value}{unit} '

    return returnstr
