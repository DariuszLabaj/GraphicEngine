def constrain(value: float, lowLimit: float, highLimit: float):
    if value <= lowLimit:
        return lowLimit
    if value >= highLimit:
        return highLimit
    return value
