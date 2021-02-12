from telethon import functions, types
from scipy.optimize import minimize
from user import User
import numpy as np
import pandas as pd
import math
import time
import os

fL = open(os.getenv('SAVE_PATH') + "locations-"+str(time.time())+".csv", "w")
fL.write("user,lat,lon\n")

def loadLocated():
  df = pd.read_csv(os.getenv('FILE_PATH'), index_col=[0])
  return list(df.index)


located = loadLocated()
dictionary = {}
prev = {}
cleanUpTime = int(os.getenv('CLEANUP_TIME'))
latK = 110574

startLat = float(os.getenv('BASE_LAT'))
startLon = float(os.getenv('BASE_LON'))
lat = startLat
lon = startLon


def saveAndMerge(dstFile):
  fL.flush()
  os.fsync(fL.fileno())
  dst = pd.read_csv(dstFile)
  src = pd.read_csv(fL.name)
  fdf = pd.concat([dst, src])
  fdf = fdf[~((fdf['user'].duplicated(keep='first')) & (fdf['user']!='Point'))]
  fdf = fdf[~fdf.duplicated(keep='first')]
  fdf.to_csv(dstFile, index=False)

def testStuck(result, id):
  if id not in prev:
    prev[id] = {}
  d = {}
  equal = len(result.users) > 0
  for i in range(min(len(result.users), 5)):
    uid = result.users[i].id
    dist = result.updates[0].peers[i].distance
    d[uid] = dist
    if uid not in prev[id] or prev[id][uid] != dist:
      equal = False

  if not equal:
    prev[id] = d
  return equal

async def getNearBy(latM, lonM, cl, savePoint):
  coords = getCoords(latM, lonM)
  if savePoint:
    fL.write('Point,' + str(coords[0]) + ',' + str(coords[1]) + '\n')
  return await cl(functions.contacts.GetLocatedRequest(
    geo_point=types.InputGeoPoint(
      lat=coords[0],
      long=coords[1]
    ),
  ))

def parseResults(result, latM, lonM, n):
  count = 0
  for i in range(len(result.users)):
    uid = result.users[i].id
    dist = result.updates[0].peers[i].distance
    if dist > 100 and uid not in located:
      if count<n:
        print(str(dist), getName(result.users[i]))
        count += 1

      if uid in dictionary:
        dictionary[uid].points[(latM, lonM)] = dist
      else:
        u = User(getName(result.users[i]), time.time(), (latM, lonM), dist)
        dictionary[uid] = u

def getName(user):
  name = ""
  if user.first_name:
    name += user.first_name
  if user.last_name:
    name += ' ' + user.last_name
  if user.username:
    name += ' @' + user.username
  return name.replace(',','|')

def locateUser(uid):
  dist = []
  points = []
  for point in dictionary[uid].points:
    points.append(point)
    dist.append(dictionary[uid].points[point])
  
  points = list(np.array(points))
  if(len(points) >= 3): 
    p = gps_solve(dist, points)
    e = error(p, points, dist)
    c = getCoords(p[0], p[1])
    fL.write(dictionary[uid].name + ',' + str(c[0]) + ',' + str(c[1]) + '\n')
    located.append(uid)
    return p, e
  return (0,0),-1

def cleanDict():
  global dictionary
  t = time.time()
  dictionary = { key:value for (key,value) in dictionary.items() if key not in located and (t-value.time)<cleanUpTime}

def error(x, c, r):
  return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

def gps_solve(distances_to_station, stations_coordinates):
  l = len(stations_coordinates)
  S = sum(distances_to_station)
  W = [((l - 1) * S) / (S - w) for w in distances_to_station]
  x0 = sum([W[i] * stations_coordinates[i] for i in range(l)])
  return minimize(error, x0, args=(stations_coordinates, distances_to_station), method='Nelder-Mead').x

def getCoords(latM, lonM):
  newLat = lat + latM/latK
  newLon = lon + lonM/(111320*math.cos(math.radians(newLat)))
  return (newLat, newLon)

def getCoordsFromBase(latM, lonM):
  newLat = startLat + latM/latK
  newLon = startLon + lonM/(111320*math.cos(math.radians(newLat)))
  return (newLat, newLon)
