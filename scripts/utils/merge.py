import pandas as pd
import sys
from dotenv import load_dotenv
load_dotenv()

src = pd.read_csv(sys.argv[1])
dst = pd.read_csv(os.getenv('FILE_PATH'))

fdf = pd.concat([dst, src])
fdf = fdf[~((fdf['user'].duplicated(keep='first')) & (fdf['user']!='Point'))]
fdf = fdf[~fdf.duplicated(keep='first')]
fdf.to_csv(os.getenv('FILE_PATH'), index=False)