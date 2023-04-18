from src.carBluetoothService import MockCarBluetoothProvider

def test_isCurrentlyConnected():
    mock_provider = MockCarBluetoothProvider()
    is_connected = mock_provider.isCurrentlyConnected()
    expected_value = {"connected": "true"}
    assert is_connected == expected_value