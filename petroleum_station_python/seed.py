
from stations.models import Station
from inventory.models import FuelType, Tank, Pump, Supplier
from loyalty.models import LoyaltyReward
from services.models import CarWashService

def seed_data():
    # Stations
    s1, _ = Station.objects.get_or_create(station_name="Main Station", location="Kigali, Rwanda")
    s2, _ = Station.objects.get_or_create(station_name="Airport Station", location="Kanombe, Rwanda")

    # Fuel Types
    petrol, _ = FuelType.objects.get_or_create(fuel_name="Petrol", price_per_liter=1500.00)
    diesel, _ = FuelType.objects.get_or_create(fuel_name="Diesel", price_per_liter=1450.00)
    kerosene, _ = FuelType.objects.get_or_create(fuel_name="Kerosene", price_per_liter=1200.00)

    # Tanks
    Tank.objects.get_or_create(fuel=petrol, capacity=10000.00, current_stock=5000.00)
    Tank.objects.get_or_create(fuel=diesel, capacity=10000.00, current_stock=7000.00)

    # Pumps
    Pump.objects.get_or_create(station=s1, fuel=petrol)
    Pump.objects.get_or_create(station=s1, fuel=diesel)
    Pump.objects.get_or_create(station=s2, fuel=petrol)

    # Suppliers
    Supplier.objects.get_or_create(name="TotalEnergies", contact_person="John Doe", phone="+250780000001", email="john@total.com")

    # Loyalty Rewards
    LoyaltyReward.objects.get_or_create(name="Free 5 Liters of Fuel", description="Redeem points for 5 free liters of any fuel type.", points_cost=500)
    LoyaltyReward.objects.get_or_create(name="Basic Car Wash", description="One free basic exterior car wash.", points_cost=300)

    # Car Wash Services
    CarWashService.objects.get_or_create(name="Basic External Wash", description="Standard exterior wash and dry", price=5000.00, estimated_duration_minutes=30)
    CarWashService.objects.get_or_create(name="Full Detail", description="Comprehensive exterior & interior cleaning", price=15000.00, estimated_duration_minutes=120)

    print("Data seeded successfully!")

if __name__ == "__main__":
    seed_data()
