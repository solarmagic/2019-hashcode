#!/usr/bin/python3
import sys
import random

class Book:
  def __init__(self, id, score):
    self.id = id
    self.score = score

  def __repr__(self):
    return 'Book(id={}, score={})'.format(self.id, self.score)

class Library:
  def __init__(self, id, bs, signup, scanlimit):
    self.id = id
    self.books = bs
    self.books.sort(key=lambda x: -books[x].score)
    self.signup = signup
    self.scanlimit = scanlimit

  def __repr__(self):
    return 'Library(id={}, books[:3]={})'.format(self.id, self.books[:3])

  def probableScore(self):
    num = max((D - int(avg_signup) - self.signup) * self.scanlimit, 0)
    b = self.books[:min(num, len(self.books))]
    return sum(b) / self.signup

  def getScan(self, t, used):
    num = max((D - t - self.signup) * self.scanlimit, 0)
    filtered = [x for x in self.books if x not in used]
    b = filtered[:min(num, len(filtered))]
    return Scan(self.id, b)

class Scan:
  def __init__(self, lib, books):
    self.lib = lib
    self.books = books

  def __repr__(self):
    return 'Scan(lib={}, books[:3]={})'.format(self.lib, self.books[:3])

  def getLib(self):
    return libs[self.lib]

  def ignore(self, t):
    l = self.getLib()
    num = (D - t - l.signup) * l.scanlimit
    self.books = self.books[:min(num, len(self.books))]

################################################################
books = []
libs = []
scans = []

def get_input(filename):
  global B, L, D, books, libs
  global avg_signup
  f = open(filename)

  B, L, D = [int(x) for x in f.readline().split()]

  S = [int(x) for x in f.readline().split()]
  for i in range(B):
    books.append(Book(i, S[i]))

  for i in range(L):
    N, T, M = [int(x) for x in f.readline().split()]
    b = [int(x) for x in f.readline().split()]
    libs.append(Library(i, b, T, M))

  ################
  avg_signup = 0
  for lib in libs:
    avg_signup += lib.signup
  avg_signup /= len(libs)

  avg_signup

def parse_state(filename):
  if filename == None:
    return
  f = open(filename)

  A = int(f.readline())
  t = 0

  for i in range(A):
    Y, K = [int(x) for x in f.readline().split()]
    b = [int(x) for x in f.readline().split()]
    s = Scan(Y, b)
    s.ignore(t)
    t += s.getLib().signup
    scans.append(s)

def export_state(filename):
  if filename == None:
    return

  f = open(filename, 'w')

  A = len(scans)
  f.write(str(A) + '\n')

  for i in range(A):
    Y, K = scans[i].lib, len(scans[i].books)
    f.write('{} {}\n'.format(str(Y), str(K)))
    f.write(' '.join(str(x) for x in scans[i].books) + '\n')

################################################################
def getScore():
  scanned = set()
  t = 0
  for s in scans:
    s.ignore(t)
    t += s.getLib().signup
    for b in s.books:
      scanned.add(b)

  score = 0
  for b in scanned:
    score += books[b].score
  return score

def calc():
  sortedLib = sorted(libs, key=lambda x: -x.probableScore())
  used = set()
  t = 0
  for i in range(len(sortedLib)):
    lib = sortedLib[i]
    if t + lib.signup > D:
      continue
    s = lib.getScan(t, used)
    if len(s.books) <= 2:
      continue

    scans.append(s)
    t += lib.signup
    for b in s.books:
      used.add(b)

def recalc():
  global scans
  used = set()
  newScans = []
  t = 0
  for i in range(len(scans)):
    lib = libs[scans[i].lib]
    if t + lib.signup > D:
      continue
    s = lib.getScan(t, used)
    if len(s.books) <= 2:
      continue

    newScans.append(s)
    t += lib.signup
    for b in s.books:
      used.add(b)

  scans = newScans

################################################################
from simulated_annealing import *

class State(State):
  def __init__(self, scans):
    self.used = set([x.lib for x in scans])
    self.unused = set(range(len(libs))) - self.used
    self._score = getScore()

  def score(self):
    self._score = getScore()
    return self._score

  def random_mutation(self):
    p = random.random()
    if p < 0.5:
      mut = StateMutation('Insert', random.choice(list(self.unused)))
    else:
      mut = StateMutation('Replace', random.choice(list(self.unused)))
    # print(mut) ####
    return mut

  def apply_mutation(self, mut):
    if mut.type == 'Insert':
      if mut.idx == None:
        return
      scans.insert(mut.idx, Scan(mut.lib, []))
    if mut.type == 'Replace':
      scans[mut.idx] = Scan(mut.lib, [])

    recalc()
    self.used = set([x.lib for x in scans])
    self.unused = set(range(len(libs))) - self.used

  def improvement(self, mut):
    global scans
    orig_scan = scans.copy()
    delta = -10

    if mut.type == 'Insert':
      for i in random.sample(range(len(scans)+1), min(len(scans)+1, 100)):
        scans.insert(i, Scan(mut.lib, []))
        recalc()
        score = getScore()
        if score > self._score:
          delta = score - self._score
          mut.idx = i
          break
        scans = orig_scan.copy()
      scans = orig_scan.copy()

      return delta

    if mut.type == 'Replace':
      for i in random.sample(range(len(scans)), min(len(scans), 100)):
        scans[i] = Scan(mut.lib, [])
        recalc()
        score = getScore()
        if score > self._score:
          delta = score - self._score
          mut.idx = i
          break
        scans = orig_scan.copy()
      scans = orig_scan.copy()

      return delta


class StateMutation(Mutation):
  def __init__(self, type, lib, idx=None):
    self.type = type
    self.lib = lib
    self.idx = idx

  def __repr__(self):
    return 'Mutation(type={}, lib={}, lib2={}, idx={})'.format(self.type, self.lib, self.lib2, self.idx)

################################################################

def main():
  infile = '../../input/' + sys.argv[1]
  outfile = None if len(sys.argv) <= 2 else '../../output/queued/' + sys.argv[2]
  statefile = None if len(sys.argv) <= 3 else '../../output/queued/' + sys.argv[3]
  print("OUTPUT PATH:", outfile)

  get_input(infile)
  parse_state(statefile)

  ################################
  # main logic

  # print(books)
  # print(libs)
  # print(scans)
  if not statefile:
    calc()
  print("SCORE:", getScore())

  scansState = State(scans)
  simulation = SimulatedAnnealing(ExpCoolingSchedule(1, 0.95), ExpAcceptancePolicy())
  simulation.set_state(scansState)
  simulation.run(10000, lambda : export_state(outfile))

  print("SCORE:", getScore())

  ################################

  export_state(outfile)

if __name__ == '__main__':
  if not (2 <= len(sys.argv) and len(sys.argv) <= 4):
    print("Usage: solve.py [infile] [outfile] [statefile]")
    exit(1)
  main()
