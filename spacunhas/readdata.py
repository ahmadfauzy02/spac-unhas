import os
import obspy
import pandas
from obspy import read

class ReadData:
    def __init__(self, parent_path_data, data_fnames, data_format):
        self.path_data= parent_path_data.path_data
        self.path_processing= parent_path_data.path_processing
        self.path_figures= parent_path_data.path_figures
        self.data_format= data_format
        self.data_fnames= data_fnames
        self.readed_data=[]

    def read_data(self):
        missing_files = [
            fname for fname in self.data_fnames 
            if not os.path.isfile(os.path.join(self.path_data, fname))
        ]
        if missing_files:
            print(f"Missing data files: {', '.join(missing_files)}")
            print(f"Please ensure all required files are placed in the data folder: {self.path_data}")
        else:
            print("All required data files are present.")
            
        data = []
        for i in [f'{self.path_data}{j}' for j in self.data_fnames]:
            a = read(i, format=self.data_format)
            stats = a[0].stats   
            receiver_name=i.split('/')[-1]
            datas = pandas.DataFrame({
                    'Path': [i],
                    'Network': [stats.network],
                    'Station': [stats.station],
                    'Location': [stats.location],
                    'Channel': [receiver_name],
                    'Starttime': [stats.starttime],
                    'Endtime': [stats.endtime],
                    'Sampling_rate': [stats.sampling_rate],
                    'Delta': [stats.delta],
                    'Npts': [stats.npts],
                    'Amplitude': [a[0].data[:]],
                    'Time': [a[0].times()[:]]
            })
            data.append(datas)
            self.readed_data.append(data)
            a.plot(outfile=f'{self.path_figures}{receiver_name}.png')        
        return data
