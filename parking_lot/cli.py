import click
from os import path
from parking_lot.services.parking_lot import ParkingLotService
from parking_lot.exceptions import InvalidCommandException

commands = (
    "parking_lots",
    "create_parking_lot",
    "park",
    "leave",
    "status",
    "slot_numbers_for_cars_with_colour",
    "slot_number_for_registration_number",
    "registration_numbers_for_cars_with_colour",
)


@click.command()
@click.argument("input_file", type=str, required=False)
def parking_lot(input_file: str) -> None:
    parking_lot_service = ParkingLotService()
    if input_file:
        process_file(parking_lot_service, input_file)
    else:
        process_input(parking_lot_service)


def process_file(parking_lot_service: ParkingLotService, input_file: str) -> None:
    if not path.exists(input_file):
        raise FileNotFoundError(input_file)
    with open(input_file) as fp:
        lines = fp.readlines()
        for line in lines:
            decide_action(parking_lot_service, line)


def process_input(parking_lot_service: ParkingLotService) -> None:
    try:
        while True:
            line = input("$ ")
            if line == "exit":
                exit(0)
            decide_action(parking_lot_service, line)
    except (KeyboardInterrupt, SystemExit):
        return
    except Exception as ex:
        print("Error: {}. Couldn't process command {}".format(ex, line))


def decide_action(parking_lot_service: ParkingLotService, line: str) -> None:
    line = line.strip().split()
    command = line[0]
    if command not in commands:
        raise InvalidCommandException(command)
    params = line[1:]
    command_function = getattr(parking_lot_service, command)
    command_function(*params)


if __name__ == "__main__":
    parking_lot()
