import pandas as pd

# Use dict to translate
GENDER_dict = {1: "male", 2: "female"}
GENDER_inv = {v: k for k, v in GENDER_dict.items()}
EDUCATION_dict = {
    0: "education_other",
    1: "graduate_school",
    2: "university",
    3: "high_school",
    4: "education_other",
    5: "education_other",
    6: "education_other",
}
EDUCATION_inv = {v: k for k, v in EDUCATION_dict.items()}
MARRIAGE_dict = {0: "marriage_other", 1: "married", 2: "single", 3: "marriage_other"}
MARRIAGE_inv = {v: k for k, v in MARRIAGE_dict.items()}
label_dict = {0: "yes", 1: "no"}
label_inv = {v: k for k, v in label_dict.items()}


def pre_pipeline_process(X, no_pay=True, bill=True):
    """Process columns before pipline. Remove ID, remove Pay columns, 
       combine bill amount and pay amount since they are correlated.
       Change categorical columns to str and combine small categories.

    Args:
        X ([type]): [description]
        no_pay (bool, optional): [description]. Defaults to True.
        bill (bool, optional): [description]. Defaults to True.

    Returns:
        [type]: [description]
    """
    # Remove cols ID
    X = X.drop(columns=["ID"])

    if no_pay:
        # Remove cols ID and Pay_0 to Pay_7
        cols_to_drop = ["PAY_" + str(i) for i in range(7)]
        X = X.drop(columns=cols_to_drop)
        
    if bill:
        # Use BAL_AMT = BILL_AMT - PAY_AMT
        BAL_cols = ["BAL_AMT" + str(i + 1) for i in range(6)]
        BILL_cols = ["BILL_AMT" + str(i + 1) for i in range(6)]
        PAY_cols = ["PAY_AMT" + str(i + 1) for i in range(6)]

        for i, j, k in zip(BAL_cols, BILL_cols, PAY_cols):
            X[i] = X[j] - X[k]
            X = X.drop(columns=[j, k])

    # Combine categories in categorical data
    X["EDUCATION"] = X["EDUCATION"].replace(EDUCATION_dict)
    X["MARRIAGE"] = X["MARRIAGE"].replace(MARRIAGE_dict)
    X["SEX"] = X["SEX"].replace(GENDER_dict)
    return X



