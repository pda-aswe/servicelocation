class MockCarBluetoothProvider:
    def isCurrentlyConnected(self):
        return {"connected": "true"}