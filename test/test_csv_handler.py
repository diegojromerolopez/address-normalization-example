import os
from csv_handler import CsvHandler 

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def test_read_csv():
    reader = CsvHandler(f"{CURRENT_DIRECTORY}/resources/csv_handler/test.csv").read_csv()
    row = next(reader)
    assert row["country"] == "Wales"
    assert row["address"] == "61 Wellfield Road Roath Cardiff"
    row = next(reader)
    assert row["country"] == "England"
    assert row["address"] == "14 Tottenham Court Road London England"
    row = next(reader)
    assert row["country"] == "England"
    assert row["address"] == "91 Western Rd. Brighton East Sussex England"


def test_write_csv():
    output_csv_file_path = f"{CURRENT_DIRECTORY}/resources/csv_handler/write_test.csv" 

    csv_handler = CsvHandler(output_csv_file_path)
    writer = csv_handler.write_csv(["country", "address"])
    writer.writerow({"country": "Wales", "address": "61 Wellfield Road Roath Cardiff"})
    csv_handler.close()

    csv_handler = CsvHandler(output_csv_file_path)
    reader = csv_handler.read_csv()
    row = next(reader)
    assert row["country"] == "Wales"
    assert row["address"] == "61 Wellfield Road Roath Cardiff"
    csv_handler.close()

    os.remove(output_csv_file_path)