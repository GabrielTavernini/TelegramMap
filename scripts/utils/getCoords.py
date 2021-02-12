import sys
import math
import os
from dotenv import load_dotenv
load_dotenv()

startLat = float(os.getenv('BASE_LAT'))
startLon = float(os.getenv('BASE_LON'))
latK = 110574

def getCoordsFromBase(latM, lonM):
  newLat = startLat + latM/latK
  newLon = startLon + lonM/(111320*math.cos(math.radians(newLat)))
  return (newLat, newLon)

print(getCoordsFromBase(int(sys.argv[1]), int(sys.argv[2])))
