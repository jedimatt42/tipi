

# convert an integer from -9999 to 9999 to a bytearray with value encoded as a float
def asFloat(val):
    bytes = bytearray(9)
    bytes[0] = 8
    
    word0 = 0
    word1 = 0
    tmp = val

    if val < 0:
        val *= -1

    if val >= 100:
        word0 = (val / 100) | 0x4100
        word1 = val % 100
    else:
        if val == 0:
            word0 = 0
        else:
            word0 = val | 0x4000
        word1 = 0

    if tmp < 0:
        word0 = (~word0)+1

    bytes[1] = (word0 >> 8) & 0xff
    bytes[2] = word0 & 0xff
    bytes[3] = word1 & 0xff

    for i in range(4,9):
        bytes[i] = 0

    return bytes

