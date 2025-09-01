# visualization functions of quality control flags for the spectral data
# visualization of post-QC spectral and broadband measurements
from src.quality_control import SpectralQC
import matplotlib.pyplot as plt

class SpectralQCVisualization:
    def __init__(self, spectralQC: SpectralQC) -> None:
        self.spectralQC = spectralQC

    def plot_fractions(self):
        # Horizontal bar plot with check names on x axis and fractions on y axis
        check_names = list(self.spectralQC.fractions.keys())
        check_fractions = list(self.spectralQC.fractions.values())
        n_checks = len(check_names)
        n_rows = 5
        n_cols = n_checks // n_rows
        fig, ax = plt.subplots(figsize=(3*n_cols, 5), ncols=n_cols,nrows = 5)
        for i in range(n_checks):
            ax[i//n_cols, i%n_cols].barh(check_names[i], check_fractions[i])
            ax[i//n_cols, i%n_cols].set_xlabel('Fraction of data passing QC check')
            ax[i//n_cols, i%n_cols].set_ylabel('QC check')
        ax.set_title('Fraction of data passing QC checks')
        plt.show()

    def plot_flags(self):
        pass