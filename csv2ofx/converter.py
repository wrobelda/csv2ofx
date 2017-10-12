__author__ = 'cromo'

from .csvutils import SimpleCSVGrid
from .xlsxutils import SimpleXLSXGrid
from .ofx import export as ofxexport
from .qif import export as qifexport
from mappings import all_mappings
import os


class Converter():
    def GetFileEncoding(self, mapping_name):
        mapping = all_mappings[mapping_name]
        try:
            return mapping['_params']['encoding']
        except:
            return None

    def OpenFile(self, mapping_name, input_file_path):
        """
            Takes a csv file and loads it's contents into the data table.
        """

        mapping = all_mappings[mapping_name]

        try:
            delimiter = mapping['_params']['delimiter']
        except:
            delimiter = ','
        try:
            skip_first = mapping['_params']['skip_first']
        except:
            skip_first = 0
        try:
            skip_last = mapping['_params']['skip_last']
        except:
            skip_last = 0
        try:
            has_header = mapping['_params']['has_header']
        except:
            has_header = True
        try:
            skip_initial_space = mapping['_params']['skip_initial_space']
        except:
            skip_initial_space = False

        if (os.path.splitext(input_file_path)[1][1:].lower() in ("csv", "txt")):
            input_file = open(input_file_path, 'r', encoding=self.GetFileEncoding(mapping_name))
            self.grid_table = SimpleCSVGrid(input_file, delimiter, skip_first=skip_first, skip_last=skip_last,
                                            has_header=has_header,
                                            skip_initial_space=skip_initial_space)
        elif (os.path.splitext(input_file_path)[1][1:].lower() in ("xlsx", "xls")):
            input_file = open(input_file_path, 'rb')
            self.grid_table = SimpleXLSXGrid(input_file, delimiter, skip_last, has_header, skip_initial_space)
        else:
            raise Exception("Unknown file type")

    def ExportFiles(self, mapping_name, output_format, output_filename):

        mapping = all_mappings[mapping_name][output_format]
        params = all_mappings[mapping_name]['_params'] if '_params' in all_mappings[mapping_name] else []

        grid = self.grid_table

        if output_format == 'OFX':
            csv2ofx_export = ofxexport
        elif output_format == 'QIF':
            csv2ofx_export = qifexport
        else:
            raise Exception("Unhandled export format: %s" % format)

        csv2ofx_export(output_filename, mapping, params, grid)
