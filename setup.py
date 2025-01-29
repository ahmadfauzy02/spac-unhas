

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
    
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Spatial Autocorrelation Processing'
LONG_DESCRIPTION = 'Package for extract dispersion curve based on spatial autocorrelation method.'

# Setting up
setup(
    name="spacunhas",
    version=VERSION,
    author="Ahmad Fauzy",
    author_email="<ahmadfauzyarif@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['scipy', 'obspy', 'pandas', 'numpy', 'matplotlib', 'os'],
    keywords=['geophysics', 'dispersioncurve', 'spac'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Geophysicst",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
