from datetime import date
import pandas as pd
import pickle

from typing import List

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, validator


from model.model_preprocessing import *
class Account(BaseModel):
    update_date: date
    balance: float


class Transaction(BaseModel):
    amount: float
    date: date


class RequestPredict(BaseModel):
    account: Account
    transactions: List[Transaction]

    @validator("transactions")
    def validate_transaction_history(cls, v, *, values):
        # validate that 
        # - the transaction list passed has at least 6 months history
        # - no transaction is posterior to the account's update date
        if len(v) < 1:
            raise ValueError("Must have at least one transaction")

        update_t = values["account"].update_date

        oldest_t = v[0].date
        newest_t = v[0].date
        for t in v[1:]:
            if t.date < oldest_t:
                oldest_t = t.date
            if t.date > newest_t:
                newest_t = t.date

        assert (
            update_t - newest_t
        ).days >= 0, "Update Date Inconsistent With Transaction Dates"
        assert (update_t - oldest_t).days > 183, "Not Enough Transaction History"

        return v


class ResponsePredict(BaseModel):
    predicted_amount: float


# preprocessed data as returned from API
class modelData(BaseModel):
    month: float
    ingoing: float
    average_transactions_per_month: float
    age: float
    initial_balance: float
    ingoing_1: float
    ingoing_2: float
    ingoing_3: float
    ingoing_5: float
    ingoing_6: float




def predict(
    transactions: List[Transaction], account: Account
) -> float:
    raise NotImplementedError()

app = FastAPI()
pickle_in = open("lightgbm.pkl","rb")
gbm = pickle.load(pickle_in)
# Routes
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/preprocess/")
def preprocess_data(data: RequestPredict):
    account = data['account']
    transactions = data['transactions']
    #print(type(account))
    #df_account = pd.DataFrame([t.__dict__ for t in account ])
    df_transactions = pd.DataFrame(map(dict, transactions))
    a = preprocess(account, df_transactions)
    # store preprocessed data / model input as dictionary
    processed =  a
                
    # return preprocessed data
    return processed

@app.post("/predict")
def root(predict_body: RequestPredict):
    transactions = predict_body.transactions
    account = predict_body.account

    test_data = {
        "account": account,
        "transactions": transactions,
    }

    inputData = preprocess_data(test_data)
    series = pd.Series(inputData)
    series = series.astype(float)
    print(inputData)

    # Call your prediction function/code here
    ####################################################

    # predicted_amount = gbm.predict(transactions, account)

    predicted_amount = gbm.predict(series, predict_disable_shape_check=True)[0]

    # Return predicted amount
    return {"predicted_amount": predicted_amount}