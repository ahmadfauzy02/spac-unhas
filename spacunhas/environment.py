try:
    # Core Python modules
    import os
    import sys
    import obspy
    import numpy as np
    from obspy import read
    import pandas
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from matplotlib.cm import get_cmap
    from scipy import signal
    from scipy.fft import fft, fftfreq  # Removed duplicate fft/fftfreq import
    from matplotlib.ticker import LogLocator, FixedLocator, MultipleLocator, LogFormatter
    from scipy.signal import decimate
    from scipy.special import jv
    from scipy.optimize import least_squares
    import scipy
    
    print("All modules loaded successfully!")
    
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please install required modules using:")
    print("pip install -r requirements.txt")



class SPACProcessing():
    def __init__(self, path):
        self.path = path
        self.path_data= f'{os.path.join(self.path, 'data')}/'
        self.path_processing= f'{os.path.join(self.path, 'processing')}/'
        self.path_figures= f'{os.path.join(self.path, 'figures')}/'
        self.make_folder()
        
    def make_folder(self):
        for folder in [self.path_data, self.path_processing, self.path_figures]:
            os.makedirs(folder, exist_ok=True)
        print(f"Folders are ready:\n- Data folder: {self.path_data}\n- Processing folder: {self.path_processing}")

