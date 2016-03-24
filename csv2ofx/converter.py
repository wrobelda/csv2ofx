__author__ = 'cromo'

from .csvutils import SimpleCSVGrid
from .ofx import export as ofxexport
from .qif import export as qifexport
from mappings import all_mappings


class Converter():
    def GetFileEncoding(self, mapping_name):
        mapping = all_mappings[mapping_name]
        try:
            return mapping['_params']['encoding']
        except:
            return None

    def OpenFile(self, mapping_name, csv_file):
        """
            Takes a csv file and loads it's contents into the data table.
        """

        mapping = all_mappings[mapping_name]

        try:
            delimiter = mapping['_params']['delimiter']
        except:
            delimiter = ','
        try:
            skip_last = mapping['_params']['skip_last']
        except:
            skip_last = 0
        try:
            has_header = mapping['_params']['has_header']
        except:
            has_header = True
        self.grid_table = SimpleCSVGrid(csv_file, delimiter, skip_last, has_header)


    def ExportFiles(self, mapping_name, output_format, output_file):

        mapping = all_mappings[mapping_name][output_format]

        grid = self.grid_table

        if output_format == 'OFX':
            csv2ofx_export = ofxexport
        elif output_format == 'QIF':
            csv2ofx_export = qifexport
        else:
            raise Exception("Unhandled export format: %s" % format)

        csv2ofx_export(output_file, mapping, grid)
