# train_yolo_mlflow.py

import os
from ultralytics import YOLO
import mlflow
import mlflow.ultralytics

# -----------------------------
# 1️⃣ Configuración de paths
# -----------------------------
# Ruta donde DVC descargó tu dataset
DATASET_PATH = "/home/ubuntu/Microproyecto_Cervical_Cancer_Classifier/dataset_preproc"

# Verifica que el dataset exista
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"No se encontró el dataset en {DATASET_PATH}. "
                            "Ejecuta `dvc pull dataset_preproc.dvc` primero.")

# Modelo preentrenado o base
MODEL_PATH = "yolo11l-cls.pt"

# -----------------------------
# 2️⃣ Configuración de entrenamiento
# -----------------------------
EPOCHS = 200
IMGSZ = 224
BATCH_SIZE = 64
DEVICE = 0          # GPU: 0, CPU: -1
LEARNING_RATE = 0.005
OPTIMIZER = "AdamW"

# -----------------------------
# 3️⃣ Iniciar experimento MLflow
# -----------------------------
mlflow.set_experiment("Cervical-Cancer-Classification")

with mlflow.start_run():

    # Log de parámetros
    mlflow.log_param("epochs", EPOCHS)
    mlflow.log_param("img_size", IMGSZ)
    mlflow.log_param("batch_size", BATCH_SIZE)
    mlflow.log_param("device", DEVICE)
    mlflow.log_param("learning_rate", LEARNING_RATE)
    mlflow.log_param("optimizer", OPTIMIZER)
    
    # -----------------------------
    # 4️⃣ Entrenamiento YOLO
    # -----------------------------
    model = YOLO(MODEL_PATH)
    
    model.train(
        data=DATASET_PATH,
        epochs=EPOCHS,
        imgsz=IMGSZ,
        batch=BATCH_SIZE,
        device=DEVICE,
        optimizer=OPTIMIZER,
        lr0=LEARNING_RATE,
    )
    
    # -----------------------------
    # 5️⃣ Log del modelo entrenado
    # -----------------------------
    mlflow.ultralytics.log_model(model, "yolo_model")
    
    print("✅ Entrenamiento completado y logueado en MLflow")
