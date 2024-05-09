import requests
from math import radians, cos, sin, sqrt, atan2


class Vehicle:
    def __init__(self, id=None, name=None, model=None, year=None, color=None, price=None, latitude=None,
                 longitude=None):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'<Vehicle {self.name} {self.model} {self.year} {self.price}>'


class VehicleManager:
    def __init__(self, url):
        self.url = url

    def get_vehicles(self):
        response = requests.get(f'{self.url}/vehicles')
        vehicles = response.json()
        return [Vehicle(**vehicle) for vehicle in vehicles]

    def filter_vehicles(self, params):
        vehicles = self.get_vehicles()
        for key, value in params.items():
            vehicles = [vehicle for vehicle in vehicles if getattr(vehicle, key) == value]
        return vehicles

    def get_vehicle(self, vehicle_id):
        response = requests.get(f'{self.url}/vehicles/{vehicle_id}')
        vehicle_data = response.json()
        return Vehicle(**vehicle_data)

    def add_vehicle(self, vehicle):
        response = requests.post(f'{self.url}/vehicles', json=vehicle.__dict__)
        return Vehicle(**response.json())

    def update_vehicle(self, vehicle):
        response = requests.put(f'{self.url}/vehicles/{vehicle.id}', json=vehicle.__dict__)
        return Vehicle(**response.json())

    def delete_vehicle(self, id):
        requests.delete(f'{self.url}/vehicles/{id}')

    def get_distance(self, id1, id2):
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)
        return self.calculate_distance(vehicle1.latitude, vehicle1.longitude, vehicle2.latitude, vehicle2.longitude)

    def get_nearest_vehicle(self, id):
        base_vehicle = self.get_vehicle(id)
        all_vehicles = self.get_vehicles()
        closest_vehicle = None
        min_distance = float('inf')
        for vehicle in all_vehicles:
            if vehicle.id != id:
                distance = self.calculate_distance(base_vehicle.latitude, base_vehicle.longitude, vehicle.latitude,
                                                   vehicle.longitude)
                if distance < min_distance:
                    min_distance = distance
                    closest_vehicle = vehicle
        return closest_vehicle

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        R = 6373000
        distance = R * c
        return distance


manager = VehicleManager(url="https://test.tspb.su/test-task")
print(manager.get_vehicles())

print(manager.filter_vehicles(params={"name": "Toyota"}))

print(manager.get_vehicle(vehicle_id=1))

print(manager.add_vehicle(
    vehicle=Vehicle(
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
))

print(manager.delete_vehicle(id=1))
print(manager.get_distance(id1=1, id2=2))

print(manager.get_nearest_vehicle(id=1))