from csv_handler import CsvHandler
from postal.expand import expand_address


class CsvAddressExpander(object):
    @staticmethod
    def expand_csv(csv_file_path, output_csv_file_path, other_fields=None):
        """
        Expand a CSV file
        """
        other_fields = other_fields or []
        csv_file_reader = CsvHandler(csv_file_path).read_csv()
        csv_handler = CsvHandler(output_csv_file_path)
        output_fields = other_fields+["normalized_address"]
        csv_output_file_writer = csv_handler.write_csv(output_fields)
        for row in csv_file_reader:
            expanded_rows = CsvAddressExpander.expand_row(
                row, other_fields=other_fields
            )
            csv_output_file_writer.writerows(expanded_rows)

    @staticmethod
    def expand_row(row, other_fields):
        """
        Expand a row
        """
        expanded_addresses = expand_address(row["address"])
        expanded_rows = []
        for expanded_address in expanded_addresses:
            expanded_row = {"normalized_address": expanded_address}
            for other_field in other_fields:
                expanded_row[other_field] = row[other_field]
            expanded_rows.append(expanded_row)
        return expanded_rows
