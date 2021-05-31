import time
import network
import ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('xxxx', 'xxxxx')
wifistart = time.time()
while not wlan.isconnected():
    if time.time() - wifistart > 20:
        print("Resetting due to wifi timeout")
        time.sleep(2)
        machine.reset()
def scan():
    ssidlist = wlan.scan()
    print('{0:30} {1:5} {2:5}'.format("SSID","   CH"," RSSI"))
    print("-" *47)
    for x in ssidlist:
        ssid = x[0]
        channel = x[2]
        rssi = x[3]
        print('{0:30} {1:5} {2:5}'.format(ssid,channel,rssi))


print(wlan.ifconfig())
print("Mac: " + ubinascii.hexlify(network.WLAN().config('mac'),':').decode() + "\n")
scan()

