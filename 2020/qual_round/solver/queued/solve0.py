#!/usr/bin/python3
import sys

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

  def getScan(self, t):
    num = max((D - t - self.signup) * self.scanlimit, 0)
    b = self.books[:min(num, len(self.books))]
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
  for s in scans:
    for b in s.books:
      scanned.add(b)

  score = 0
  for b in scanned:
    score += books[b].score
  return score

def calc():
  sortedLib = sorted(libs, key=lambda x: -x.probableScore())
  t = 0
  for i in range(len(sortedLib)):
    lib = sortedLib[i]
    if t + lib.signup >= D:
      break
    scans.append(lib.getScan(t))

################################################################

def main():
  infile = '../../input/' + sys.argv[1]
  outfile = None if len(sys.argv) <= 2 else '../../output/queued/' + sys.argv[2]
  statefile = None if len(sys.argv) <= 3 else sys.argv[3]
  print("OUTPUT PATH:", outfile)

  i = get_input(infile)
  s = parse_state(statefile)

  ################################
  # main logic

  # print(books)
  # print(libs)
  # print(scans)
  calc()

  print("SCORE:", getScore())

  ################################

  export_state(outfile)

if __name__ == '__main__':
  if not (2 <= len(sys.argv) and len(sys.argv) <= 4):
    print("Usage: solve.py [infile] [outfile] [statefile]")
    exit(1)
  main()
