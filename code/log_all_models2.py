import os
import mlflow
import mlflow.pyfunc
import pandas as pd
import yaml
from ultralytics import YOLO

BASE_DIR = "/home/ubuntu/mis_modelos"

class YOLOWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, model_path):
        self.model_path = model_path

    def load_context(self, context):
        self.model = YOLO(self.model_path)

    def predict(self, context, model_input):
        results = self.model(model_input)
        return results

if __name__ == "__main__":
    mlflow.set_experiment("YOLO_best_models")

    for model_dir in os.listdir(BASE_DIR):
        model_path = os.path.join(BASE_DIR, model_dir, "best.pt")
        args_path = os.path.join(BASE_DIR, model_dir, "args.yaml")
        results_path = os.path.join(BASE_DIR, model_dir, "results.csv")

        if not os.path.exists(model_path):
            continue  # saltar si no hay modelo

        # --- hiperparámetros ---
        hyperparams = {}
        if os.path.exists(args_path):
            with open(args_path, "r") as f:
                args = yaml.safe_load(f)
                hyperparams.update(args)

        metrics = {}
        if os.path.exists(results_path):
            df = pd.read_csv(results_path)
            last_row = df.iloc[-1].to_dict()  # última fila = última época

            metrics["train_loss"] = last_row.get("train/loss")
            metrics["val_loss"] = last_row.get("val/loss")
            metrics["accuracy_top1"] = last_row.get("metrics/accuracy_top1")
            metrics["accuracy_top5"] = last_row.get("metrics/accuracy_top5")
            metrics["lr_pg0"] = last_row.get("lr/pg0")
            metrics["lr_pg1"] = last_row.get("lr/pg1")
            metrics["lr_pg2"] = last_row.get("lr/pg2")

        # --- log en MLflow ---
        with mlflow.start_run(run_name=model_dir):
            if hyperparams:
                mlflow.log_params(hyperparams)

            clean_metrics = {k: v for k, v in metrics.items() if v is not None and pd.notna(v)}
            if clean_metrics:
                mlflow.log_metrics(clean_metrics)

            mlflow.pyfunc.log_model(
                artifact_path=f"model_{model_dir}",
                python_model=YOLOWrapper(model_path),
                artifacts={"best_pt": model_path}
            )

            print(f"✔ Modelo {model_dir} registrado en MLflow con métricas")

