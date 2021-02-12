import time
from telethon.sync import TelegramClient
from telethon import functions, types
import sys
import os
import asyncio
import math
import numpy as np

from dotenv import load_dotenv
load_dotenv()

import utils

api_id = os.getenv('API_ID1')
api_hash = os.getenv('API_HASH1')
client = TelegramClient('anon', api_id, api_hash)

api_id2 = os.getenv('API_ID2')
api_hash2 = os.getenv('API_HASH2')
client2 = TelegramClient('anon2', api_id2, api_hash2)

#Max 20m/s | 72km/h
length = int(os.getenv('POINT_DISTANCE'))
cooldown = length/20

#Grid
height = int(os.getenv('GRID_HEIGHT'))
width = int(os.getenv('GRID_WIDTH'))
start = (int(os.getenv('START_X')), int(os.getenv('START_Y')))
multiplier = 3

dst = os.getenv('FILE_PATH')


async def getDist(latM, lonM, cl):
  n = 0
  result = await utils.getNearBy(latM, lonM, cl, True)
  while utils.testStuck(result, cl.api_id):
    n += 1
    print("Stuck -", n)
    result = await utils.getNearBy(latM, lonM, cl, False)
    time.sleep(cooldown)
  
  l = len(result.users)
  print(utils.getCoords(latM, lonM), l)
  utils.parseResults(result, latM, lonM, 5)
  print()
  return l
      
async def mapSquare(dir):
  if dir:
    await getDist(-length/2, -length/2, client)
    await getDist(+length/2, -length/2, client2)
    time.sleep(cooldown)
    await getDist(-length/2, +length/2, client)
    await getDist(+length/2, +length/2, client2)
  else:
    await getDist(-length/2, +length/2, client)
    await getDist(+length/2, +length/2, client2)
    time.sleep(cooldown)
    await getDist(-length/2, -length/2, client)
    await getDist(+length/2, -length/2, client2)
  
  e = []
  for uid in utils.dictionary:
    p, err = utils.locateUser(uid)
    if err>0:
      e.append(err)

  utils.saveAndMerge(dst)
  utils.cleanDict()
  print("Dict length:", len(utils.dictionary))
  if len(e) > 0:
    print("Avg Error:", np.mean(e))
    print("Min Error:", np.amin(e))
    print("Max Error:", np.amax(e))
  print("\n\n")

def updateCoords(i, j):
  c = utils.getCoordsFromBase(i*(length*multiplier),j*(length*multiplier))
  utils.lat = c[0]
  utils.lon = c[1]

async def executeCycle(i, j, dir):
  updateCoords(i, j)
  await mapSquare(dir)  
  time.sleep(math.ceil(length*(multiplier-1)/20)+1)

async def main():
  i, j = start
  while i < height:
    if i%2 == 0:
      while j < width:
        await executeCycle(i, j, 1)
        j += 1
      i += 1
      j = width-1
    
    while j >= 0:
      await executeCycle(i, j, 0)
      j -= 1
    i += 1
    j = 0

#Main execution
if __name__ == '__main__':
  try:
    client.start()
    client2.start()
    asyncio.get_event_loop().run_until_complete(main())
  except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
