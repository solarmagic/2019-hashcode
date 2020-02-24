#!/usr/bin/python3
import sys

class Book:
  def __init__(self, id, S):
    self.id = id
    self.S = S

  def __repr__(self):
    return 'Book(id={}, S={})'.format(self.id, self.S)

class Library:
  def __init__(self, id, books, signup, scanlimit):
    self.id = id
    self.books = books
    self.signup = signup
    self.scanlimit = scanlimit

  def __repr__(self):
    return 'Library(id={}, books[:3]={})'.format(self.id, self.books[:3])


################################################################
books = []
libraries = []

def get_input(filename):
  global B, L, D, books, libraries
  f = open(filename)

  B, L, D = [int(x) for x in f.readline().split()]

  S = [int(x) for x in f.readline().split()]
  for i in range(B):
    books.append(Book(i, S[i]))

  for i in range(L):
    N, T, M = [int(x) for x in f.readline().split()]
    b = [int(x) for x in f.readline().split()]
    libraries.append(Library(i, books, T, M))


get_input("f.in")

mini = 1234567890
maxi = 0
nmini = 1234567890
nmaxi = 0
scanmini = 1234567890
scanmaxi = 0
upmini = 1234567890
upmaxi = 0

rmini, rmaxi = 1234567890.0, 0.0

zeron = 0

for i in range(len(books)):
    mini = min(mini, books[i].S)
    maxi = max(maxi, books[i].S)

for i in range(len(libraries)):
    nmini = min(nmini, len(libraries[i].books))
    nmaxi = max(nmaxi, len(libraries[i].books))
    scanmini = min(scanmini, libraries[i].scanlimit)
    scanmaxi = max(scanmaxi, libraries[i].scanlimit)
    upmini = min(upmini, libraries[i].signup)
    upmaxi = max(upmaxi, libraries[i].signup)
    if libraries[i].signup == 0:
        zeron += 1
    else:
        rmini = min(rmini, libraries[i].scanlimit / libraries[i].signup)
        rmaxi = max(rmaxi, libraries[i].scanlimit / libraries[i].signup)

print(mini, maxi)
print(nmini, nmaxi)
print(scanmini, scanmaxi)
print(upmini, upmaxi)
print(rmini, rmaxi)