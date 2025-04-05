from fastapi import FastAPI, File, UploadFile
import pandas as pd
import joblib
import io as BytesIO
from pyngrok import ngrok
app = FastAPI()
# Загрузка обученной модели​

model_path = "./pkl/laptop_price_model.pkl"

model = joblib.load(model_path)

@app.post("/predict/")

async def predict(file: UploadFile = File(...)):

    content = await file.read()

    df = pd.read_csv(BytesIO(content))

    predictions = model.predict(df)

    return {"predictions": predictions.tolist()}

public_url = ngrok.connect(8000)
print("API доступно по адресу:", public_url)