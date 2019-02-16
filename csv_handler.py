import csv

class CsvHandler(object):
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_csv(self):
        """
        CSV reader
        """
        self.file = open(self.file_path, 'r')
        csv_file_reader = csv.DictReader(self.file, delimiter=';', quotechar='"')
        return csv_file_reader
    
    def write_csv(self, header: list):
        """
        CSV writer
        """
        self.file = open(self.file_path, 'w')
        csv_file_writer = csv.DictWriter(self.file, fieldnames=header, delimiter=';', quotechar='"')
        csv_file_writer.writeheader()
        return csv_file_writer

    def close(self):
        """
        Close file
        """
        self.file.close()