from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="http")


def get_coordinates(address: str):
    location = geolocator.geocode(address)
    return location.latitude, location.longitude


print(get_coordinates('Канаш, Чувашия'))