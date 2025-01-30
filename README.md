# spac-unhas
`spac-unhas` is python package for processing seismic data using spatial-autocorrelation (SPAC) method

## Features
This package contain:
- **`environment`**: Generates working directory for process the data
- **`readdata`**: Reads gathered seismic data files which defaultly compatible with `obspy`
- **`windowing`**: Splits the seismic data into specific number of windows
- **`complexcoherence`**: Computes the complex coherencies in frequency domain
- **`spaccoefficient`**: Calculates directional average of complex coherencies for equally distance radii
- **`dispersioncurve`**: Perform least-square fitting between SPAC coefficient and Bessel's function first kind zero order

## Installation
To install the package just simply hit the following command on your terminal:
```bash
pip install spac-unhas
```

## Example
`example` folder provide a simple example for implementing this package. `data` gained from open source InterPACIFIC project website (https://interpacific.geopsy.org/), especially in passive seismic data collected from The Mirandola site using circular array with radius 15 meters (MIR_C_15_45).


## Additional Support
Please leave your comment on discussion section if you have any thoughts, suggestion, or encounter any problem with this. I welcome for any improvement for further develoment. Feel free to discuss.
