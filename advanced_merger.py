import csv
import os
import pandas as pd
import sys
from postal.expand import expand_address


class ExpansionBasedMerger(object):

    def __init__(self, csv_file1_path, csv_file2_path):
        self.csv_file1_path = csv_file1_path
        self.csv_file2_path = csv_file2_path

    def merge(self, output_path):
        expanded_csv_file1_path = "expanded_file1.csv"
        ExpansionBasedMerger.expand_csv(self.csv_file1_path, expanded_csv_file1_path, ["id_store", "variable1"])
        
        expanded_csv_file2_path = "expanded_file2.csv"
        ExpansionBasedMerger.expand_csv(self.csv_file2_path, expanded_csv_file2_path, ["variable2"])

        file1_df = pd.read_csv(expanded_csv_file1_path, sep=";")
        file2_df = pd.read_csv(expanded_csv_file2_path, sep=";")

        merged_df = pd.merge(file1_df, file2_df, how='inner', on='normalized_address')

        output_df = merged_df#[['id_store', 'variable1','variable2']]
        output_df["ratio"] = output_df["variable1"] / output_df["variable2"]
        output_df.rename(index=str, columns={"variable1": "var1", "variable2": "var2"})

        output_df.to_csv(output_path, index=False, sep=";")

        os.remove(expanded_csv_file1_path)
        os.remove(expanded_csv_file2_path)

    @staticmethod
    def expand_csv(csv_file_path, output_csv_file_path, other_fields=None):
        other_fields = other_fields or []
        csv_file_reader = ExpansionBasedMerger.read_csv(csv_file_path)
        csv_output_file_writer = ExpansionBasedMerger.write_csv(output_csv_file_path, other_fields+["normalized_address"])
        for row in csv_file_reader:
            expanded_rows = ExpansionBasedMerger.expand_row(row, other_fields=other_fields)
            csv_output_file_writer.writerows(expanded_rows)

    @staticmethod
    def expand_row(row, other_fields):
        #print("row", row)
        expanded_addresses = set(expand_address(row["address"]))
        expanded_rows = []
        for expanded_address in expanded_addresses:
            expanded_row = {"normalized_address": expanded_address}
            for other_field in other_fields:
                expanded_row[other_field] = row[other_field]
            expanded_rows.append(expanded_row)
        return expanded_rows

    @staticmethod
    def read_csv(csv_file_path: str):
        """
        CSV reader
        """
        csv_file = open(csv_file_path, 'r')
        csv_file_reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
        return csv_file_reader
    
    @staticmethod
    def write_csv(csv_file_path: str, header: list):
        """
        CSV writer
        """
        csv_file = open(csv_file_path, 'w')
        csv_file_writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=';', quotechar='"')
        csv_file_writer.writeheader()
        return csv_file_writer


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise "Error, expected two CSV files with an address column"

    merger = ExpansionBasedMerger(sys.argv[1], sys.argv[2])
    merger.merge(sys.argv[3])
