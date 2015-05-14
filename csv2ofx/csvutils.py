from csv import reader


class SimpleCSVGrid():
    def __init__(self, csv_path, delimiter=',', skip_last=0, has_header=True):
        # delimiter, quote could come from config file perhaps
        csv_reader = reader(csv_path, delimiter=delimiter, quotechar='"')
        self.grid_contents = [row for row in csv_reader if len(row) > 0]
        if skip_last:
            self.grid_contents = self.grid_contents[:-skip_last]

        # the 1st row is the column headers
        self.grid_cols = len(self.grid_contents[0])
        self.grid_rows = len(self.grid_contents)

        self.has_header = has_header
        if self.has_header:
            # header map
            # results in a dictionary of column labels to numeric column location
            self.col_map = dict([(self.grid_contents[0][c], c) for c in range(self.grid_cols)])

    def GetNumberRows(self):
        if self.has_header:
            return self.grid_rows - 1
        else:
            return self.grid_rows

    def GetNumberCols(self):
        return self.grid_cols

    def GetRowNumber(self, row):
        if self.has_header:
            return row + 1
        else:
            return row

    def IsEmptyCell(self, row, col):
        try:
            return len(self.grid_contents[self.GetRowNumber(row)][col]) == 0
        except IndexError:
            return False

    def GetValue(self, row, col):
        try:
            return self.grid_contents[self.GetRowNumber(row)][col]
        except IndexError:
            return ""

    def GetColLabelValue(self, col):
        return self.grid_contents[0][col]

    def GetColPos(self, col_name):
        return self.col_map[col_name]


def xmlize(dat):
    """
        Xml data can't contain &,<,>
        replace with &amp; &lt; &gt;
        Get newlines while we're at it.
    """
    return dat.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\r\n', ' ').replace('\n', ' ')


def fromCSVCol(row, grid, column):
    """
        Uses the current row and the name of the column to look up the value from the csv data.
    """
    if grid.has_header:
        position = grid.GetColPos(column)
    else:
        position = column
    return xmlize(grid.GetValue(row, position))
