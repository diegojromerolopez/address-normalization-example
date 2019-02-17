import csv
import logging
import os
import pandas as pd
import shortuuid
import sys
import time
from csv_handler import CsvHandler
from csv_address_expander import CsvAddressExpander
from pathlib import Path
from postal.expand import expand_address


class AddressCsvMerger(object):

    def __init__(self, csv_file1_path, csv_file2_path):
        self.csv_file1_path = csv_file1_path
        self.csv_file2_path = csv_file2_path

    def pandas_merge(self, output_path):
        """
        Do the merge by using Pandas
        """

        logging.info(f"Starting pandas merge {self.csv_file1_path} + {self.csv_file2_path} to {output_path}")

        start_time = time.time()

        expanded_csv_file1_path = "expanded_file1.csv"
        CsvAddressExpander.expand_csv(self.csv_file1_path, expanded_csv_file1_path, ["id_store", "variable1"])
        
        expanded_csv_file2_path = "expanded_file2.csv"
        CsvAddressExpander.expand_csv(self.csv_file2_path, expanded_csv_file2_path, ["variable2"])

        file1_df = pd.read_csv(expanded_csv_file1_path, sep=";")
        file1_df.set_index("normalized_address", drop=True, inplace=True)
        
        file2_df = pd.read_csv(expanded_csv_file2_path, sep=";")
        file2_df.set_index("normalized_address", drop=True, inplace=True)
        
        merged_df = pd.merge(file1_df, file2_df, how='inner', left_index=True, right_index=True)

        output_df = merged_df[['id_store', 'variable1','variable2']]
        output_df["ratio"] = output_df["variable1"] / output_df["variable2"]
        output_df.rename(index=str, columns={"variable1": "var1", "variable2": "var2"})

        output_df.drop_duplicates().to_csv(output_path, index=False, sep=";")

        os.remove(expanded_csv_file1_path)
        os.remove(expanded_csv_file2_path)

        elapsed_time = time.time() - start_time
        csv1_address_count = file1_df.shape[0]
        merged_address_count = output_df.shape[0]
        merged_address_percentage = 100.0 * merged_address_count / csv1_address_count
        logging.info(f"Merge of addresses {merged_address_count} of {csv1_address_count} ({merged_address_percentage} %) completed in {output_path} in {elapsed_time} seconds")

    def merge(self, output_path):
        """
        Do the merge the best way possible
        """

        logging.info(f"Starting merge {self.csv_file1_path} + {self.csv_file2_path} to {output_path}")

        start_time = time.time()

        # Expand the CSV file 1, i.e. duplicate rows by addint a new column called "normalized_address"
        # each new row will have all the same values in the first columns, but a different one in "normalized_address"
        expanded_csv_file1_path = "expanded_file1.csv"
        CsvAddressExpander.expand_csv(self.csv_file1_path, expanded_csv_file1_path, ["id_store", "variable1"])
        file1_df = pd.read_csv(expanded_csv_file1_path, sep=";")
        # Set an index to increase perfomance of filters
        file1_df.set_index("normalized_address", drop=True, inplace=True)
        
        # Prepare the output CSV writer
        csv_output_file_writer = CsvHandler(output_path).write_csv(['id', 'var1','var2', 'ratio'])
        csv_output_file_row_count = 0
        # Read each row of the CSV file 2 and expand their addresses, loop through their normalized addresses and
        # as soon as there is a coincidence, write the result on the output CSV file
        csv_file2_reader = CsvHandler(self.csv_file2_path).read_csv()
        for row2 in csv_file2_reader:
            normalized_addresses = expand_address(row2["address"])
            for normalized_address in normalized_addresses:
                # Exact match
                file1_normalized_address_selection = file1_df[file1_df.index == normalized_address]
                file1_normalized_address_selection_match_found = file1_normalized_address_selection.shape[0] > 0
                if file1_normalized_address_selection_match_found:
                    row1 = file1_normalized_address_selection.iloc[0]
                    output_row = {
                        "id": row1["id_store"],
                        "var1": row1["variable1"],
                        "var2": row2["variable2"],
                        "ratio": float(row1["variable1"])/float(row2["variable2"]) if float(row2["variable2"]) != 0.0 else None
                    }
                    csv_output_file_writer.writerow(output_row)
                    csv_output_file_row_count += 1
                    break
            else:
                # Exact match has not delivered any results
                # TODO: implement fuzzy matching
                logging.error(f"Error. {row2['address']}' couldn't be found on expanded address set.")
        os.remove(expanded_csv_file1_path)

        elapsed_time = time.time() - start_time
        csv1_address_count = file1_df[["id_store"]].drop_duplicates().shape[0]
        merged_address_percentage = 100.0 * csv_output_file_row_count / csv1_address_count
        logging.info(f"Merge of addresses {csv_output_file_row_count} of {csv1_address_count} ({merged_address_percentage} %) completed in {output_path} in {elapsed_time} seconds")



if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise "Error, expected two CSV files with an address column"

    csv1_file_path = sys.argv[1]
    csv2_file_path = sys.argv[2]
    ouput_csv_file_path = sys.argv[3]
    debug = len(sys.argv) >= 5 and sys.argv[4] == "debug"

    # Setup a logger
    execution_uuid = shortuuid.uuid()
    this_file_path = Path().absolute()
    logging.basicConfig(filename=f'{this_file_path}/log/address_csv_merger.log', format=f'%(asctime)s %(levelname)s: [{execution_uuid}] %(message)s', level=logging.INFO)
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    merger = AddressCsvMerger(csv1_file_path, csv2_file_path)
    
    if debug:
        merger.merge(ouput_csv_file_path)
    else:
        merger.merge(ouput_csv_file_path)