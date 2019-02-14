import sys
import csv
from postal.expand import expand_address


class BasicMerger(object):

    def __init__(self, csv_file1_path, csv_file2_path):
        self.csv_file1_path = csv_file1_path
        self.csv_file2_path = csv_file2_path

    def merge(self, output_path, extra_csv1_fields=None, extra_csv2_fields=None):
        extra_csv1_fields = extra_csv1_fields or {}
        extra_csv2_fields = extra_csv2_fields or {}
        
        csv1 = BasicMerger.read_csv(self.csv_file1_path)
        csv2 = BasicMerger.read_csv(self.csv_file2_path)
        
        csv3 = []
        for row1 in csv1:
            for row2 in csv2:
                are_the_same_address = len(row1["addresses"] & row2["addresses"])
                if are_the_same_address > 0:
                    # If variable 2 is zero, ratio should be infinity, so it it set to null 
                    ratio = None
                    if float(row2["variable2"]) != 0:
                        ratio = float(row1["variable1"]) / float(row2["variable2"])
                    
                    row3 = {"id": row1["id_store"], "var1": row1["variable1"], "var2": row2["variable2"], "ratio": ratio}
                    
                    # Extra fields for csv1
                    for csv1_field, output_field in extra_csv1_fields.items():
                        row3[output_field] = row1[csv1_field]
                    # Extra fields for csv2
                    for csv2_field, output_field in extra_csv2_fields.items():
                        row3[output_field] = row2[csv2_field]
                    
                    csv3.append(row3)
        
        # Output the file
        with open(output_path, 'w') as output_file:
            csv3_fields = ["id","var1","var2","ratio"] + list(extra_csv1_fields.values()) + list(extra_csv2_fields.values())
            csv_file_writer = csv.DictWriter(output_file, fieldnames=csv3_fields, delimiter=';', quotechar='"')
            csv_file_writer.writeheader()
            csv_file_writer.writerows(csv3)

    @staticmethod
    def read_csv(csv_file_path):
        rows = []
        with open(csv_file_path, 'r') as csv_file:
            csv_file_reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
            for row in csv_file_reader:
                row["addresses"] = set(BasicMerger.address_expander(row["address"]))
                rows.append(row)
        return rows

    @staticmethod
    def address_expander(address):
        return expand_address(address)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise "Error, expected two CSV files with an address column"

    csv1_file_path = sys.argv[1]
    csv2_file_path = sys.argv[2]
    ouput_csv_file_path = sys.argv[3]
    debug = len(sys.argv) >= 5 and  sys.argv[4] == "debug"

    merger = BasicMerger(csv1_file_path, csv2_file_path)
    if debug:
        merger.merge(ouput_csv_file_path, {"address": "address1"}, {"address": "address2"})
    else:
        merger.merge(ouput_csv_file_path)
