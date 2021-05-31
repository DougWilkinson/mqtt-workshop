import machine
import time
from machine import Pin
import network

try:
    pin = machine.Pin(2, machine.Pin.OUT)
    for i in range(5):
        pin.value(0)
        time.sleep_ms(500)
        pin.value(1)
        time.sleep_ms(500)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('xxxxx', 'xxxxxx')
    wifistart = time.time()
    while not wlan.isconnected():
        pin.value(0)
        time.sleep_ms(250)
        pin.value(1)
        time.sleep_ms(250)
        if time.time() - wifistart > 20:
            print("Resetting due to wifi timeout")
            time.sleep(2)
            machine.reset()
    #wlan.ifconfig(('192.168.x.xx', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
    print(wlan.ifconfig())
    import node
    node.main()
except KeyboardInterrupt:
    pin.value(1)
    print("Control-C detected")
except Exception as e:
    pin.value(1)
    print("node.py import error, trying node1.py ...")
    print(e)
    try:
        import node1
        node1.main()
    except Exception as e:
        print(e)
        print("Unrecoverable error ... Resetting in 30 seconds ")
        time.sleep(30)
        print("machine.reset()")

