import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import get_cmap
import numpy as np

class Windowing:
    def __init__(self, parent_path_processing, parent_read_data, window_size):
        self.fname = parent_read_data.data_fnames
        self.readed_data= parent_read_data.readed_data
        self.time = []
        self.amplitude = []
        self.window_size = window_size
        self.path_processing = parent_path_processing.path_processing
        self.path_figures = parent_path_processing.path_figures
        self.x = []  
        self.y = []
        self.n_window = 0
        
    def windowing(self, selected_receiver=None):
        self.selected_receiver= selected_receiver
        data = self.readed_data[0]
        if selected_receiver is None:
            print(f"No receiver specified. Available receivers: {[i['Channel'][0] for i in data]}")
            return None
        receiver_data = None
        for i in data:
            if i['Channel'][0] == selected_receiver:  
                receiver_data = i
                break            
        if receiver_data is None:
            print(f"Receiver {selected_receiver} not found in the data.")
            return None            
        print(f"Processing receiver: {selected_receiver}")            
        n_sample = receiver_data['Npts'][0]
        n_window = n_sample / self.window_size
        self.time.append(receiver_data['Time'][0])
        self.amplitude.append(receiver_data['Amplitude'][0])                                         
        if n_window.is_integer():
            n_window = int(n_window)
            for n in range(n_window):
                start_index = n * self.window_size
                end_index = (n + 1) * self.window_size
                self.x.append(receiver_data['Time'][0][start_index:end_index])
                self.y.append(receiver_data['Amplitude'][0][start_index:end_index])
        else:
            n_window = int(np.floor(n_window)) + 1
            for n in range(n_window - 1):
                start_index = n * self.window_size
                end_index = (n + 1) * self.window_size
                self.x.append(receiver_data['Time'][0][start_index:end_index])
                self.y.append(receiver_data['Amplitude'][0][start_index:end_index])
            if len(self.x) < n_window:
                n_shift = end_index - ((n_window * self.window_size) - n_sample)
                self.x.append(receiver_data['Time'][0][int(n_shift):])
                self.y.append(receiver_data['Amplitude'][0][int(n_shift):])            
        self.n_window = n_window
        for i in range(self.n_window):
            np.savetxt(f'{self.path_processing}/{selected_receiver}_window_{i + 1}.txt', 
                       np.column_stack((self.x[i], self.y[i])), 
                       header='#Sample (s) #Amplitude')
        # print(f'window length is{len(self.x[0])*data['Npts'][0]/60}')
        print(f'Window has {len(self.x[0])*data[0]['Delta'][0]/60} minutes in length')  
        print(f'There are {self.n_window} windows')                  
        return self.n_window, self.x, self.y    

    def plot_windows(self):
        """Plot the windowed data."""
        plt.figure(figsize=(9, 3))
        cmap = plt.get_cmap('seismic')
        norm = mcolors.Normalize(vmin=1, vmax=self.n_window)    
        for i in range(self.n_window):
            plt.plot(self.x[i], self.y[i], c='black')
            plt.axvspan(self.x[i][0], self.x[i][-1], color=cmap(norm(i + 1)), alpha=0.5)
            plt.text(np.median(self.x[i]), max(np.concatenate(self.y)) + (max(np.concatenate(self.y)) * 0.2), 
                     s=(i + 1), ha='center', va='center', size=6)

        plt.xlabel('Waktu (s)', weight='bold')
        plt.ylabel('Amplitudo', weight='bold')
        plt.xlim(0, np.max(self.time))

        plt.title('Windowed Data', weight='bold', pad=15)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{self.path_figures}{self.selected_receiver}_windowed.png')

        plt.show()

