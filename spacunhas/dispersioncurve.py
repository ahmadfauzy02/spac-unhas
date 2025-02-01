import scipy
from scipy.signal import decimate
from scipy.special import jv
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FixedLocator, MultipleLocator, LogFormatter
import numpy as np

class DispersionCurve:
    def __init__(self, spaccoefficient_processing):
        self.path_processing = spaccoefficient_processing.path_processing
        self.frequency = spaccoefficient_processing.frequency
        self.spaccoefficient = spaccoefficient_processing.spaccoefficient
        self.radius = spaccoefficient_processing.radius
        self.frequency_decimated= []
        self.spaccoefficient_decimated= []
        self.path_figures = spaccoefficient_processing.path_figures
    def decimator(self, downsampling_operator):
        freq_dec = scipy.signal.decimate(self.frequency[0], downsampling_operator)
        avspac_dec = scipy.signal.decimate(self.spaccoefficient[0], downsampling_operator)
        print(f'Number of samples reduced from {len(self.spaccoefficient[0])} to {len(avspac_dec)}')
        self.frequency_decimated.append(freq_dec)
        self.spaccoefficient_decimated.append(avspac_dec)
        return freq_dec, avspac_dec

    @staticmethod
    def res(xi, fi, r, yi):
        omega = 2 * np.pi * r
        return yi - jv(0, (omega * fi / xi))

    @staticmethod
    def model(xi, fi, r):
        omega = 2 * np.pi * r
        return jv(0, (omega * fi / xi))

    def calculate_dispcurv(self, minimum_pv, maximum_pv):
        x0 = np.sort(np.linspace(minimum_pv, maximum_pv, len(self.spaccoefficient_decimated[0])))    
        fitted_avspac = least_squares(
            self.res, x0, args=(self.frequency_decimated[0], self.radius, self.spaccoefficient_decimated[0]),
            method='trf', bounds=(minimum_pv, maximum_pv), loss='linear')    
        pv = fitted_avspac.x
        f_pv = self.frequency_decimated[0]
        bessel_fit = self.model(pv, self.frequency_decimated[0], self.radius)  
        x_bessel = 2 * np.pi * self.radius * self.frequency_decimated[0] / pv    
        plt.scatter(f_pv, pv, color='black', label='Fitted Dispersion Curve')
        plt.xlabel('Frequency (Hz)', weight='bold')
        plt.ylabel('Phase Velocity (m/s)', weight='bold')
        # plt.title('Dispersion Curve', weight='bold')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig(f'{self.path_figures}/dispcurv_radii{self.radius}.png')
        plt.show()
        plt.close()
        np.savetxt(f'{self.path_processing}/dispcurv_radii{self.radius}.txt', 
                           np.column_stack((f_pv, pv, x_bessel, bessel_fit, fitted_avspac.fun)),
                            header='#Frequency(Hz) #PhaseVelocity(m/s) #BesselOrdinat #BesselAbsis #SPACCoefficient ')
        return pv, f_pv, bessel_fit, x_bessel, fitted_avspac
