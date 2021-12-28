import sqlite3
import pathlib

APP_DIR = pathlib.Path(__file__).resolve().parent.parent
DB_FILE  = APP_DIR / "customer_loans.db"

def db_action(db_command, db_params="", one_line=False, db_name=DB_FILE):
    #Open db connection
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    #Run action
    cur.execute(db_command, db_params)
    if one_line:
        result = cur.fetchone()
    else:
        result = cur.fetchall()
    
    # Write change
    conn.commit()
    conn.close()
    return result


def nr_customers_in_db():
    #Check if song already in the db
    db_command = "Select count(customer_id) FROM customer_data;"
    num_customers = db_action(db_command, one_line=True)
    return  num_customers[0]    


def get_high_balance():
    db_command = """SELECT customer_name, limit_bal \
                 FROM customer_data \
                 ORDER BY limit_bal DESC \
                     LIMIT(10);"""
    high_balance = db_action(db_command=db_command, one_line=False)
    high_balance_dict = [{'Customer': i[0], 'Balance Limit':i[1]} for i in high_balance]
    return high_balance_dict


def add_sample_to_db(feature_data):
    del_cols = ["BILL_AMT2", "BILL_AMT3","BILL_AMT4","BILL_AMT5","BILL_AMT6", 
        "PAY_AMT2","PAY_AMT3","PAY_AMT4","PAY_AMT5","PAY_AMT6",
        "PAY_0","PAY_1","PAY_2","PAY_3","PAY_4","PAY_5","PAY_6"]

    feature_sample = feature_data.drop(columns=del_cols)
    
    #Make lists for adding to tuple
    customer_name_list = feature_sample.ID.astype(int).to_list()
    limit_list = feature_sample.LIMIT_BAL.astype(int).to_list()
    gender_list = feature_sample.SEX.astype(int).to_list()
    education_list = feature_sample.EDUCATION.astype(int).to_list()
    marriage_list = feature_sample.MARRIAGE.astype(int).to_list()
    age_list = feature_sample.AGE.astype(int).to_list()
    bill_amt_list = feature_sample.BILL_AMT1.round(0).to_list()
    pay_amt_list = feature_sample.PAY_AMT1.round(0).to_list()
    
    #Open database
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    result_tuple = (customer_name_list[0], gender_list[0], education_list[0], 
                    marriage_list[0], age_list[0], limit_list[0], bill_amt_list[0], pay_amt_list[0])
    #Inset new records
    cur.execute("INSERT OR IGNORE INTO customer_data (customer_name,gender,education,marriage, age, limit_bal, last_pay_amt, last_bill_amt) VALUES (?,?,?,?,?,?,?,?);""",
                    result_tuple)
    # Write change
    conn.commit()
    conn.close()
    return