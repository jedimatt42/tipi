# convert an integer from -9999 to 9999 to a bytearray with value encoded
# as a float
def asFloat(val):
    bytes = bytearray(9)
    bytes[0] = 8

    word0 = 0
    word1 = 0
    tmp = val

    if val < 0:
        val *= -1

    if val >= 100:
        word0 = int(val // 100) | 0x4100
        word1 = int(val % 100)
    else:
        if val == 0:
            word0 = 0
        else:
            word0 = int(val) | 0x4000
        word1 = 0

    if tmp < 0:
        word0 = (~word0) + 1

    bytes[1] = (word0 >> 8) & 0xFF
    bytes[2] = word0 & 0xFF
    bytes[3] = word1 & 0xFF

    for i in range(4, 9):
        bytes[i] = 0

    return bytes


def asInt(bytes):
    if bytes[0] != 8:
        return 0
    word0 = (bytes[1] << 8) + bytes[2]
    word1 = bytes[3]

    neg = 1
    if (bytes[1] & 0xB0) == 0xB0:
        neg = -1
        word0 = ~(word0 - 1)

    val = 0
    if word0 & 0xFF00 == 0x4000:
        val = word0 & 0xFF
    if word0 & 0xFF00 == 0x4100:
        val = ((word0 & 0xFF) * 100) + (word1 & 0xFF)

    if neg == -1:
        val = -1 * val
    return val


if __name__ == "__main__":
    print(asInt(asFloat(0)))
    print(asInt(asFloat(1)))
    print(asInt(asFloat(6)))
    print(asInt(asFloat(128)))
    print(asInt(asFloat(-1)))
    print(asInt(asFloat(-6)))
    print(asInt(asFloat(-128)))
