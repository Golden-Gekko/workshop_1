import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset

from app.settings import BINARY_COLS, CATEGORY_COLS, NUMERIC_COLS


class ClassedDatasetFromPandas(Dataset):
    def __init__(self, data: pd.DataFrame):
        cols_total = len(BINARY_COLS + CATEGORY_COLS + NUMERIC_COLS)
        if cols_total != len(data.columns):
            raise ValueError('Некорректное число признаков в датасете!')

        self.data_bin = (
            data[BINARY_COLS]
            .apply(lambda row: int(''.join(str(x) for x in row), 2), axis=1)
            .values.astype(np.float32))
        self.data_cat = data[CATEGORY_COLS].values.astype(np.int32)
        self.data_num = data[NUMERIC_COLS].values.astype(np.float32)

        lengths = [len(self.data_bin), len(self.data_cat), len(self.data_num)]
        if any(length != lengths[0] for length in lengths):
            raise AssertionError('Потеря данных при создании датасета!')

    def __len__(self):
        return len(self.data_num)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.data_bin[idx]),
            torch.tensor(self.data_cat[idx]),
            torch.tensor(self.data_num[idx]),
        )


class HeartAttackRiskNN_emb(nn.Module):
    def __init__(
            self,
            inputs: int,
            bins: int = 64,
            diet_lvl: int = 3,
            stress_lvl: int = 10,
            max_days: int = 8,
            embedding_size: int = 32):
        super().__init__()

        self.bins_emb = nn.Embedding(bins, embedding_size * 4)
        self.diet_emb = nn.Embedding(diet_lvl, embedding_size)
        self.stress_emb = nn.Embedding(stress_lvl, embedding_size)
        self.act_day_emb = nn.Embedding(max_days, embedding_size)

        self.linear = nn.Sequential(
            nn.Linear(inputs + 7 * embedding_size, 128), nn.BatchNorm1d(128), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(128, 256), nn.BatchNorm1d(256), nn.Mish(), nn.Dropout(0.5),
            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.Mish(), nn.Dropout(0.5),
            nn.Linear(128, 1)
        )

    def forward(
        self,
        X_bin: torch.Tensor,
        X_cat: torch.Tensor,
        X_num: torch.Tensor
    ) -> torch.Tensor:
        bins = self.bins_emb(X_bin.int())
        for i, cat in enumerate(CATEGORY_COLS):
            if cat == 'diet':
                diet = self.diet_emb(X_cat[:, i].int())
            elif cat == 'stress_level':
                stress = self.stress_emb(X_cat[:, i].int())
            elif cat == 'physical_activity_days_per_week':
                act_day = self.act_day_emb(X_cat[:, i].int())
        try:
            features = torch.cat((bins, diet, stress, act_day, X_num), dim=1)
        except RuntimeError:
            print('size bins - ', bins.size())
            print('size diet - ', diet.size())
            print('size stress - ', stress.size())
            print('size act_day - ', act_day.size())
            print('size X_num - ', X_num.size())
        output = self.linear(features)

        return output
