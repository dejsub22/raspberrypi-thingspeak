import sensors
import uasyncio
from machine import Pin

# Dictionary som inneholder strukturerte data for tre forskjellige sensorer
data = dict(
    bme = dict(temperature=0, humidity=0, pressure=0),
    ens = dict(tvoc=0, eco2=0, rating=''),
    aht = dict(temperature=0, humidity=0),
    )

# Representerer GPIO-pinnene på en mikrokontroller
# Kontrollerer LED-er
r_rgb = Pin(2, Pin.OUT, Pin.PULL_DOWN)
g_rgb = Pin(1, Pin.OUT, Pin.PULL_DOWN)
b_rgb = Pin(0, Pin.OUT, Pin.PULL_DOWN)

# Asynkron funksjon som styrer fargen på en RGB-LED basert på en "rating" fra en sensor
async def deki():
    while True:
        if data["ens"]["rating"] == 'excellent':
            r_rgb.value(1)
            g_rgb.value(0)
            b_rgb.value(1)
            
        elif data["ens"]["rating"] == 'good':
            r_rgb.value(0)
            g_rgb.value(0)
            b_rgb.value(1)
        elif data["ens"]["rating"] == 'fair':
            r_rgb.value(0)
            g_rgb.value(0)
            b_rgb.value(1)
        elif data["ens"]["rating"] == 'poor':
            r_rgb.value(0)
            g_rgb.value(1)
            b_rgb.value(1)
        elif data["ens"]["rating"] == 'bad':
            r_rgb.value(0)
            g_rgb.value(1)
            b_rgb.value(1)
            
        await uasyncio.sleep_ms(1000)
            
            
#loop = uasyncio.get_event_loop()
#loop.create_task(deki())
#loop.create_task(sensors.collect_sensors_data(data, False))

#loop.run_forever()


#if __name__ == '__main__':
 #   test()