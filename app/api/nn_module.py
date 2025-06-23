import logging
import sys
import re

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from app.api.pt_models import ClassedDatasetFromPandas
from app.settings import (
    MODEL_FILE_PATH,
    BINARY_COLS,
    CATEGORY_COLS,
    NUMERIC_COLS)

logger = logging.getLogger(__name__)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.jit.load(MODEL_FILE_PATH).to(device)


def rename_columns_to_snake_case(
        df: pd.DataFrame,
        inplace: bool = False) -> pd.DataFrame:
    """Переименовывает все столбцы DataFrame в стиль snake_case."""
    column_mapping = {
        col: (
            re.sub(r'[()]', '', col)
            .lower()
            .replace(' ', '_')
            .replace('-', '_')
        ) for col in df.columns
    }
    return df.rename(columns=column_mapping, inplace=inplace)


def dropna_with_control(
        df: pd.DataFrame,
        name: str | None = None) -> pd.DataFrame:
    """
    Функция для безопасного удаления строк с пропущенными значениями из
    DataFrame. Дополнительно корректирует столбец "gender", при наличии.
    """
    data = df.copy()

    data_loss = data.isna().sum().max() / len(data)
    start_size = data.shape

    data.dropna(inplace=True)
    if not (data.shape[0] == start_size[0] * (1 - data_loss)):
        raise ValueError('Потери данных превышают теоретически допустимые!')
    if not (data.shape[1] == start_size[1]):
        raise AssertionError('При исключении пропусков были потеряны колонки!')
    if name:
        logger.info(
            f'Удалено пропусков в {name}: {start_size[0] - data.shape[0]}')
        logger.info(
            f'Остаток данных: {(data.shape[0] / start_size[0] * 100):.2f}%')

    if 'gender' in data:
        unique_genders = sorted(data.gender.unique())
        expected_values = ['Female', 'Male']
        if unique_genders != expected_values:
            raise ValueError(
                'Ошибка при удалении данных из gender: найдены значения'
                f'{unique_genders}')

        data['gender'] = data['gender'].apply(
            lambda x: 0 if x == 'Female' else 1)
        new_unique_genders = sorted(data.gender.unique())
        expected_after_replacement = [0, 1]
        if new_unique_genders != expected_after_replacement:
            raise ValueError(
                'Ошибка при замене "gender": новые значения'
                f'{new_unique_genders}')

    return data


def convert_float_to_int(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Функция для преобразования значений указанных колонок из float в int."""
    nan_count = df[columns].isna().sum().sum()
    if nan_count > 0:
        raise ValueError(f'В данных присутствуют NaN ({nan_count})')

    data = df.copy()

    for col in columns:
        data[col] = data[col].astype(int)

    if data.shape != df.shape:
        raise AssertionError('Размер DataFrame изменился после преобразования')
    for col in columns:
        if not np.issubdtype(data[col].dtype, np.integer):
            raise TypeError(f'Колонка "{col}" не была преобразована в тип int')

    return data


def predict_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df_id = pd.DataFrame({'id': df.id})
    rename_columns_to_snake_case(df, inplace=True)
    df = dropna_with_control(df)
    df = convert_float_to_int(df, BINARY_COLS + CATEGORY_COLS)

    with torch.no_grad():
        data_set = ClassedDatasetFromPandas(
            df[BINARY_COLS + CATEGORY_COLS + NUMERIC_COLS])
        data_loader = DataLoader(data_set, batch_size=len(data_set))
        X_bin, X_cat, X_num = next(iter(data_loader))
        outputs = model(X_bin.to(device), X_cat.to(device), X_num.to(device))
        y_pred = torch.sigmoid(outputs).detach().cpu().numpy().ravel()

    return pd.merge(
        df_id,
        pd.DataFrame({'id': df.id, 'predict': y_pred}),
        on='id',
        how='left'
    ).fillna(0.5)


if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
