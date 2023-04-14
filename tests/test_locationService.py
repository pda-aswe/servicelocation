from src.locationService import MockLocationProvider

def test_getCurrentLocation():
    mock_provider = MockLocationProvider()
    location = mock_provider.getCurrentLocation()
    expected_location = {"latitude": 40.7128, "longitude": -74.0060}
    assert location == expected_location