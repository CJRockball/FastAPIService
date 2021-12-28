import sqlite3
import pandas as pd
import pathlib
import util_file as util_file


def make_db():
    #Connect to db
    conn = sqlite3.connect("customer_loans.db")
    cur = conn.cursor()
    #Create a table
    cur.execute("""DROP TABLE IF EXISTS customer_data""")
    cur.execute("""DROP TABLE IF EXISTS gender_table""")
    cur.execute("""DROP TABLE IF EXISTS eduaction_table""")
    cur.execute("""DROP TABLE IF EXISTS marriage_table""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS customer_data (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name INTEGER,
                    gender INTEGER,
                    education INTEGER,
                    marriage INTEGER,
                    age INTEGER,
                    limit_bal REAL,
                    last_pay_amt REAL,
                    last_bill_amt REAL                  
                    );""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS gender_table (
                    gender_id INTEGER UNIQUE,
                    gender_name TEXT);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS education_table (
                    education_id INTEGER UNIQUE,
                    education_name TEXT);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS marriage_table (
                    marriage_id INTEGER UNIQUE,
                    marriage_name TEXT);""")

   # Write changes
    conn.commit()
    conn.close()
  
    #Make tuple for gender    
    gender_tuple = ((1, "male"), (2, "female"))
    education_tuple = ((0, "education_other"), (1, "graduate_school"), (2, "university"),
                       (3, "high_school"), (4, "education_other"), (5, "education_other"),
                       (6, "education_other"))  
    marriage_tuple = ((0, "marriage_other"), (1, "married"), (2, "single"), (3, "marriage_other"))  

    #Open database
    conn = sqlite3.connect("customer_loans.db")
    cur = conn.cursor()    
    #Inset new records
    cur.executemany("INSERT OR IGNORE INTO gender_table (gender_id,gender_name) VALUES (?,?);"""
                    ,gender_tuple)
    cur.executemany("INSERT OR IGNORE INTO education_table (education_id,education_name) VALUES (?,?);"""
                    ,education_tuple)
    cur.executemany("INSERT OR IGNORE INTO marriage_table (marriage_id,marriage_name) VALUES (?,?);"""
                    ,marriage_tuple)

    # Write change
    conn.commit()
    conn.close()    
  
  
  
    return

def populate_db(num_rows:int):
    APP_DIR = pathlib.Path(__file__).resolve().parent.parent
    DATA_FILE  = APP_DIR / "data/data.csv"
    
    #Get data
    source_data = pd.read_csv(DATA_FILE)
    #label_data = source_data[["default.payment.next.month"]]
    feature_data = source_data.loc[
        :, source_data.columns != "default.payment.next.month"]
    feature_sample = feature_data.sample(n=num_rows)
    
    del_cols = ["BILL_AMT2", "BILL_AMT3","BILL_AMT4","BILL_AMT5","BILL_AMT6", 
                "PAY_AMT2","PAY_AMT3","PAY_AMT4","PAY_AMT5","PAY_AMT6",
                "PAY_0","PAY_1","PAY_2","PAY_3","PAY_4","PAY_5","PAY_6"]
    
    feature_sample = feature_sample.drop(columns=del_cols)
    
    #Make lists for adding to tuple
    customer_name_list = feature_sample.ID.astype(int).to_list()
    limit_list = feature_sample.LIMIT_BAL.astype(int).to_list()
    gender_list = feature_sample.SEX.astype(int).to_list()
    education_list = feature_sample.EDUCATION.astype(int).to_list()
    marriage_list = feature_sample.MARRIAGE.astype(int).to_list()
    age_list = feature_sample.AGE.astype(int).to_list()
    bill_amt_list = feature_sample.BILL_AMT1.round(0).to_list()
    pay_amt_list = feature_sample.PAY_AMT1.round(0).to_list()
    
    #Make tuple and add data to db
    for i in range(len(customer_name_list)):            
        #Open database
        conn = sqlite3.connect("customer_loans.db")
        cur = conn.cursor()
        result_tuple = (customer_name_list[i], gender_list[i], education_list[i], 
                        marriage_list[i], age_list[i], limit_list[i], bill_amt_list[i], pay_amt_list[i])
        #Inset new records
        cur.execute("INSERT OR IGNORE INTO customer_data (customer_name,gender,education,marriage, age, limit_bal, last_pay_amt, last_bill_amt) VALUES (?,?,?,?,?,?,?,?);""",
                        result_tuple)
        # Write change
        conn.commit()
        conn.close()

    return


if __name__ == "__main__":  
    make_db()
    populate_db(100)



