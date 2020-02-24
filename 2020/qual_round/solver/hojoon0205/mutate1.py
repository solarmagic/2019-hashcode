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

    def __repr__(self):
        return 'Library(id={}, books[:3]={})'.format(self.id, self.books[:3])

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
    libbookinfo = [ int(k) for k in input_lines[linenum].split(' ') ]
    libbookinfo.sort(key= lambda s: -books[s].S)
    #print(libnum)
    libs.append(Library(libnum, libbookinfo, libinfo[1], libinfo[2]))
    linenum += 1

f.close()


f = open("./" + input_file + ".out", "r")
input_lines = f.readlines()
outL = int(input_lines[0])
lib_order = []
for i in range(outL):
    outLinfo1 = [int(x) for x in input_lines[i*2+1].split(' ')]
    #outLinfo2 = [int(y) for y in input_lines[i*2+2].split(' ')]
    lib_order.append(outLinfo1[0])

class Ans_Lib:
    def __init__(self, id, books):
        self.id = id
        self.books = books

ans_lib_list = []

def calc_score():
    score = 0
    cur_time = 0
    book_chk = [False] * B
    for libid in lib_order:
        libinfo = libs[libid]
        cur_time += libinfo.signup
        remain_time = D - cur_time
        remain_books = min(remain_time * libinfo.scanlimit, len(libinfo.books))
        for bid in libinfo.books:
            if remain_books == 0:
                break
            if book_chk[bid]:
                continue
            remain_books -= 1
            score += books[bid].S
            book_chk[bid] = True
    return score


def update_ans():
    ans_lib_list = []
    cur_time = 0
    book_chk = [False] * B
    for libid in lib_order:
        ans_lib_list.append(Ans_Lib(libid, []))
        libinfo = libs[libid]
        cur_time += libinfo.signup
        remain_time = D - cur_time
        remain_books = min(remain_time * libinfo.scanlimit, len(libinfo.books))
        for bid in libinfo.books:
            if book_chk[bid]:
                continue
            remain_books -= 1
            book_chk[bid] = True
            ans_lib_list[-1].books.append(bid)
    return ans_lib_list

score = calc_score()
ans_lib_list = update_ans()
eprint(len(ans_lib_list))
for i in range(outL-1):
    if i % 1000 == 0:
        eprint(i)
    a, b = lib_order[i], lib_order[i+1]
    lib_order[i], lib_order[i+1] = b, a
    tmp_score = calc_score()
    if tmp_score > score:
        score = tmp_score
        ans_lib_list = update_ans()
    else:
        a, b = lib_order[i], lib_order[i+1]
        lib_order[i], lib_order[i+1] = b, a

print(len(ans_lib_list))
for anslib in ans_lib_list:
    print(anslib.id, len(anslib.books))
    print(*anslib.books)
