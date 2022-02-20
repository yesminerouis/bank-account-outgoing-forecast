import pandas as pd
import numpy as np
import json

def convert_to_month_year(df: pd.DataFrame):
    """ Converts regular date format (Y-M-d) to month-year format (m-Y)."""
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['year'] = pd.to_datetime(df['date']).dt.year
    return df

def get_monthly_outgoing(df: pd.DataFrame):
    """ Sums the outgoing amounts ( <0 transactions) in the same month and sorts chronologically."""
    ROC = df.loc[df.amount<0]
    if not ROC.empty:
        ROC = ROC.set_index("date")
        df_outgoing = ROC.groupby(['month', 'year'], 
                                                as_index=False)['amount'].sum()
        df_outgoing.sort_values(by=['month', 'year'], inplace=True)
        df_outgoing = df_outgoing.rename(columns={"amount": "outgoing"})
    else:
        df_outgoing = df.groupby(['month', 'year'],as_index=False)['amount'].sum()
        df_outgoing['outgoing'] = 0
    return df_outgoing

    
    return df_outgoing

def get_monthly_ingoing(df: pd.DataFrame):
    """ Sums the ingoing amounts (> 0 transactions)  in the same month and sorts chronologically."""
    ROC = df.loc[df.amount>=0]
    
    if not ROC.empty:
        ROC = ROC.set_index("date")
        df_ingoing = ROC.groupby(['month', 'year'], as_index=False)['amount'].sum()
        df_ingoing.sort_values(by=['month', 'year'], inplace=True)
        df_ingoing = df_ingoing.rename(columns={"amount": "ingoing"})
    else:
        df_ingoing = df.groupby(['month', 'year'],as_index=False)['amount'].sum()
        df_ingoing['ingoing'] = 0
    return df_ingoing

def compute_average_transactions_per_month(df: pd.DataFrame):
    """ Computes the number of transactions per month the account. """
    ROC = df.groupby(['month', 'year'],
              as_index=False)['amount'].count()
    ROC = ROC.rename(columns={"amount": "average_transactions_per_month"})
    return ROC

def compute_account_age(account, df: pd.DataFrame):
    """ Compute the age of the account (Number of months between the update date and the oldest transation date). """
    oldest_df = df.sort_values('date', ascending=False).tail(1)
    age = ((account.update_date - oldest_df.date)/np.timedelta64(1, 'M')).astype(int)
    
    return age

def compute_initial_balance(account, df: pd.DataFrame):
    """ Computes the initial balance of the account given the last balance and the historical transactions. """
    sum_transactions = df['amount'].sum()
    initial_balance = account.balance - sum_transactions
    return initial_balance

def Hist(df: pd.DataFrame, n):
    """ Computes the n th previous average amount of transactions for the account. """
    df['outgoing_'+str(n)] = df['outgoing'].shift(n)
    df['ingoing_'+str(n)] = df['ingoing'].shift(n)
    return df

def preprocess(account, df: pd.DataFrame):
    """ Prerocess function given the account and transactions dataframes. """
    print(df.head())
    data = convert_to_month_year(df)
    # remove duplicates 
    data=data[data.duplicated()==False]
    # Compute and Add the feature ingoing to the data
    data_monthly = get_monthly_outgoing(data)
    
    # Add the feature ingoing to the data
    data_ingoing = get_monthly_ingoing(data)
    keys = ['month', 'year']
    data_monthly = pd.merge(data_monthly, data_ingoing, on = keys, how = 'inner')
    
    df_transactions_number = compute_average_transactions_per_month(data)
    # Add the feature average_transactions_per_month to the data
    data_monthly = pd.merge(data_monthly, df_transactions_number, on = keys, how = 'inner')
    # Compute the age of the account
    account_age = compute_account_age(account, data)    
    data_monthly['age'] = account_age.iloc[0]

    # Compute the initial balance of the account
    initial_balance = compute_initial_balance(account, data)
    data_monthly['initial_balance'] = initial_balance
    
    N = 6
    for n in range (1,N+1):
        Hist(data_monthly, n)
    print('je teste')
    df_row = data_monthly.sort_values(['month'], ascending = (False)).head(1)
    print(df_row)
    parsed = {
        'month': df_row.iloc[0].month,
        'average_transactions_per_month': df_row.iloc[0].average_transactions_per_month,
        'age': df_row.iloc[0].age,
        'initial_balance': df_row.iloc[0].initial_balance,
        'outgoing_1': df_row.iloc[0].outgoing_1,
        'ingoing_1': df_row.iloc[0].ingoing_1,
        'outgoing_2': df_row.iloc[0].outgoing_2,
        'ingoing_2': df_row.iloc[0].ingoing_2,
        'outgoing_3': df_row.iloc[0].outgoing_3,
        'ingoing_3': df_row.iloc[0].ingoing_3,
        'outgoing_4': df_row.iloc[0].outgoing_4,
        'ingoing_4': df_row.iloc[0].ingoing_4,
        'outgoing_5': df_row.iloc[0].outgoing_5,
        'ingoing_5': df_row.iloc[0].ingoing_5,
        'outgoing_6': df_row.iloc[0].outgoing_6,
        'outgoing_6': df_row.iloc[0].outgoing_6
    }
    #parsed = json.dumps(df_row, indent=4) 
    return parsed
    



if __name__ == "__main__":
    print('Begin Preprocessing...')