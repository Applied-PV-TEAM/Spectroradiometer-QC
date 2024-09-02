# Here goes all the actual functions that returns / saves flags for each QC check


class SpectralQC:
    def __init__(self,data) -> None:
        if data:
            # ensure that the data is of the correct format (from data_preprocessing)
            # Could also make a data class that has a pandas dataframe and some metadata, and force the user to pass an instance of that class as an argument
            pass
        self.data = data
        self.flags = {}