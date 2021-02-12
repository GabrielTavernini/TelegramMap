import pandas as pd

#keep first three letters
df = pd.read_csv(sys.argv[1])
df['user'] = df['user'].apply(lambda x: x if x == 'Point' else x[1:4] if x[0] == '@' else x[:min(3, x.rfind('@'))] if '@' in x else x[:3])

df.to_csv("locationsAnon.csv", index=False)
