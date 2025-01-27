class SPACProcessing:
    def __init__(self, path):
        self.path = path
        self.path_data = f'{os.path.join(self.path, "data")}/'
        self.path_processing = f'{os.path.join(self.path, "processing")}/'
        self.make_folder()
        
    def make_folder(self):
        for folder in [self.path_data, self.path_processing]:
            os.makedirs(folder, exist_ok=True)
        print(f"Folders are ready:\n- Data folder: {self.path_data}\n- Processing folder: {self.path_processing}")
