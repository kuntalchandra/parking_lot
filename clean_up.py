from time import sleep

# TODO: Temporary script to address stale data clean up. Need to be addressed properly with isolated test DB
from parking_lot.repositories.parking_slot import ParkingSlotRepository
from parking_lot.repositories.car import CarRepository

# Clean up stale data
car_repo = CarRepository()
parking_slot_repo = ParkingSlotRepository()
car_repo.clean_up()
parking_slot_repo.clean_up()