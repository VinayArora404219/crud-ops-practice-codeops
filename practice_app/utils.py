import pandas as pd
from django.core.exceptions import ValidationError


def check_missing_values(df):
    for col in df.columns:
        print(col)
        miss = df[col].isnull().sum()
        if miss > 0:
            raise ValidationError("{} has {} missing value(s)".format(col, miss))
        else:
            pass


def validate_csv(df):
    check_missing_values(df)

