import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""DEFINE FUNCTIONS"""
def affich():
   print('is working')

def  load_csv(patth,delimiter=',', encoding='utf-8'):
    df = pd.read_csv(patth,delimiter=delimiter, encoding=encoding)
    return df
