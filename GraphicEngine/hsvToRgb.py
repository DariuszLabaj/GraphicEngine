def hsvToRgb(hue: int, saturation: float = 1.0, value: float = 1.0):
    if hue < 0 or hue > 359:
        raise ValueError
    if saturation < 0 or saturation > 1.0:
        raise ValueError
    if value < 0 or value > 1.0:
        raise ValueError

    c = value * saturation
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = value - c

    if 0 <= hue < 60:
        rp, gp, bp = c, x, 0
    elif 60 <= hue < 120:
        rp, gp, bp = x, c, 0
    elif 120 <= hue < 180:
        rp, gp, bp = 0, c, x
    elif 180 <= hue < 240:
        rp, gp, bp = 0, x, c
    elif 240 <= hue < 300:
        rp, gp, bp = x, 0, c
    elif 300 <= hue < 360:
        rp, gp, bp = c, 0, x
    r, g, b = (rp + m) * 255, (gp + m) * 255, (bp + m) * 255
    return (int(r), int(g), int(b))
