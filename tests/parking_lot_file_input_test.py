import sys
from os import getcwd
from unittest import TestCase
from parking_lot.services.parking_lot import ParkingLotService
from parking_lot.cli import process_file


class ParkingLotFileInputTest(TestCase):
    def setUp(self) -> None:
        self.input_file = "/tests/fixtures/file_input.txt"
        self.output_file = "/tests/fixtures/file_output.txt"
        self.stdout_file = "/var/tmp/parking_lot_output_file_test.txt"

    def test_parking_lot(self):
        original_stdout = sys.stdout
        input_path = getcwd() + self.input_file
        output_path = getcwd() + self.output_file
        with open(output_path) as fp:
            output = fp.readlines()  # Output fixture

        with open(self.stdout_file, "w") as fp:
            sys.stdout = fp  # Change the standard output to the file
            parking_lot_service = ParkingLotService()
            process_file(parking_lot_service, input_path)
            sys.stdout = original_stdout  # Reset the standard output

        with open(self.stdout_file) as fp:
            std_out = fp.readlines()
            self.assertListEqual(std_out, output)
