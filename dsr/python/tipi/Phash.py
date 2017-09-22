
import random
import Ptable


class Phash:

    def __init__(self):
        self.table = Ptable.table

    def digestAll(self, hash, bytes):
        value = hash
        for byte in bytes:
            value = self.digest(value, byte)
        return value

    def digest(self, hash, byte):
        return self.table[hash ^ byte]

    def printTable(self):
        generator = random.Random()
        generator.seed("TIPI")
        table = list(range(256))
        generator.shuffle(table)

        chunks = [table[i::64] for i in range(64)]
        for ch in chunks:
            print "\tbyte\t{},{},{},{}".format(ch[0], ch[1], ch[2], ch[3])


# uncomment to regenerate the table.
# phash = PHash()

# phash.printTable()
