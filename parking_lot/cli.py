import click


@click.command()
@click.argument("input_file", type=str, required=False)
def parking_lot(input_file: str) -> None:
    # Get commands
    print("Init", input_file)
    pass


@click.command(name="create_parking_lot")
@click.argument("slots", type=int)
def create_parking_lot(slots: int) -> None:
    print("Created a parking lot with f{slots} slots")


@click.command(name="park")
@click.argument("registration_number", type=str)
@click.argument("color", type=str)
def park(registration_number: str, color: str) -> None:
    print("Allocated slot number: f{slot}")


@click.command(name="leave")
@click.argument("slot", type=int)
def leave(slot: int) -> None:
    print("Slot number f{slot} is free")


@click.command(name="status")
def status() -> None:
    print("Slot No. Registration No Colour")


if __name__ == "__main__":
    parking_lot()
