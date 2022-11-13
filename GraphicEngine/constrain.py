def constrain(value: float, lowLimit: float, highLimit: float):
    return lowLimit if value < lowLimit else highLimit if value > highLimit else value
