import unittest
import filecmp
from csv2ofx import converter


class TestSplitwise(unittest.TestCase):
    infile_name = "Samples\PayPal.txt"
    outfile_name = "Out\PayPal"
    bank_name = "PayPal"

    def test_splitwise(self):
        c = converter.Converter()

        c.OpenFile(self.bank_name, self.infile_name)
        c.ExportFiles(self.bank_name, "QIF", self.outfile_name)

        self.assertTrue(filecmp.cmp("Samples\PayPal USD.qif", self.outfile_name + ' PayPal USD.qif'))
        self.assertTrue(filecmp.cmp("Samples\PayPal PLN.qif", self.outfile_name + ' PayPal PLN.qif'))


if __name__ == '__main__':
    unittest.main()
