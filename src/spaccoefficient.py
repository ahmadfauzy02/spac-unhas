class SPACCoefficient:
    def __init__(self, coherence_processing, windowing_processing, radius):
        self.path_processing = coherence_processing.path_processing
        self.n_window= windowing_processing.n_window
        self.radius= radius
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
                plt.plot(f, rho, color='gray')
                all_freq.append(f)
                all_rho.append(rho)
        avspac = np.mean(all_rho, axis=0)
        plt.plot(all_freq[0], avspac, color='black')
        # plt.xscale('log')
        plt.xlim(0, max(all_freq[0]))
        plt.ylim(-1.1, 1.1)
        plt.ylabel('SPAC Coefficient', weight='bold')
        plt.xlabel('Frequency', weight='bold')
        plt.grid()
        plt.show()
        plt.close()
        self.frequency.append(all_freq[0])
        self.spaccoefficient.append(avspac)
        np.savetxt(f'{self.path_processing}/avspac_radii{self.radius}.txt', 
                   np.column_stack((all_freq[0], avspac)), 
                    header='#Frequency (Hz) #SPACCoefficient')            
        return all_freq[0], avspac
