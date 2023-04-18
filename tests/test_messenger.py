import sys
import os
import json
from src import messenger
from unittest import mock
from unittest.mock import MagicMock, patch, call, ANY

def test_connect():
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.connect()
        mock_connect.connect.assert_called_with(ANY, 1883, 60)

def test_disconnect():
    obj = messenger.Messenger()

    with patch.object(obj, 'connected', True), patch.object(obj, 'mqttConnection') as mock_connect:
        obj.disconnect()
        mock_connect.disconnect.assert_called()

def test_foreverLoop():
    obj = messenger.Messenger()
    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.foreverLoop()
        mock_connect.loop_forever.assert_called()

def test_onMQTTconnect():
    obj = messenger.Messenger()
    mock_client = MagicMock()
    obj._Messenger__onMQTTconnect(mock_client, None, None, None)
    mock_client.subscribe.assert_called()
    calls = list(mock_client.subscribe.call_args_list)
    expected_calls = [call([("req/location/current", 0)]), call([("req/car/connected", 0)])]
    assert calls == expected_calls

def test_onMQTTMessage():
    obj = messenger.Messenger()
    obj._Messenger__onMQTTMessage(MagicMock(),None,None)

@patch("locationService.MockLocationProvider")
def test_locationCallback(mock_location):
    obj = messenger.Messenger()

    responseData = MagicMock()
    responseData.payload = json.dumps({"latitude": 40.7128, "longitude": -74.0060})

    with patch.object(obj, 'mqttConnection') as mock_connect:
        mock_location().getCurrentLocation.return_value = {"latitude": 40.7128, "longitude": -74.0060}
        obj.locationCallback(None, None, responseData)
        mock_connect.publish.assert_called_with("location/current", json.dumps({"latitude": 40.7128, "longitude": -74.0060}))

@patch("carBluetoothService.MockCarBluetoothProvider")
def test_carBluetoothCallback(mock_car_bluetooth):
    obj = messenger.Messenger()

    responseData = MagicMock()
    responseData.payload = json.dumps({"connected": "true"})

    with patch.object(obj, 'mqttConnection') as mock_connect:
        mock_car_bluetooth.return_value.isCurrentlyConnected.return_value = {"connected": "true"}
        obj.carBluetoothCallback(None, None, responseData)
        mock_connect.publish.assert_called_with("car/connected", '{"connected": "true"}')