# Here goes all the actual functions that saves flags for each QC check
import pandas as pd
from pprint import pprint
from SMARTS import create_run_smarts_input_file_dni

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
        self.flags['less_than_am0'] = self.data['Integrated DNI']>=1001.2785
        self.fractions['less_than_am0'] = self.flags['less_than_am0'].mean()
        print(f"Fraction of data flagged during the less than AM0 check: {self.fractions['less_than_am0']:.3f}")

    def clearsky_broadband_check(self):  # sergiu
        dni_type_check = pd.api.types.is_float_dtype(self.data['DNI']) if 'DNI' in self.data.columns else False

        if not dni_type_check:
        # Set flags and fractions to pass the check if DNI columns are not floats
            self.flags['broadband_check'] = pd.Series([True] * len(self.data), index=self.data.index)
            self.fractions['broadband_check'] = 0.0
            print("Broadband check not usable. Data does not have measured DNI columns of float types.")
            return
        def is_within_whisker(x_val, y_val, whisker_values):
            for interval in whisker_values:
                i, i_plus_1, lower_whisker, upper_whisker = interval
                if i <= x_val < i_plus_1:
                    if (lower_whisker > y_val) | (y_val> upper_whisker):
                        return True
                    else:
                        return False
            return False

        # Quick check for 'Clear sky' values
        if 'Clear sky' not in self.data.columns:
            raise ValueError("'Clear sky' column not found in the data")
        # Quick check for 'DNI' and 'DNI integrated' values
        if 'DNI' not in self.data.columns or 'Integrated DNI' not in self.data.columns:
            raise ValueError("'DNI' or 'Integrated DNI' column not found in the data")

        # Check if 'DNI' and 'DNI integrated' are float values
        if not pd.api.types.is_float_dtype(self.data['DNI']) or not pd.api.types.is_float_dtype(self.data['Integrated DNI']):
            raise ValueError("'DNI' or 'Integrated DNI' column is not of float type")

        # Filter data for 'Clear sky' equal to 1, air mass <= 10, and AOD <= 2.5
        clear_sky_data = self.data[
            (self.data['Clear sky'] == 1) &
            (self.data['Airmass'] <= 10) &
            (self.data['AOD'] <= 2.5)
        ]

        # Calculate fraction of data with 'Clear sky' equal to 1, air mass <= 10, and AOD <= 2.5
        clear_sky_fraction = len(clear_sky_data) / len(self.data)
        print(f"Fraction of data with 'Clear sky' equal to 1, air mass <= 10, and AOD <= 2.5: {clear_sky_fraction:.3f}")

        if clear_sky_data.empty:
            print("Warning: No data points meet the criteria: 'Clear sky' equal to 1, air mass <= 10, and AOD <= 2.5")
            self.flags['broadband_check'] = pd.Series([False] * len(self.data), index=self.data.index)
            self.fractions['broadband_check'] = 0.0
            print(f"Fraction of clear sky data passing broadband check: {self.fractions['broadband_check']:.3f}")
            return

        # Load whisker values from CSV file
        whisker_values = pd.read_csv("AOD_limits_550nm.csv").values.tolist()

        # Apply the check only to clear sky data
        broadband_check = clear_sky_data.apply(
            lambda row: is_within_whisker(
                row['Airmass'] * row['AOD'],
                row['Integrated DNI'] / row['DNI'],
                whisker_values
            ),
            axis=1
        )

        # Create a Series for the entire dataset with False for non-clear sky data
        self.flags['broadband_check'] = pd.Series([False] * len(self.data), index=self.data.index)
        self.flags['broadband_check'].update(broadband_check)

        # Calculate fraction of clear sky data passing the check
        self.fractions['broadband_check'] = broadband_check.mean()
        print(f"Fraction of clear sky data flagged during the broadband check: {self.fractions['broadband_check']:.3f}")

    def smarts_check(self, smarts_data: pd.DataFrame): # sergiu
        pass
