import logging

from fastapi import APIRouter, HTTPException, UploadFile
import pandas as pd

from app.api.schemas import PredictData
from app.api.nn_module import predict_pipeline

api_router = APIRouter(prefix='/api', tags=['API'])
logger = logging.getLogger(__name__)


@api_router.post('/get_prediction/', summary='Получение одного предсказания')
async def get_prediction(data: PredictData):
    df = pd.DataFrame.from_dict({k: [v] for k, v in data.model_dump().items()})
    df['id'] = 0
    try:
        predict = predict_pipeline(df)
    except Exception as e:
        logger.error(f"Ошибка при выполнении предсказания: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Произошла ошибка: {str(e)}"
        )
    return {"predict": predict.iloc[0].predict * 100}


@api_router.post('/get_predictions/')
def upload_file(file: UploadFile):
    if file.content_type != 'text/csv':
        raise HTTPException(400, detail='Invalid document type')
    df = pd.read_csv(file.file)
    try:
        predict = predict_pipeline(df)
    except Exception as e:
        logger.error(f"Ошибка при выполнении предсказания: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Произошла ошибка: {str(e)}"
        )
    return predict.to_dict(orient='records')
