import pandas as pd
import joblib
import util_file as util_file
from db_util import add_sample_to_db


def get_data_line(query, DATA_FILE):
    source_data = pd.read_csv(DATA_FILE)
    label_data = source_data[["default.payment.next.month"]]
    feature_data = source_data.loc[
        :, source_data.columns != "default.payment.next.month"]
    feature_line = feature_data.iloc[query,:].to_frame()
    label_line = label_data.iloc[query,:].to_frame()
    add_sample_to_db(feature_data)
    return feature_line, label_line


def predict_fcn(query:int, AI_MODEL, PIPE_FILE, DATA_FILE):
    #Import pipeline and prediction model
    pipe = joblib.load(PIPE_FILE)
    
    feature_line, label_line = get_data_line(query, DATA_FILE)
    
    # Pre process
    feature_lineT = feature_line.T
    feature_pre_processed = util_file.pre_pipeline_process(feature_lineT,no_pay=True, bill=False)
    feature_data=feature_pre_processed.T.to_dict()
    # Transform test
    feature_pipe = pipe.transform(feature_pre_processed)
    
    pred_array = AI_MODEL.predict_proba(feature_pipe)
    return pred_array, feature_data