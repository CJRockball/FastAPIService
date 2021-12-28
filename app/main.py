
from fastapi import FastAPI
import pathlib
from pickle import load
from predictions import predict_fcn 
from db_util import nr_customers_in_db, get_high_balance
import json
import os
import uvicorn

app = FastAPI()

APP_DIR = pathlib.Path(__file__).resolve().parent.parent
MODEL_PATH = APP_DIR / "model_artifact/xgb_best.pkl"
PIPE_FILE  = APP_DIR / "model_artifact/pipe.joblib"
DATA_FILE  = APP_DIR / "data/data.csv"

AI_MODEL = None

#Preload model
@app.on_event("startup")
def on_startup():
    global MODEL_PATH, AI_MODEL
    if MODEL_PATH.exists():
        AI_MODEL=load(open(MODEL_PATH, 'rb'))
    
#Test home page
@app.get("/")
def home():
    return "To predict type /predictions/?q=number. To get number of entries in database /total_count. To get a list of the highest balance customers /high_balance"
    
#Total number of entries in db
@app.get("/total_count")
def home():
    num_customers = nr_customers_in_db()
    return {"Total": num_customers}


#10 highest balances
@app.get("/high_balance")
def home():
    high_balance = get_high_balance()
    return list(high_balance)

#Predict API
@app.get("/predict")
def read_index(q:int):
    pred_array, feature_data = predict_fcn(int(q), AI_MODEL, PIPE_FILE, DATA_FILE)
    data = json.dumps(feature_data)
    return {"0":str(pred_array[0][0]), "1":str(pred_array[0][1]), **feature_data}

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    uvicorn.run(app, host="0.0.0.0", port=port)
