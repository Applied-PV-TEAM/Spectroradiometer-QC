# Here goes all the actual functions that returns / saves flags for each QC check
import pandas as pd


class SpectralQC:
    def __init__(self,data: pd.DataFrame) -> None:
        if data:
            # ensure that the data is of the correct format (from data_preprocessing)
            # Could also make a data class that has a pandas dataframe and some metadata, and force the user to pass an instance of that class as an argument
            pass
        self.data = data
        self.flags = {}

    def gt_zero_check(self): # jacob
        self.flags['gt_zero'] = self.data > 0
        pass

    def nan_check(self): # jacob
        self.flags['nan'] = self.data.isna()
        pass

    def lt_am0_check(self): # jacob
        pass

    def clearsky_broadband_check(self): # sergiu
        pass

    def smarts_check(self, smarts_data: pd.DataFrame): # sergiu
        pass