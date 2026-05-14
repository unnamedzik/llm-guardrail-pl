from torch.utils.data import Dataset

class GuardRailDataset(Dataset):
    def __init__(self, dataframe):
        self.df = dataframe

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        x = self.df.iloc[idx]['prompt']
        
        y = {
            'category': self.df.iloc[idx]['category'],
            'status': self.df.iloc[idx]['status']
        }
        return x, y