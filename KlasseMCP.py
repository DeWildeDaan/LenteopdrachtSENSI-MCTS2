import spidev
spi = spidev.SpiDev()


class KlasseMCP:
    # Constructor
    def __init__(self, bus=0, slave=0):
        self.bus = bus
        self.slave = slave
        spi.open(self.bus, self.slave)  # Bus SPI0, slave op CE 0
        spi.max_speed_hz = 10 ** 5

    def read_channel(self, channel):
        bytes_out = [0x1, channel, 0x0]
        bytes_in = spi.xfer(bytes_out)
        x = bytes_in[1]
        y = bytes_in[2]
        uitkomst = ((x & 3) << 8) | y
        return uitkomst

    def close(self):
        spi.close()
