import unittest
import filecmp
from mappings import splitwise
from csv2ofx import converter


class TestSplitwise(unittest.TestCase):
    infile_name = "Samples\splitwise.csv"
    outfile_name = "Out\splitwise"
    bank_name = "Splitwise"
    splitwise['_params']['owners_name'] = 'owner'

    def test_splitwise(self):
        c = converter.Converter()

        c.OpenFile(self.bank_name, self.infile_name)
        c.ExportFiles(self.bank_name, "QIF", self.outfile_name)

        self.assertTrue(filecmp.cmp("Samples\splitwise Splitwise USD.qif", self.outfile_name + ' Splitwise USD.qif'))
        self.assertTrue(filecmp.cmp("Samples\splitwise john.doe USD.qif", self.outfile_name + ' john.doe USD.qif'))
        self.assertTrue(filecmp.cmp("Samples\splitwise owner USD.qif", self.outfile_name + ' owner USD.qif'))


if __name__ == '__main__':
    unittest.main()
