
from csv_address_expander import CsvAddressExpander

def test_expand_row():
    row = {"address": "61 Wellfield Rd. R. Cardiff", "country": "Wales"}
    other_fields = ["country"]
    expanded_rows = CsvAddressExpander.expand_row(row, other_fields)
    expanded_rows = sorted(expanded_rows, key=lambda row: row["normalized_address"])
    
    expected_normalized_addresses = [
        '61 wellfield road r cardiff',
        '61 wellfield road rear cardiff',
        '61 wellfield road right cardiff',
        '61 wellfield road road cardiff'
    ]
    assert 4 == len(expanded_rows)
    for index, expanded_row in enumerate(expanded_rows):
        assert expected_normalized_addresses[index] == expanded_row["normalized_address"]