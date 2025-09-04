# code/train_yolo_mlflow.py
import os
import mlflow
from ultralytics import YOLO
import dvc.api

# -------------------------
# CONFIGURACIÓN MLflow
# -------------------------
EXPERIMENT_NAME = "yolo_experiment"
mlflow.set_experiment(EXPERIMENT_NAME)

# -------------------------
# OBTENER DATOS DESDE DVC/S3
# -------------------------
# Ruta lógica dentro del repo
DATA_PATH = "dataset_preproc"

# Si quieres obtener la URL S3 directa (opcional)
# url = dvc.api.get_url(DATA_PATH)

# -------------------------
# HIPERPARÁMETROS
# -------------------------
EPOCHS = 100
BATCH_SIZE = 8
IMGSZ = 224
DEVICE = -1  # 0 = primera GPU, -1 = CPU

# -------------------------
# INICIO DEL EXPERIMENTO MLflow
# -------------------------
with mlflow.start_run():
    # Registrar hiperparámetros
    mlflow.log_param("epochs", EPOCHS)
    mlflow.log_param("batch_size", BATCH_SIZE)
    mlflow.log_param("img_size", IMGSZ)
    mlflow.log_param("device", DEVICE)

    # -------------------------
    # ENTRENAR MODELO YOLO
    # -------------------------
    model = YOLO("yolo11l-cls")  # Cambiar por tu modelo preentrenado si es necesario
    model.train(
        data=DATA_PATH,
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        imgsz=IMGSZ,
        device=DEVICE,
        workers=0
    )

    # -------------------------
    # GUARDAR MODELO ENTRENADO
    # -------------------------
    MODEL_PATH = "yolo_model.pt"
    model.save(MODEL_PATH)
    mlflow.log_artifact(MODEL_PATH)

    # -------------------------
    # EJEMPLO DE MÉTRICA
    # -------------------------
    # Aquí podrías calcular AUC u otra métrica
    example_metric = 0.85
    mlflow.log_metric("example_metric", example_metric)

print("Entrenamiento finalizado. Modelo y métricas registrados en MLflow.")
