import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

#keep first three letters
df['user'] = df['user'].apply(lambda x: x if x == 'Point' else x[0:4] if x[0] == '@' else x[:min(3, x.rfind('@'))] if '@' in x else x[:3])

df.to_csv("locationsAnon.csv", index=False)
