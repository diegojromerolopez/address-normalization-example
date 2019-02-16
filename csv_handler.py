import csv

class CsvHandler(object):
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_csv(self):
        """
        CSV reader
        """
        csv_file = open(self.file_path, 'r')
        csv_file_reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
        return csv_file_reader
    
    def write_csv(self, header: list):
        """
        CSV writer
        """
        csv_file = open(self.file_path, 'w')
        csv_file_writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=';', quotechar='"')
        csv_file_writer.writeheader()
        return csv_file_writer