#!/usr/bin/python3
import sys


def dist(a, b, x, y):
  return abs(x - a) + abs(y - b)


class Ride:
  def __init__(self, a, b, x, y, s, f, idx):
    self.a = a
    self.b = b
    self.x = x
    self.y = y
    self.s = s
    self.f = f
    self.idx = idx
    assert(self.lastOrder() >= self.s)

  def __repr__(self):
    return 'Ride(a={}, b={}, x={}, y={}, s={}, f={}, idx={})'.format(self.a, self.b, self.x, self.y, self.s, self.f, self.idx)

  def dist(self):
    return dist(self.a, self.b, self.x, self.y)

  def lastOrder(self):
    return self.f - self.dist()


class Taxi:
  def __init__(self, idx, x, y, rides=[]):
    self.idx = idx
    self.x = x
    self.y = y
    self.t = 0
    self.rides = rides

  def dist(self, x, y):
    return dist(self.x, self.y, x, y)

  def deliverable(self, ride, T):
    if self.t + self.dist(ride.a, ride.b) <= ride.s:
      return "BONUS"
    elif self.t + self.dist(ride.a, ride.b) + ride.dist() <= min(ride.f, T):
      return "YES"
    else:
      return "NO"

  def deliver(self, ride, B, T, assigned):
    deliverable = self.deliverable(ride, T)
    if deliverable == "BONUS":
      self.t = ride.s + ride.dist()
      self.x, self.y = ride.x, ride.y
      assigned[ride.idx] = True
      return B + ride.dist()
    elif deliverable == "YES":
      self.t += self.dist(ride.a, ride.b) + ride.dist()
      self.x, self.y = ride.x, ride.y
      assigned[ride.idx] = True
      return ride.dist()
    else:
      assigned[ride.idx] = False
      return 0

  def get_score(self, B, T, assigned):
    score = 0
    self.t = 0
    for ride in self.rides:
      score += self.deliver(ride, B, T, assigned)
    return score

  def reassign_ride(self, ride, B, T, assigned):
    orig_score = self.get_score(B, T, assigned)
    for i in range(len(self.rides)):
      self.rides.insert(i, ride)

      new_score = self.get_score(B, T, assigned)
      if new_score > orig_score:
        print("Taxi {} score updated! {} -> {}".format(self.idx, orig_score, new_score))
        break

      self.rides.pop(i)

    self.get_score(B, T, assigned)

    temp_rides = []
    for ride in self.rides:
      if assigned[ride.idx]:
        temp_rides.append(ride)
    self.rides = temp_rides


class City:
  def __init__(self, R, C, B, T, rides, taxies, time=0):
    self.R = R
    self.C = C
    self.B = B
    self.T = T
    self.rides = rides
    self.sorted_rides = rides.copy()
    self.assigned_rides = []
    self.taxies = taxies
    self.time = time

  def get_score(self):
    score = 0
    for taxi in self.taxies:
      score += taxi.get_score(self.B, self.T, self.assigned_rides)
    return score

  def reassign(self):
    for taxi in self.taxies:
      for ride in range(1000):
      # for ride in range(len(self.rides)):
        if self.assigned_rides[ride]:
          continue
        taxi.reassign_ride(self.rides[ride], self.B, self.T, self.assigned_rides)


################################################

def get_input():
  R, C, F, N, B, T = [int(x) for x in input().split()]

  city = City(R, C, B, T, [], [])

  for i in range(N):
    a, b, x, y, s, f = [int(x) for x in input().split()]
    city.rides.append(Ride(a, b, x, y, s, f, i))

  for i in range(F):
    city.taxies.append(Taxi(i, 0, 0))

  # Sort rides by last order
  city.sorted_rides.sort(key=lambda x: x.lastOrder())
  city.assigned_rides = [False] * len(city.rides)
  return city


def parse_output(city, filename):
  f = open(filename)

  for i in range(len(city.taxies)):
    rides = [int(x) for x in f.readline().split()[1:]]
    for x in rides:
      city.assigned_rides[x] = True
    rides = [city.rides[x] for x in rides]
    city.taxies[i].rides = rides

################################################

def main():
  city = get_input()
  print(city.R, city.C, len(city.taxies), len(city.rides), city.B, city.T)

  parse_output(city, sys.argv[1])

  print(city.get_score())
  city.reassign()
  print(city.get_score())

  f = open('d.out', 'w')
  for taxi in city.taxies:
    f.write(str(len(taxi.rides)))
    f.write(' ')
    f.write(' '.join([str(ride.idx) for ride in taxi.rides]))
    f.write('\n')


if __name__ == '__main__':
  main()
