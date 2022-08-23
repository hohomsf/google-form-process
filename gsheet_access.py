import gspread
import pandas as pd


class Sheet:
    """
    A class used to represent a Google Sheet.
    """

    def __init__(self, token, spread_name, sheet_name):
        """
        The constructor for Sheet class.

        Parameters:
            token (str): Access token to Google API services.
            spread_name (str): Name of the Spreadsheet.
            sheet_name (str): Name of the Sheet inside the Spreadsheet.
        """
        self.sheet = gspread.service_account(filename=token).open(spread_name).worksheet(sheet_name)
        self.all_values = self.sheet.get_all_records()
        self.df = pd.DataFrame(self.all_values)
        self.nrows = len(self.df) + 1

    def clear(self):
        """
        Clear the Google Sheet EXCEPT the header.
        """
        self.sheet.delete_rows(2, self.nrows)
