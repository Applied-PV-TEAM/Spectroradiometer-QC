# Here goes all the actual functions that saves flags for each QC check
import pandas as pd
from pprint import pprint


class SpectralQC:
    def __init__(self,data: pd.DataFrame, column_mapping: dict) -> None:
        
        if data is not None:
            data = data.rename(columns=column_mapping)
        self.data = data
        self.flags = {}
        # dict to hold fraction of data passing each QC check
        self.fractions = {}
        self.column_mapping = column_mapping
        self.spectral_columns = [col for col in self.data.columns if col.replace('.', '', 1).isdigit()]
        self.spectral_columns_mapping = {
            col:float(col) for col in self.spectral_columns
        }
        print("QC initialized with data of shape: ", self.data.shape)
        print(self.data.info())

    def all_checks(self):
        self.greater_than_zero_check()
        self.not_a_number_check()
        self.less_than_am0_check()
        self.clearsky_broadband_check()
        #self.smarts_check('some pandas dataframe')

    def greater_than_zero_check(self): # jacob
        self.flags['greater_than_zero'] = self.data[self.spectral_columns] < 0
        self.fractions['greater_than_zero'] = self.flags['greater_than_zero'].mean().mean()
        print(f"Fraction of data passing greater than zero check: {self.fractions['greater_than_zero']:.3f}")

    def not_a_number_check(self): # jacob
        self.flags['not_a_number'] = self.data[self.spectral_columns].isna()
        self.fractions['not_a_number'] = self.flags['not_a_number'].mean().mean()
        print(f"Fraction of data passing not a number check: {self.fractions['not_a_number']:.3f}")

    def less_than_am0_check(self): # jacob
        pass

    def clearsky_broadband_check(self):  # sergiu
        def is_within_whisker(x_val, y_val, whisker_values):
            for interval in whisker_values:
                i, i_plus_1, lower_whisker, upper_whisker = interval
                if i <= x_val < i_plus_1:
                    if lower_whisker <= y_val <= upper_whisker:
                        return True
            return False

        # Load whisker values from CSV file
        whisker_values = pd.read_csv("AOD_limits_550nm.csv").values.tolist()

        # Apply the check
        self.flags['broadband_check'] = self.data.apply(
            lambda row: is_within_whisker(
                row['Airmass'] * row['AOD'],
                row['Integrated DNI'] / row['DNI broadband'],
                whisker_values
            ),
            axis=1
        )

        # Calculate fraction of data passing the check
        self.fractions['broadband_check'] = self.flags['broadband_check'].mean()
        print(f"Fraction of data passing broadband check: {self.fractions['broadband_check']:.3f}")
        pass

    def smarts_check(self, smarts_data: pd.DataFrame): # sergiu
        pass
