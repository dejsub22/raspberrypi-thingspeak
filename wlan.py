# Importerer nettverk funskjon slik at Raspberry Pi-en kan kobles på nett
import network
import time

SSID = 'DATO IOT'
PASSWORD = 'Admin:123'

# Koden for å få den trådløse koblinga på
def connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        c = 0
        while sta_if.isconnected() == False:
            c += 1
            time.sleep(0.2)
            if c > 50:
                print('Connection failed')
                break
        if c <= 50:
            print('Connection successful')
    else:
        print('Already connected!')
    print(sta_if.ifconfig())
    return sta_if

if __name__ == '__main__':
    sta_if = connect()
    nets = sta_if.scan()
    for n in nets:
        print(n)