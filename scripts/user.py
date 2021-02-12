class User:
  def __init__(self, name, time, point, dist):
    self.name = name
    self.time = time
    self.points = {point: dist}