
import ujson as json

class BaseEntity(object):

    def __init__(self, mqtt, component, object_id, node_id, discovery_prefix):
        self.mqtt = mqtt
        
        if node_id:
            base_topic = "{}/{}/{}/{}/".format(discovery_prefix, component, node_id, object_id)
        else:
            base_topic = "{}/{}/{}/".format(discovery_prefix, component, object_id)

        self.config_topic = base_topic + "config"
        self.state_topic = base_topic + "state"

class BinarySensor(BaseEntity):

    def __init__(self, mqtt, name, device_class, object_id, node_id=None, discovery_prefix="homeassistant"):

        super(BinarySensor, self).__init__(mqtt, "binary_sensor", object_id, node_id, discovery_prefix)

        self.config = {"name": name, "device_class": device_class}
        self.mqtt.publish(self.config_topic, bytes(json.dumps(self.config), 'utf-8'), True, 1)

    def setState(self, state):
        if state:
            self.mqtt.publish(self.state_topic, bytes("ON", 'utf-8'))
        else:
            self.mqtt.publish(self.state_topic, bytes("OFF", 'utf-8'))
            
    def on(self):
        self.setState(True)

    def off(self):
        self.setState(False)

class Sensor(BaseEntity):

    def __init__(self, mqtt, name, unit_of_measurement, object_id, node_id=None, discovery_prefix="homeassistant", value_template=None):

        super(Sensor, self).__init__(mqtt, "sensor", object_id, node_id, discovery_prefix)

        self.config = {"name": name, "unit_of_measurement": unit_of_measurement, "device_class": "sensor"}
        if value_template:
            self.config['value_template'] = value_template
        self.mqtt.publish(self.config_topic, bytes(json.dumps(self.config), 'utf-8'), True, 1)

    def setState(self, state):
        self.mqtt.publish(self.state_topic, bytes(json.dumps(state), 'utf-8'))

