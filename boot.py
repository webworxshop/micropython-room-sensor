# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl
import ujson
import network

def load_config():
    with open('config.json') as f:
        return ujson.loads(f.read())

def do_connect(config):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(config['essid'], config['password'])
        while not sta_if.isconnected():
            pass
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        print('Network config:', sta_if.ifconfig())

do_connect(load_config())
webrepl.start()
gc.collect()

