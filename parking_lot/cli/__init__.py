"""
Client Application for Parking Lot
"""

import click


@click.group()
@click.argument("input_file", type=str, default=None)
@click.pass_context
def parking_lot():
    print("Init parking lot.......................")

