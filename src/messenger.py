import paho.mqtt.client as mqtt
import os
import json
from src import locationService
from src import carBluetoothService

class Messenger:
    def __init__(self):
        self.connected = False

        # Create LocationService and CarBluetoothService objects
        self.locationService = locationService.MockLocationProvider()
        self.carBluetoothService = carBluetoothService.MockCarBluetoothProvider()

        # Setup MQTT connection
        self.mqttConnection = mqtt.Client()
        self.mqttConnection.on_connect = self.__onMQTTconnect
        self.mqttConnection.on_message = self.__onMQTTMessage

        # Define callback functions for specific topics
        self.mqttConnection.message_callback_add("req/location/current", self.locationCallback)
        self.mqttConnection.message_callback_add("req/car/connected", self.carBluetoothCallback)

    def connect(self):
        if not self.connected:
            try:
                docker_container = os.environ.get('DOCKER_CONTAINER', False)
                if docker_container:
                    mqtt_address = "broker"
                else:
                    mqtt_address = "localhost"
                self.mqttConnection.connect(mqtt_address,1883,60)
            except:
                return False
        self.connected = True
        return True
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.mqttConnection.disconnect()
        return True

    def __onMQTTconnect(self,client,userdata,flags, rc):
        client.subscribe([("req/location/current",0)])
        client.subscribe([("req/car/connected",0)])

    def __onMQTTMessage(self,client, userdata, msg):
        pass

    def locationCallback(self,client, userdata, msg):
        location = self.locationService.getCurrentLocation()
        self.mqttConnection.publish("location/current",json.dumps(location))

    def carBluetoothCallback(self,client, userdata, msg):
        payload = self.carBluetoothService.isCurrentlyConnected()
        self.mqttConnection.publish("car/connected",json.dumps(payload))

    def foreverLoop(self):
        self.mqttConnection.loop_forever()