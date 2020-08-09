import numpy as np
import pandas as pd


# Calculate pScore
x = []
p_score = dict.fromkeys(x)
for var in x:
    for i in range(0, len(df)):
        n = df[var][i]**2
        p_score[var] += n
    p_score[var] = p_score[var]**1/2

# Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)