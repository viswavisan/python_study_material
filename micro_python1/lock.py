import uasyncio as asyncio
import framebuf,neopixel
from machine import Pin, PWM, I2C
import time

class OLED(framebuf.FrameBuffer):
    def __init__(self):
        self.x=0
        self.y=0
        SET_DISP = const(0xAE)
        SET_MEM_ADDR = const(0x20)
        SET_COL_ADDR = const(0x21)
        SET_PAGE_ADDR = const(0x22)
        SET_CONTRAST = const(0x81)
        self.i2c=I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
        width,height,self.addr=128,64,0x3C
        self.buffer = bytearray((height // 8) * width)
        super().__init__(self.buffer, width, height, framebuf.MONO_VLSB)
        cmds = [ SET_DISP | 0x00, SET_MEM_ADDR, 0x00, SET_COL_ADDR, 0, 128 - 1, SET_PAGE_ADDR, 0, (height // 8) - 1, SET_CONTRAST, 0xFF, SET_DISP | 0x01 ,0xA1]
        for cmd in cmds:self.i2c.writeto(self.addr, bytearray([0x80, cmd]))
        self.clear()
       
    def show(self):
        self.i2c.writeto(self.addr, bytearray([0x40]) + self.buffer)
    
    def clear(self):
        self.fill(0)
        self.show()

    def sleep(self):
        self.i2c.writeto(self.addr, bytearray([0x80, 0xAE]))
    def wake(self):
        self.i2c.writeto(self.addr, bytearray([0x80, 0xAF]))

class lock:
    def __init__(self):
        #set pins
        self.keypad_r=[Pin(i, Pin.OUT) for i in (7,6,5,4)]
        self.keypad_c=[Pin(i, Pin.IN, Pin.PULL_DOWN) for i in (3,2,1,0)]
        self.buzzer = Pin( 19, Pin.OUT)
        self.lock   = Pin(17, Pin.OUT)
        self.scl    = Pin(27)
        self.sda    = Pin(26)
        self.keys   = [['1', '2', '3', 'A'],['4', '5', '6', 'B'],['7', '8', '9', 'C'],['*', '0', '#', 'D']]
        self.last_keypress=time.ticks_ms()
        self.mode   ='wake'
        self.password=''
        # self.oled=OLED()
        # self.reset()
        asyncio.create_task(self.keypad_task(self.on_keypress))

    def reset(self):
        self.password=''
        self.oled.wake()
        self.oled.clear()
        self.oled.text('welcome',0,0)
        self.oled.text('enter password',0,16)
        self.oled.show()
        self.oled.x=0

    async def keypad_task(self,callback):
        while True:
            for row_index, row in enumerate(self.keypad_r):
                row.value(1)
                for col_index, col in enumerate(self.keypad_c):
                    if col.value() == 1:
                        if self.mode=='sleep':
                            self.mode='wake'
                            # self.oled.wake()
                        key = self.keys[row_index][col_index]
                        row.value(0)
                        await callback(key)
                        await asyncio.sleep(0.3)  # debounce
                        self.last_keypress=time.ticks_ms()      
                row.value(0)
            if time.ticks_diff(time.ticks_ms(), self.last_keypress) > 10000 and self.mode=='wake':
                self.mode='sleep'
                # self.oled.sleep()
            await asyncio.sleep_ms(10)

    async def on_keypress(self,key):
        await self.beep(200)
        print("Key pressed:", key)
        # self.update_oled(key)
    
    async def beep(self,duration_ms=100):
        self.buzzer.value(1)
        await asyncio.sleep_ms(duration_ms)
        self.buzzer.value(0)
    
    async def unlock(self):
        self.lock.value(1)
        await asyncio.sleep(3)
        self.lock.value(0)
        self.reset()
    
    def update_oled(self,text):
        if text=='A':self.reset()    
        if text=='D':self.unlock()  
        elif text=='B':
            self.oled.clear()
            if self.password=='123': 
                self.oled.text('password acepted',0,0)
                asyncio.create_task(self.unlock())
                self.oled.show()     
            else:
                self.oled.text('Error password',0,0)
                self.oled.show()
                time.sleep(3)
                self.reset()     
        else:
            self.password+=text
            self.oled.text(text, self.oled.x, 32)
            self.oled.show()
            self.oled.x+=10


async def main():
    lock_code=lock()
    while True:await asyncio.sleep(1)

asyncio.run(main())
