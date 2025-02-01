import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import get_cmap
from matplotlib.ticker import LogLocator, FixedLocator, MultipleLocator, LogFormatter

class SPACCoefficient:
    def __init__(self, coherence_processing, windowing_processing, radius):
        self.path_processing = coherence_processing.path_processing
        self.path_figures = coherence_processing.path_figures
        self.n_window= windowing_processing.n_window
        self.radius= radius
        self.all_frequency=[]
        self.all_rho= []
        self.frequency= []
        self.spaccoefficient= []
        
    def list_coherence_file(self):
        coh_files = []
        pairs= []
        pair_windows = {}            
        for file in os.listdir(self.path_processing):
            for i in range(1, self.n_window + 1):
                if file.endswith(f'pair_spacfunc_window_{i}.txt'):
                    coh_files.append(file)    
        for lis in coh_files:
            pair = lis.split('pair')[0]
            windows = lis.split('window')[-1].replace('_', '').replace('.txt', '')                
            if pair in pair_windows:
                pair_windows[pair].append(windows)
            else:
                pair_windows[pair] = [windows]
            if pair not in pairs:
                pairs.append(pair)            
        for pair, windows in pair_windows.items():
            print(f'Pair {pair} has windows {sorted([int(window) for window in windows])}')            
        return coh_files, pair_windows, pairs
    def avspac(self, list_coherence_file, selected_windows_pair):
        all_rho= []
        all_freq= []
        def closest(list, K):  
            return list[min(range(len(list)), key = lambda i: abs(list[i]-K))]
        for pair, sel_win in selected_windows_pair.items():
            for wins in sel_win:
                # print(f'{self.path_processing}{pair}pair_spacfunc_window_{wins}.txt')
                f= np.loadtxt(f'{self.path_processing}{pair}pair_spacfunc_window_{wins}.txt')[:, 0]
                rho= np.loadtxt(f'{self.path_processing}{pair}pair_spacfunc_window_{wins}.txt')[:,1]
#                plt.plot(f, rho, color='gray')
                all_freq.append(f)
                all_rho.append(rho)
        avspac = np.mean(all_rho, axis=0)
        self.frequency.append(all_freq[0])
        self.spaccoefficient.append(avspac)
        self.all_frequency.append(all_freq)
        self.all_rho.append(all_rho)
        np.savetxt(f'{self.path_processing}/avspac_radii{self.radius}.txt', 
                   np.column_stack((all_freq[0], avspac)), 
                    header='#Frequency (Hz) #SPACCoefficient')
        return all_freq[0], avspac
    def plot_avspac(self, max_frequency_to_plot=None):
        if max_frequency_to_plot:
            plt.plot(self.all_frequency[0], self.all_rho[0], color='gray')
            plt.plot(self.frequency[0], self.spaccoefficient[0], color='black')
            
            # plt.xscale('log')
            plt.xlim(0, max_frequency_to_plot)
            plt.ylim(-1.1, 1.1)
            plt.ylabel('SPAC Coefficient', weight='bold')
            plt.xlabel('Frequency', weight='bold')
            plt.grid()
            plt.tight_layout()
            plt.savefig(f'{self.path_figures}/avspac_radii{self.radius}.png')
            plt.show()
            plt.close()
        else:
            plt.plot(self.all_frequency[0], self.all_rho[0], color='gray')
            plt.plot(self.frequency[0], self.spaccoefficient[0], color='black')
            # plt.xscale('log')
            plt.xlim(0, max(self.frequency[0]))
            plt.ylim(-1.1, 1.1)
            plt.ylabel('SPAC Coefficient', weight='bold')
            plt.xlabel('Frequency', weight='bold')
            plt.grid()
            plt.tight_layout()
            plt.savefig(f'{self.path_figures}/avspac_radii{self.radius}.png')
            plt.show()
            plt.close()

            

