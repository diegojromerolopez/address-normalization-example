from address_csv_merger import AddressCsvMerger
import os
import shortuuid

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = f"{CURRENT_DIRECTORY}/resources/address_csv_merger/"

def test_merge():
    file1_path = f"{RESOURCES_DIR}/merge/test_merge_file1.csv"
    file2_path = f"{RESOURCES_DIR}/merge/test_merge_file2.csv"
    
    output_path = f"{RESOURCES_DIR}/merge/output-{shortuuid.uuid()}.csv"
    merger = AddressCsvMerger(file1_path, file2_path)
    merger.merge(output_path)

    expected_output_path = f"{RESOURCES_DIR}/merge/expected_output.csv"
    with open(expected_output_path, "r") as expected_output_file:
        with open(output_path, "r") as output_file:
            assert expected_output_file.read(), output_file.read()  

    os.remove(output_path)
