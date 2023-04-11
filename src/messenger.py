import paho.mqtt.client as mqtt
import os
import json
import locationService
import carBluetoothService

class Messenger:
    def __init__(self):
        self.connected = False

        #StockService-Object erstellen
        self.locationService = locationService.MockLocationProvider()
        self.carBluetoothService = carBluetoothService.MockCarBluetoothProvider()

        #aufbau der MQTT-Verbindung
        self.mqttConnection = mqtt.Client()
        self.mqttConnection.on_connect = self.__onMQTTconnect
        self.mqttConnection.on_message = self.__onMQTTMessage

        #Definition einer Callback-Funktion für ein spezielles Topic
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
        self.mqttConnection.publish("location/current",json.dumps(self.locationService.getCurrentLocation()))

    def carBluetoothCallback(self,client, userdata, msg):
        self.mqttConnection.publish("req/car/connected",json.dumps(self.carBluetoothService.isCurrentlyConnected()))

    def foreverLoop(self):
        self.mqttConnection.loop_forever()