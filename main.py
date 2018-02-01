
from machine import Pin
from umqtt.robust import MQTTClient
import uasyncio as asyncio
import dht
import ubinascii
import machine
from boot import load_config
import hassnode
import time

PIR_PIN = 2
DHT_PIN = 12

motion_sensor = None
temperature_sensor = None
humidity_sensor = None

def motion_callback(p):
    value = p.value()
    print("Motion event:", value)
    motion_sensor.setState(value)

async def dht_task():
    sensor = dht.DHT22(Pin(DHT_PIN))
    while True:
        try:
            sensor.measure()
            temperature = sensor.temperature()
            humidity = sensor.humidity()

            print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))
            temperature_sensor.setState(temperature)
            humidity_sensor.setState(humidity)
        except OSError:
            print("Can't read from DHT22")

        await asyncio.sleep(30)

def main(config):
    global temperature_sensor, motion_sensor, humidity_sensor

    client_id = "esp8266_room_sensor_" + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
    print(client_id)
    mqtt = MQTTClient(client_id, config['mqtt']['broker'], port=config['mqtt']['port'],
                      user=config['mqtt']['user'], password=config['mqtt']['password'])
    mqtt.connect()
    print("Connected to {}".format(config['mqtt']['broker']))

    motion_sensor = hassnode.BinarySensor(mqtt, config['motion']['name'], "motion", config['motion']['entity_id']) 
    temperature_sensor = hassnode.Sensor(mqtt, config['temperature']['name'], "°C", config['temperature']['entity_id'])
    humidity_sensor = hassnode.Sensor(mqtt, config['humidity']['name'], "%", config['humidity']['entity_id'])

    pir = Pin(PIR_PIN, Pin.IN)
    pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=motion_callback)
    
    loop = asyncio.get_event_loop()
    loop.create_task(dht_task())
    loop.run_forever()

if __name__ == "__main__":
    config = load_config()
    main(config)

