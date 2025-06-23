from pydantic import BaseModel, Field, ConfigDict


class BaseModelConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PredictData(BaseModelConfig):
    diabetes: bool = Field(..., description='Наличие диабета')
    family_history: bool = Field(..., description='Заболевания в семье')
    obesity: bool = Field(..., description='У пациента ожирение')
    alcohol_consumption: bool = Field(..., description='Пациент пьющий')
    previous_heart_problems: bool = Field(
        ..., description='Проблемы с сердцем ранее')
    medication_use: bool = Field(..., description='Принимает припараты')

    diet: int = Field(..., ge=0, le=2, description='Тип диеты')
    stress_level: int = Field(..., ge=1, le=10, description='Уровень стресса')
    physical_activity_days_per_week: int = Field(
        ..., ge=0, le=7, description='Физическая активность в неделю')

    age: float = Field(..., ge=0, le=1, description='Возраст пациента')
    cholesterol: float = Field(
        ..., ge=0, le=1, description='Уровень холестерина')
    heart_rate: float = Field(
        ..., ge=0, le=1, description='Пульс')
    exercise_hours_per_week: float = Field(
        ..., ge=0, le=1,
        description='Количество часов физических упражнений в неделю')
    sedentary_hours_per_day: float = Field(
        ..., ge=0, le=1,
        description='Количество часов сидячего Образа жизни в день')
    bmi: float = Field(..., ge=0, le=1, description='Индекс массы тела (ИМТ)')
    triglycerides: float = Field(
        ..., ge=0, le=1, description='Уровень триглицеридов')
    sleep_hours_per_day: float = Field(
        ..., ge=0, le=1, description='Количество часов сна в день')
    blood_sugar: float = Field(
        ..., ge=0, le=1, description='Уровень сахара в крови')
    ck_mb: float = Field(
        ..., ge=0, le=1, description='Уровень фермента креатинкиназы')
    troponin: float = Field(
        ..., ge=0, le=1, description='Уровень тропонина')
    systolic_blood_pressure: float = Field(
        ..., ge=0, le=1, description='Систолическое артериальное давление')
    diastolic_blood_pressure: float = Field(
        ..., ge=0, le=1, description='Диастолическое артериальное давление')
