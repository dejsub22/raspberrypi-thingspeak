# Importerer ulike biblioteker som brukes for å aktivere koden
from time import sleep
import json
from wlan import connect
import uasyncio
from nanoweb import Nanoweb
import urequests

import sensors
from html_functions import naw_write_http_header, render_template
import buttons
from thingspeak import thingspeak_publish_data
from machine import WDT, Pin

# Definer pin-forekomster for RGB-lysdioder
r_rgb = Pin(2, Pin.OUT, Pin.PULL_DOWN)
g_rgb = Pin(1, Pin.OUT, Pin.PULL_DOWN)
b_rgb = Pin(0, Pin.OUT, Pin.PULL_DOWN)

# Definer dataordbok
data = dict(
    bme=dict(temperature=0, humidity=0, pressure=0),
    ens=dict(tvoc=0, eco2=0, rating=''),
    aht=dict(temperature=0, humidity=0),
)

# Funksjon for å stille inn RGB LED-farge basert på vurdering
async def deki():
    # Dictionary kartlegger vurderinger til RGB-fargetupler
    rating_colors = {
        'excellent': (1, 0, 1),  # Grønn
        'good': (0, 0, 1),        # Gul
        'fair': (0, 0, 1),        # Gul
        'poor': (0, 1, 1),        # Rød
        'bad': (0, 1, 1)          # Rød
    }

    while True:
        rating = data["ens"]["rating"]
        if rating in rating_colors:
            # Angi RGB-verdier basert på vurdering
            r_value, g_value, b_value = rating_colors[rating]
            r_rgb.value(r_value)
            g_rgb.value(g_value)
            b_rgb.value(b_value)
        else:
            # Default til av (alle lysdioder av) hvis vurderingen ikke ble funnet
            r_rgb.value(0)
            g_rgb.value(0)
            b_rgb.value(0)

        await uasyncio.sleep_ms(1000)

# Initialiser WiFi-tilkobling
sta_if = connect()  # Kobles til trådløst nettverk

# Initialiser Nanoweb
naw = Nanoweb()

# Initialiser Pin-forekomster for knapper
inputs = dict(button_1=False)

# Definer ruter for Nanoweb
@naw.route("/")
def index(request):
    naw_write_http_header(request)
    html = render_template(
        'index.html',
        temperature_bme=str(data['bme']['temperature']),
        humidity_bme=str(data['bme']['humidity']),
        pressure=str(data['bme']['pressure']),
        tVOC=str(data['ens']['tvoc']),
        eCO2=str(data['ens']['eco2']),
        temperature_aht=str(data['aht']['temperature']),
        humidity_aht=str(data['aht']['humidity']),
    )
    await request.write(html)

@naw.route("/api/data")
def api_data(request):
    naw_write_http_header(request, content_type='application/json')
    await request.write(json.dumps(data))

# Asynkrone tasks
async def control_loop():
    while True:
        thingspeak_publish_data(data)
        await uasyncio.sleep_ms(60 * 1000)

async def wdt_loop():
    wdt = WDT(timeout=8000)
    while True:
        wdt.feed()
        await uasyncio.sleep_ms(6000)

# Oppretter og kjør asynkrone oppgaver
loop = uasyncio.get_event_loop()
loop.create_task(sensors.collect_sensors_data(data, False))
loop.create_task(buttons.wait_for_buttons(inputs))
loop.create_task(naw.run())
loop.create_task(control_loop())
loop.create_task(wdt_loop())
loop.create_task(deki())  # Legger deki() task til event loop

loop.run_forever()
