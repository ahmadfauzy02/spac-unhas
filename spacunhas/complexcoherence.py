import os
import numpy as np
import scipy
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import get_cmap
from matplotlib.ticker import LogLocator, FixedLocator, MultipleLocator, LogFormatter

class ComplexCoherence:
    def __init__(self, parent_path_processing, n_window, fs, smooth_constant):
        self.path_processing = parent_path_processing.path_processing
        self.path_figures = parent_path_processing.path_figures
        # self.window_no = window_no
        self.n_window = n_window.n_window
        self.fs = fs
        self.smooth_constant = smooth_constant
        self.f = []
        self.rho = []
        self.coherencies = []
        self.output_path= []
        
    def calculate_coherence(self, fname_1, fname_2, window_no):
        self.window_no = window_no
        self.fname_1 = fname_1
        self.fname_2 = fname_2
        file1 = os.path.join(self.path_processing, f"{fname_1}_window_{window_no}.txt")
        file2 = os.path.join(self.path_processing, f"{fname_2}_window_{window_no}.txt")
        print(file1, file2, window_no)                
        try:
            data1 = np.loadtxt(file1)
            data2 = np.loadtxt(file2)
            f = data1[:, 1]
            g = data2[:, 1]                
            if len(f) != len(g):
                raise ValueError(f"Data lengths are different for window {i + 1}")                
            dt = 1/self.fs
            N = len(f)
            window = signal.windows.hann(N)
            
            f_w = f * window
            g_w = g * window
            f_fft = fft(f_w) * dt
            g_fft = fft(g_w) * dt
            f_fftfreq = fftfreq(N, 1/self.fs)[:N // 2]                
            cc_fg = f_fft * np.conj(g_fft)
            cc_fg_smooth = signal.convolve(cc_fg, 
                                           np.ones(self.smooth_constant) / self.smooth_constant, 
                                           mode='same')                
            af = np.abs(f_fft) ** 2
            ag = np.abs(g_fft) ** 2
            af_smooth = signal.convolve(af, 
                                        np.ones(self.smooth_constant) / self.smooth_constant, 
                                        mode='same')
            ag_smooth = signal.convolve(ag, 
                                        np.ones(self.smooth_constant) / self.smooth_constant, 
                                        mode='same')                
            coh = cc_fg_smooth / np.sqrt(af_smooth * ag_smooth)
            ccoh = np.real(coh)                
            # self.rho.append(spac[:N // 2])
            self.f.append(f_fftfreq)
            self.coherencies.append(ccoh[:N // 2])            
        except Exception as e:
            print(f"Error processing window {i + 1}: {e}")
        np.savetxt(f'{self.path_processing}/{fname_1}-{fname_2}pair_spacfunc_window_{self.window_no}.txt', 
                   np.column_stack((self.f[0], np.real(self.coherencies[0]))), 
                    header='#Frequency (Hz) #SPAC Function #Coherence')
        self.output_path.append(f'{self.path_processing}/{fname_1}-{fname_2}pair_spacfunc_window_{self.window_no}.txt')            
        return self.f[0], self.coherencies[0]
    
    def plot_spacfunc(self , freq_limit=None):
        if not self.f or not self.coherencies:
            raise ValueError("No data available. Run calculate_spac_coefficient first.")
#        plt.figure(figsize=(6*self.n_window, 6))
        plt.plot(self.f[0], self.coherencies[0], c='black')
        plt.xlabel('Frequency (Hz)', weight='bold')
        plt.ylabel('SPAC Function', weight='bold')
        # if window_no:
        plt.title(f'SPAC Function: window {self.window_no}', weight='bold')    
        if freq_limit:
            plt.xlim(0, freq_limit)
        plt.ylim(-1.1, 1.1)
        plt.axhline(y=0, color='k', linewidth=0.5, linestyle='--')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.path_figures}/{self.fname_1}-{self.fname_2}pair_spacfunc_window_{self.window_no}.png')
        plt.show()
