#pylint: skip-file
from RPi import GPIO
from subprocess import check_output
from smbus import SMBus
import datetime
import time
import KlasseLCD
import KlasseLCDPCF
import KlasseMCP
import serial

mcp = KlasseMCP.KlasseMCP()
lcd = KlasseLCD.KlasseLCD()
lcdp = KlasseLCDPCF.KlasseLCDPCF()
i2c = SMBus()
ser = serial.Serial('/dev/serial0')

knop1 = 18
knopStatus = 0
vorigeKnopStatus = 1

knop2 = 26

rood = 22
groen = 27
blauw = 17


def setup():
    global pwmRood
    global pwmGroen
    global pwmBlauw
    global vorigUur

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(knop1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(knop2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(rood, GPIO.OUT)
    GPIO.setup(groen, GPIO.OUT)
    GPIO.setup(blauw, GPIO.OUT)

    pwmRood = GPIO.PWM(rood, 1000)
    pwmGroen = GPIO.PWM(groen, 1000)
    pwmBlauw = GPIO.PWM(blauw, 1000)

    vorigUur = ""

    GPIO.add_event_detect(knop1, GPIO.RISING, callback=plus, bouncetime=500)
    GPIO.add_event_detect(knop2, GPIO.RISING,
                          callback=sendSeconds, bouncetime=500)

    lcdp.LCDInit()
    i2c.open(1)
    pwmRood.start(0)
    pwmGroen.start(0)
    pwmBlauw.start(0)
    print("Setup.")


def plus(channel):
    global knopStatus
    if knopStatus < 2:
        knopStatus = knopStatus + 1
    else:
        knopStatus = 0


def sendSeconds(channel):
    global vorigUur
    aantal = 0
    vorigeSeconds = ""
    while aantal < 5:
        seconds = getSeconds()
        if seconds != vorigeSeconds:
            aantal = aantal + 1
            ser.write(seconds.encode(encoding='utf-8'))
            ontvangen = ser.readline().decode(encoding='utf-8')
            ontvangen = ontvangen[0:len(ontvangen)-2]
            time.sleep(0.099)
    vorigUur = ""


def readJoystick():
    global knopStatus
    global vorigeKnopStatus
    if knopStatus == 0:
        if vorigeKnopStatus != 0:
            vorigeKnopStatus = 0
            ips = getIp()
            row1 = ips[0]
            lcdp.resetCLD()
            lcdp.sendMessage(row1)
            if len(ips) > 1:
                row2 = ips[1]
                lcdp.secondRow()
                lcdp.sendMessage(row2)

    elif knopStatus == 1:
        placeholder = "0"
        blocks = []
        if vorigeKnopStatus != 1:
            vorigeKnopStatus = 1
            row2 = f"WRX => "
            lcdp.resetCLD()
            lcdp.secondRow()
            lcdp.sendMessage(row2)

        lcdp.selecPosition(0x00)
        wrx = getmcp(0x80)
        for i in range(0, int((wrx / 1023) * 16)):
            blocks.append(0xff)
        while len(blocks) < 16:
            blocks.append(0xFE)
        lcdp.sendList(blocks)

        lcdp.selecPosition(0x47)
        wrx = str(wrx)
        while len(wrx) < 4:
            wrx = placeholder + wrx
        lcdp.sendMessage(wrx)

    elif knopStatus == 2:
        placeholder = "0"
        blocks = []
        if vorigeKnopStatus != 2:
            vorigeKnopStatus = 2
            row2 = f"WRY => "
            lcdp.resetCLD()
            lcdp.secondRow()
            lcdp.sendMessage(row2)

        lcdp.selecPosition(0x00)
        wry = getmcp(0x90)
        for i in range(0, int((wry / 1023) * 16)):
            blocks.append(0xff)
        while len(blocks) < 16:
            blocks.append(0xFE)
        lcdp.sendList(blocks)

        lcdp.selecPosition(0x47)
        wry = str(wry)
        while len(wry) < 4:
            wry = placeholder + wry
        lcdp.sendMessage(wry)
    rgb()


def getIp():
    ips = str(check_output(['hostname', '--all-ip-addresses']))
    ips = ips[2:len(ips)-4]
    ips = ips.split(" ")
    return ips


def getmcp(plaats):
    value = mcp.read_channel(plaats)
    return value


def rgb():
    rood = int((getmcp(0x80) / 1023) * 100)
    groen = int((getmcp(0x90) / 1023) * 100)
    blauw = int((rood+groen) / 2)

    pwmRood.ChangeDutyCycle(rood)
    pwmGroen.ChangeDutyCycle(groen)
    pwmBlauw.ChangeDutyCycle(blauw)


def getSeconds():
    uur = str(datetime.datetime.now())
    seconds = "10:10:" + uur[17] + ":" + uur[18]
    return seconds


def getTime():
    uur = str(datetime.datetime.now())
    message = uur[11] + ":" + uur[12] + ":" + uur[14] + ":" + uur[15]
    return message


def sendTime():
    global vorigUur
    uur = getTime()
    if vorigUur != uur:
        vorigUur = uur
        ser.write(uur.encode(encoding='utf-8'))
        ontvangen = ser.readline().decode(encoding='utf-8')
        ontvangen = ontvangen[0:len(ontvangen)-2]
        print(ontvangen)


setup()

try:
    while True:
        readJoystick()
        sendTime()


except KeyboardInterrupt as e:
    print(e)
finally:
    lcdp.displayOff()
    uit = "10:10:10:10"
    ser.write(uit.encode(encoding='utf-8'))
    GPIO.cleanup()
    mcp.close()
    i2c.close()
    ser.close()
    pwmRood.stop()
    pwmGroen.stop()
    pwmBlauw.stop()
    print("Cleanup.")
