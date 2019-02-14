import sys
import pandas as pd
from postal.expand import expand_address


class Merger(object):

    def __init__(self, csv_file1_path, csv_file2_path):
        self.csv_file1_path = csv_file1_path
        self.csv_file2_path = csv_file2_path

    def merge(self, output_path):
        file1_df = pd.read_csv(self.csv_file1_path, sep=";")
        file2_df = pd.read_csv(self.csv_file2_path, sep=";")

        print("file1")
        file1_df["address"].apply(self._address_normalizer)
        
        print("file2")
        file2_df["address"].apply(self._address_normalizer)

        output_df = pd.merge(file1_df, file2_df, on='address')
        output_df["ratio"] = output_df["variable1"] / output_df["variable2"] 
        output_df.to_csv(output_path, index=False)

    def _address_normalizer(self, address):
        expanded_address = expand_address(address)
        print(expanded_address[0])
        return expanded_address[0]


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise "Error, expected two CSV files with an address column"

    merger = Merger(sys.argv[1], sys.argv[2])
    merger.merge(sys.argv[3])
