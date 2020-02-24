from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

input_file = input()

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
        self.chk = False

    def __repr__(self):
        return 'Library(id={}, books[:3]={})'.format(self.id, self.books[:3])

    def get_max_score(self, cur_time, deadline, already_read):
        can_new_read = list(self.books - already_read)
        can_new_read.sort(key=lambda bid : -books[bid].S)
        remaintime = deadline - cur_time - self.signup
        can_read_num = min(remaintime * self.scanlimit, len(can_new_read))
        can_new_read = can_new_read[:can_read_num]
        return sum(books[bid].S for bid in can_new_read), set(can_new_read)



f = open("../../input/" + input_file + ".in", "r")
input_lines = f.readlines()
base_info = [ int(k) for k in input_lines[0].split(' ') ]

B = base_info[0]
L = base_info[1]
D = base_info[2]

book_info = [ int(k) for k in input_lines[1].split(' ') ]
books = {}
cnt = 0
for b_score in book_info:
    books[cnt] = Book(cnt, b_score)
    cnt += 1

linenum = 2
libs = []
for libnum in range(L):
    libinfo = [ int(k) for k in input_lines[linenum].split(' ') ]
    linenum += 1
    libbookinfo = set([ int(k) for k in input_lines[linenum].split(' ') ])
    #print(libnum)
    libs.append(Library(libnum, libbookinfo, libinfo[1], libinfo[2]))
    linenum += 1

# greedy 

class Ans_Lib:
    def __init__(self, id, books):
        self.id = id
        self.books = books

ans_libs = []

cur_time = 0
already = set()
while cur_time < D:
    maxscore = -1
    m_readbook = set()
    m_stime = 0
    m_id = 0
    for libr in libs:
        if libr.chk:
            continue
        score, readbook = libr.get_max_score(cur_time, D, already)
        if score > maxscore:
            maxscore = score
            m_readbook = readbook.copy()
            m_stime = libr.signup
            m_id = libr.id
    cur_time += m_stime
    already.union(m_readbook)
    libs[m_id].chk = True
    ans_libs.append(Ans_Lib(m_id, list(m_readbook)))

    if len(ans_libs) % 1000 == 0:
        eprint(len(ans_libs))

print(len(ans_libs))
for anslib in ans_libs:
    print(anslib.id, len(anslib.books))
    print(*anslib.books)