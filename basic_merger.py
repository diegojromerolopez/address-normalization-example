import sys
import csv
from postal.expand import expand_address
import shortuuid
import logging
import time


class BasicMerger(object):

    def __init__(self, csv_file1_path: str, csv_file2_path: str, minimum_address_matching_ratio: float=0.50, unique_addresses: bool=True):
        """
        Initialize a basic CSV merger object.
        """

        self.csv_file1_path = csv_file1_path
        self.csv_file2_path = csv_file2_path
        self.minimum_address_matching_ratio = minimum_address_matching_ratio
        self.unique_addresses = unique_addresses
        logging.debug(f"New merger: paths: {self.csv_file1_path} and {self.csv_file2_path}. Min address matching r.: {minimum_address_matching_ratio}. Uniq. address? {unique_addresses}")

    def merge(self, output_path: str, extra_csv1_fields: dict=None, extra_csv2_fields: dict=None):
        """
        Merge two CSV files in a file with the path output_path.
        """

        logging.info(f"Starting merge {self.csv_file1_path} + {self.csv_file2_path} to {output_path}")

        start_time = time.time()
        
        extra_csv1_fields = extra_csv1_fields or {}
        extra_csv2_fields = extra_csv2_fields or {}
        
        csv1 = BasicMerger.read_csv(self.csv_file1_path)
        csv2 = BasicMerger.read_csv(self.csv_file2_path)
        
        csv3 = []
        for row1 in csv1:
            row1_has_a_match = False
            closest_score = -1
            closest_row = None
            row2_index = 0
            while row2_index < len(csv2):
                row2 = csv2[row2_index]

                # Two addresses are equal when their normalized addresses match with a matching ration equals to self.minimum_address_matching_ratio
                # Note we pass the addres set to the matcher, not the actual addresses to avoid compute the normalized addresses again and again
                addresses_match, row2_address_score = self.addresses_match(row1["normalized_addresses"], row2["normalized_addresses"])
                if closest_score < row2_address_score:
                    closest_score = row2_address_score
                    closest_row = row2
                
                row1_has_a_match = row1_has_a_match or addresses_match
                if addresses_match:
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
                    logging.debug(f"Success! {row1} was merged to {row2} in {row3}")
                    
                    # If addresses don't have more than one occurence,
                    # when the first matching is found, end matching process for this address
                    if self.unique_addresses:
                        del csv2[row2_index]
                        break
                    
                row2_index += 1
            else:
                if not row1_has_a_match:
                    logging.error(f"Error. {row1['id_store']};'{row1['address']}' couldn't be merged. Closest address is {closest_row['address']} ({closest_score})")
        
        # Output the resultant CSV file
        BasicMerger.write_output_csv(output_path, csv3, list(extra_csv1_fields.values()), list(extra_csv2_fields.values()))
        
        elapsed_time = time.time() - start_time
        csv1_address_count = len(csv1)
        merged_address_count = len(csv3)
        merged_address_percentage = 100.0 * merged_address_count / csv1_address_count
        logging.info(f"Merge of addresses {merged_address_count} of {csv1_address_count} ({merged_address_percentage} %) completed in {output_path} in {elapsed_time} seconds")

    def addresses_match(self, addresses1: set, addresses2: set) -> tuple:
        """
        Inform if the normalized address sets of two addresses are enough similar. 
        """
        same_addresses_count = len(addresses1 & addresses2)
        address_matching_ratio = same_addresses_count / len(addresses1 | addresses2)
        return (address_matching_ratio >= self.minimum_address_matching_ratio, address_matching_ratio)

    @staticmethod
    def read_csv(csv_file_path: str):
        """
        Reac CSV in memory!
        """
        rows = []
        with open(csv_file_path, 'r') as csv_file:
            csv_file_reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
            for row in csv_file_reader:
                row["normalized_addresses"] = set(BasicMerger.address_expander(row["address"]))
                rows.append(row)
        return rows

    @staticmethod
    def write_output_csv(csv_file_path: str, rows: [], extra_csv1_fields: None, extra_csv2_fields: None):
        """
        Write output CSV to disk.
        """
        extra_csv1_fields = extra_csv1_fields or []
        extra_csv2_fields = extra_csv2_fields or []
        with open(csv_file_path, 'w') as csv_file:
            csv3_fields = ["id","var1","var2","ratio"] + extra_csv1_fields + extra_csv2_fields
            csv_file_writer = csv.DictWriter(csv_file, fieldnames=csv3_fields, delimiter=';', quotechar='"')
            csv_file_writer.writeheader()
            csv_file_writer.writerows(rows)
        


    @staticmethod
    def address_expander(address: str) -> list:
        """
        Return a list of normalized address for the input address.
        """
        return expand_address(address)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise "Error, expected two CSV files with an address column"

    csv1_file_path = sys.argv[1]
    csv2_file_path = sys.argv[2]
    ouput_csv_file_path = sys.argv[3]
    debug = len(sys.argv) >= 5 and sys.argv[4] == "debug"

    # Setup a logger
    execution_uuid = shortuuid.uuid()
    logging.basicConfig(filename='basic_merger.log', format=f'%(asctime)s %(levelname)s: [{execution_uuid}] %(message)s', level=logging.INFO)
    if debug:
        logging.level = logging.DEBUG

    merger = BasicMerger(csv1_file_path, csv2_file_path)
    
    if debug:
        merger.merge(ouput_csv_file_path, {"address": "address1"}, {"address": "address2"})
    else:
        merger.merge(ouput_csv_file_path)
