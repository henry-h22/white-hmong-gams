import numpy as np
from torch.utils.data import Dataset
from torch import tensor
from torch import float32
from splits import splits

class ToneContoursDataset(Dataset):
    def __init__(self, n, split: int = 0, word: bool = False):
        assert (split < 5) and (split >= 0), "Use numbers 0-4 for split numbers, there are only 5 splits (20 percent each)."
        all_ids = [i for i in range(n)]
        self.ids = list(set(all_ids) - set(splits[split]))
        self.word = word

    def __len__(self):
        return len(self.ids)
    
    def __getitem__(self, index):
        if self.word:
            x = tensor(np.load(f'v_tone_embeddings_word/{index}.npy').astype(np.float32), dtype=float32)
        else:
            x = tensor(np.load(f'v_tone_embeddings/{index}.npy').astype(np.float32), dtype=float32)
        y = tensor(np.load(f'v_context_embeddings/{index}.npy').astype(np.float32), dtype=float32)
        return x, y