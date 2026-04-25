import pandas as pd
try:
    df = pd.read_excel('inputs/Test cases - App.vwo.com.xlsx', sheet_name='Login')
    print("COLUMNS:", df.columns.tolist())
except Exception as e:
    print("Error:", e)
