import importlib.resources
import pandas as pd


def load_csv(csv_file):
    with importlib.resources.files('ulib.resources').joinpath(csv_file).open('r') as f:
        return pd.read_csv(f)

