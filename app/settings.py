import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FILES_DIR = os.path.join(BASE_DIR, 'app', 'static')
MODEL_FILE_PATH = os.path.join(
    STATIC_FILES_DIR, 'models', 'jit_model_230625_1141.pt')

BINARY_COLS = [
    'diabetes', 'family_history', 'obesity', 'alcohol_consumption',
    'previous_heart_problems', 'medication_use']
CATEGORY_COLS = ['diet', 'stress_level', 'physical_activity_days_per_week']
NUMERIC_COLS = [
    'age', 'cholesterol', 'heart_rate', 'exercise_hours_per_week',
    'sedentary_hours_per_day', 'bmi', 'triglycerides', 'blood_sugar', 'ck_mb',
    'troponin', 'systolic_blood_pressure', 'diastolic_blood_pressure',
    'sleep_hours_per_day']
