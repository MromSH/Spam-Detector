import pandas as pd
from pathlib import Path

def add_message(_message, _type, df_path):

    df = pd.read_csv(df_path, sep = "\t", header = None, names = ['label', 'text'])
    new_row = {"label": _type, "text": _message}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index = True)

    df.to_csv(df_path, sep = "\t", index = False)

