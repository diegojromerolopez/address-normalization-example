from basic_merger import BasicMerger
import os


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def test_init():
    basic_merger = BasicMerger("file1_path", "file2_path", 0.99, True)
    assert "file1_path" == basic_merger.csv_file1_path
    assert "file2_path" == basic_merger.csv_file2_path
    assert .99 == basic_merger.minimum_address_matching_ratio
    assert True == basic_merger.unique_addresses


def test_address_expander():
    expected_expanded_address = ['27 old gloucester street london wc1n', '27 old gloucester street london wc 1n']
    assert expected_expanded_address == BasicMerger.address_expander("27 Old Gloucester Street, London WC1N")


def test_read_csv():
    rows = BasicMerger.read_csv("{}/resources/basic_merger/test.csv".format(CURRENT_DIRECTORY))
    assert "Wales" == rows[0]["country"]
    assert "61 Wellfield Road Roath Cardiff" == rows[0]["address"]
    assert 1 == len(rows[0]["normalized_addresses"])
    assert "England" == rows[1]["country"]
    assert "14 Tottenham Court Road London England" == rows[1]["address"]
    assert 1 == len(rows[1]["normalized_addresses"])
    assert "England" == rows[2]["country"]
    assert "91 Western Rd. Brighton East Sussex England" == rows[2]["address"]
    assert 1 == len(rows[2]["normalized_addresses"])


def test_merge_no_extra_fields():
    file1_path = "{}/resources/basic_merger/merge/test_merge_file1.csv".format(CURRENT_DIRECTORY)
    file2_path = "{}/resources/basic_merger/merge/test_merge_file2.csv".format(CURRENT_DIRECTORY)
    
    output_path = "{}/resources/basic_merger/merge/output_with_no_fields.csv".format(CURRENT_DIRECTORY)
    basic_merger = BasicMerger(file1_path, file2_path)
    basic_merger.merge(output_path, extra_csv1_fields=None, extra_csv2_fields=None)

    expected_output_path = "{}/resources/basic_merger/merge/expected_output_no_extra_fields.csv".format(CURRENT_DIRECTORY)
    with open(expected_output_path, "r") as expected_output_file:
        with open(output_path, "r") as output_file:
            assert expected_output_file.read(), output_file.read()  

    os.remove(output_path)


def test_merge_with_extra_fields():
    file1_path = "{}/resources/basic_merger/merge/test_merge_file1.csv".format(CURRENT_DIRECTORY)
    file2_path = "{}/resources/basic_merger/merge/test_merge_file2.csv".format(CURRENT_DIRECTORY)
    
    output_path = "{}/resources/basic_merger/merge/output_with_extra_fields.csv".format(CURRENT_DIRECTORY)
    basic_merger = BasicMerger(file1_path, file2_path)
    basic_merger.merge(output_path, {"address": "address1"}, {"address": "address2"})

    expected_output_path = "{}/resources/basic_merger/merge/expected_output_with_extra_fields.csv".format(CURRENT_DIRECTORY)
    with open(expected_output_path, "r") as expected_output_file:
        with open(output_path, "r") as output_file:
            assert expected_output_file.read(), output_file.read()  

    os.remove(output_path)

