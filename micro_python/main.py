import uasyncio as asyncio
import framebuf
from machine import Pin,I2C
import time

class DC_motor:
    # with H-bridge
    def __init__(self):
        self.m1f = Pin(8, Pin.OUT)
        self.m1b = Pin(9, Pin.OUT)

    def step_run(self,direction='forward'):
        if direction=='forward':self.m1f.low();self.m1b.high()
        elif direction=='backward':self.m1f.high();self.m1b.low()
        else: return
        time.sleep(0.1)
        self.m1f.low();self.m1b.low()


    def stop(self):
        self.m1f.low()
        self.m1b.low()

class lock:
    def __init__(self):
        led=Pin('LED', Pin.OUT)
        led.on()
        #set pins
        self.keypad_r=[Pin(i, Pin.OUT) for i in (0,1,2,3)]
        self.keypad_c=[Pin(i, Pin.IN, Pin.PULL_DOWN) for i in (4,5,6,7)]
        self.buzzer = Pin( 19, Pin.OUT)
        self.lock   = Pin(17, Pin.OUT)
        self.scl    = Pin(27)
        self.sda    = Pin(26)
        self.keys   = [['1', '2', '3', 'A'],['4', '5', '6', 'B'],['7', '8', '9', 'C'],['*', '0', '#', 'D']]
        self.last_keypress=time.ticks_ms()
        self.mode   ='wake'
        self.password=''
        asyncio.create_task(self.keypad_task(self.on_keypress))
        self.lockm=DC_motor()


    async def keypad_task(self,callback):
        while True:
            for row_index, row in enumerate(self.keypad_r):
                row.value(1)
                for col_index, col in enumerate(self.keypad_c):
                    if col.value() == 1:
                        if self.mode=='sleep':
                            self.mode='wake'
                        key = self.keys[row_index][col_index]
                        row.value(0)
                        await callback(key)
                        await asyncio.sleep(0.3)
                        self.last_keypress=time.ticks_ms()      
                row.value(0)
            if time.ticks_diff(time.ticks_ms(), self.last_keypress) > 10000 and self.mode=='wake':
                self.mode='sleep'
            await asyncio.sleep_ms(10)

    async def on_keypress(self,key):
        await self.beep(200)
        print(key)
        if key=='D': await self.unlock()  

    
    async def beep(self,duration_ms=100):
        self.buzzer.value(1)
        await asyncio.sleep_ms(duration_ms)
        self.buzzer.value(0)
    
    async def unlock(self):
        print('working')
        self.lockm.step_run('backward')
        await asyncio.sleep(5)
        self.lockm.step_run('forward')
    


async def main():
    lock_code=lock()
    while True:await asyncio.sleep(1)

asyncio.run(main())
