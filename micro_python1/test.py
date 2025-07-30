import uasyncio as asyncio
from machine import Pin, I2C, SPI, UART, PWM
import time
import network
import socket
import ssd1306
import mfrc522
from time import sleep

# --- Motor Setup ---
motor_in1 = Pin(12, Pin.OUT)
motor_in2 = Pin(13, Pin.OUT)

def motor_forward():
    motor_in1.value(1)
    motor_in2.value(0)

def motor_reverse():
    motor_in1.value(0)
    motor_in2.value(1)

def motor_stop():
    motor_in1.value(0)
    motor_in2.value(0)

# --- Buzzer Setup ---
buzzer = Pin(10, Pin.OUT)

def beep(duration=0.1):
    buzzer.value(1)
    time.sleep(duration)
    buzzer.value(0)

def error_beep():
    for _ in range(2):
        beep(0.2)
        time.sleep(0.1)

# --- OLED Display Setup (SSD1306 over I2C) ---
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def oled_show(msg1="", msg2="", msg3=""):
    oled.fill(0)
    oled.text(msg1, 0, 0)
    oled.text(msg2, 0, 16)
    oled.text(msg3, 0, 32)
    oled.show()

# --- DFPlayer Mini Setup (UART) ---
dfplayer_uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))  # Set to your TX/RX pins
dfplayer_uart.init(bits=8, parity=None, stop=2)

# --- DFPlayer Mini Functions ---
def send_dfplayer_command(command, param1=0, param2=0):
    command_bytes = bytearray([0x7E, 0xFF, 0x06, 0x00, command, param1, param2, 0x7E])
    checksum = sum(command_bytes[1:7]) & 0xFF
    command_bytes[6] = checksum
    dfplayer_uart.write(command_bytes)

def play_mp3(track):
    send_dfplayer_command(0x03, track, 0x00)  # Play the MP3 track

def stop_mp3():
    send_dfplayer_command(0x16, 0x00, 0x00)  # Stop the current MP3

# --- Wi-Fi Setup ---
ssid = 'Your_SSID'
password = 'Your_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print("Connecting to WiFi...", end='')
while not wlan.isconnected():
    print(".", end='')
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("Connected, IP:", ip)

html = """
<!DOCTYPE html>
<html>
<head><title>Motor Control</title></head>
<body>
    <h2>Motor Control Panel</h2>
    <form action="/" method="get">
        <button name="action" value="forward">Forward</button>
        <button name="action" value="reverse">Reverse</button>
        <button name="action" value="stop">Stop</button>
    </form>
</body>
</html>
"""

# --- RFID Setup (MFRC522) ---
spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))
rfid = mfrc522.MFRC522(spi=spi, gpio_rst=Pin(0), gpio_cs=Pin(5))

# --- TTP229 Keypad (I2C Address 0x57) ---
TTP229_ADDR = 0x57

# --- Fingerprint Sensor Setup (UART) ---
uart = UART(1, baudrate=57600, tx=Pin(8), rx=Pin(9))

# --- RFID Reader Task ---
async def check_rfid():
    while True:
        (stat, tag_type) = rfid.request(rfid.REQIDL)
        if stat == rfid.OK:
            (stat, raw_uid) = rfid.anticoll()
            if stat == rfid.OK:
                uid = ''.join('{:02X}'.format(b) for b in raw_uid)
                print("RFID UID:", uid)
                oled_show("RFID UID:", uid, "Access OK")
                play_mp3(1)  # Play welcome sound (track 1)
                motor_forward()
                await asyncio.sleep(1)
        await asyncio.sleep(0.1)

# --- Keypad Task ---
async def check_keypad():
    while True:
        data = i2c.readfrom(TTP229_ADDR, 2)
        key = decode_ttp229(data)
        if key:
            print("Keypad:", key)
            beep(0.05)
            oled_show("Key Pressed:", str(key), "")
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.05)

# --- Fingerprint Task ---
async def check_fingerprint():
    while True:
        read_fingerprint()
        await asyncio.sleep(0.2)

# --- Motor Control Web Server ---
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

async def web_server():
    while True:
        cl, addr = s.accept()
        request = cl.recv(1024)
        request = str(request)
        print("Request:", request)

        if '/?action=forward' in request:
            motor_forward()
        elif '/?action=reverse' in request:
            motor_reverse()
        elif '/?action=stop' in request:
            motor_stop()

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()

# --- Main Task ---
async def main():
    oled_show("System Init...", "", "")
    await asyncio.sleep(1)
    await asyncio.gather(
        check_rfid(),
        check_keypad(),
        check_fingerprint(),
        web_server()  # Add web server to run alongside other tasks
    )

# Start the event loop
asyncio.run(main())
