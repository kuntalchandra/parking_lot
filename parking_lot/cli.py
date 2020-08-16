import click

from parking_lot.services.parking_lot import ParkingLotService
from parking_lot.exceptions import InvalidCommandException

commands = (
    "create_parking_lot",
    "park",
    "leave",
    "status",
    "slot_numbers_for_cars_with_colour",
    "slot_number_for_registration_number",
)


@click.command()
@click.argument("input_file", type=str, required=False)
def parking_lot(input_file: str) -> None:
    parking_lot_service = ParkingLotService()
    # TODO: Do one thing
    if input_file:
        # Get the parser action
        pass
    try:
        while True:
            line = input("$ ")
            if line == "exit":
                exit(0)
            decide_action(parking_lot_service, line)
    except (KeyboardInterrupt, SystemExit):
        return
    except Exception as ex:
        print("Invalid command {}".format(ex))


def decide_action(parking_lot_service: ParkingLotService, line: str) -> None:
    line = line.split()
    command = line[0]
    if command not in commands:
        raise InvalidCommandException(command)
    params = line[1:]
    command_function = getattr(parking_lot_service, command)
    command_function(*params)


if __name__ == "__main__":
    parking_lot()
