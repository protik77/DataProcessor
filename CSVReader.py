from os import path
import csv


class CSVReader:

    def __init__(self, csv_filename='data.csv', data_dir='.'):

        self.csv_filename = csv_filename
        self.data_dir = data_dir
        self.set_csv_path()

    def set_csv_path(self):
        ''' Sets the path of the csv

        :return: full path of the csv file
        '''

        self.CSV_full_path = path.join(self.data_dir, self.csv_filename)

    def get_properties_from_csv(self):
        ''' Reads csv file and creates a list of properties.

        If there is a header, this function gets rid of that.

        :return: a list of the properties. Each element is a tuple of property of each material.
        '''

        with open(self.CSV_full_path, newline='') as csvfile:

            sample = csvfile.read(1024)

            properties_list = []

            dialect = csv.Sniffer().sniff(sample)

            # check if the csv file has header
            has_header = csv.Sniffer().has_header(sample)

            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)

            # if the csv file has header, skip the header
            if has_header:
                next(reader, None)

            for line in reader:

                self.this_list = []

                self.this_list.append(line[0])

                if line[1] == 'Band gap':
                    self.this_list.append(float(line[2]))
                else:
                    self.this_list.append(None)

                if line[3] == 'Color':
                    self.this_list.append(line[4])
                else:
                    self.this_list.append(None)

                properties_list.append(tuple(self.this_list))

        return properties_list
