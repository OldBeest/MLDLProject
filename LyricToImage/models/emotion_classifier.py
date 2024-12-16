import transformers
import torch
import pandas as pd
import huggingface_hub
import pickle

from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel, AutoTokenizer, BartForSequenceClassification, PreTrainedTokenizerFast, BartForConditionalGeneration
from sklearn.model_selection import train_test_split
from torch.optim import AdamW
from transformers import get_scheduler


class LyricEmotionClassifier:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = BartForSequenceClassification.from_pretrained('gogamza/kobart-base-v2', num_labels=60).to(self.device)
        
    def load_weights(self, path):
        if path is None:
            print("no saved weights")
            return
        else:
            path = path
            self.model.load_state_dict(torch.load(path))
            print(self.model)
            print("load weights complete")
            return
