"""
prediction.py
--------------
Script sederhana untuk memprediksi status Attrition karyawan menggunakan
model Random Forest yang telah dilatih pada notebook.ipynb.

Cara penggunaan:
    python prediction.py --input data_karyawan_baru.csv --output hasil_prediksi.csv

Input CSV harus memiliki kolom yang sama seperti employee_data.csv
(kecuali kolom Attrition, EmployeeId opsional, dan kolom konstan
EmployeeCount/Over18/StandardHours boleh ada atau tidak ada).
"""

import argparse
import os
import pandas as pd
import joblib

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

DROP_COLS = ["EmployeeId", "EmployeeCount", "Over18", "StandardHours", "Attrition"]


def load_artifacts(model_dir: str = MODEL_DIR):
    model = joblib.load(os.path.join(model_dir, "rf_attrition_model.joblib"))
    encoders = joblib.load(os.path.join(model_dir, "encoders.joblib"))
    feature_columns = joblib.load(os.path.join(model_dir, "feature_columns.joblib"))
    return model, encoders, feature_columns


def preprocess(df: pd.DataFrame, encoders: dict, feature_columns: list) -> pd.DataFrame:
    data = df.copy()
    existing_drop = [c for c in DROP_COLS if c in data.columns]
    data = data.drop(columns=existing_drop)

    for col, le in encoders.items():
        if col in data.columns:
            # Nilai kategori baru yang tidak dikenali model akan ditandai -1
            data[col] = data[col].astype(str).map(
                lambda v: le.transform([v])[0] if v in le.classes_ else -1
            )

    missing = [c for c in feature_columns if c not in data.columns]
    if missing:
        raise ValueError(f"Kolom input berikut tidak ditemukan: {missing}")

    return data[feature_columns]


def predict(input_csv: str, output_csv: str, model_dir: str = MODEL_DIR):
    model, encoders, feature_columns = load_artifacts(model_dir)

    raw = pd.read_csv(input_csv)
    X = preprocess(raw, encoders, feature_columns)

    pred = model.predict(X)
    proba = model.predict_proba(X)[:, 1]

    result = raw.copy()
    result["Predicted_Attrition"] = pred
    result["Predicted_Attrition_Label"] = pd.Series(pred).map({0: "Bertahan", 1: "Resign"})
    result["Attrition_Risk_Probability"] = proba.round(3)
    result = result.sort_values("Attrition_Risk_Probability", ascending=False)

    result.to_csv(output_csv, index=False)
    print(f"Selesai. {len(result)} baris diprediksi -> disimpan ke '{output_csv}'.")
    print(f"Jumlah diprediksi Resign: {(pred == 1).sum()} dari {len(pred)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prediksi Attrition karyawan Jaya Jaya Maju")
    parser.add_argument("--input", required=True, help="Path ke CSV data karyawan baru")
    parser.add_argument("--output", default="hasil_prediksi.csv", help="Path CSV hasil prediksi")
    parser.add_argument("--model-dir", default=MODEL_DIR, help="Folder berisi artefak model")
    args = parser.parse_args()

    predict(args.input, args.output, args.model_dir)
