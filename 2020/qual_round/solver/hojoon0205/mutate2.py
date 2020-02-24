from __future__ import print_function
import sys

import random

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
lib_chk = [False] * L
for i in range(outL):
    outLinfo1 = [int(x) for x in input_lines[i*2+1].split(' ')]
    #outLinfo2 = [int(y) for y in input_lines[i*2+2].split(' ')]
    lib_order.append(outLinfo1[0])
    lib_chk[outLinfo1[0]] = True

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
            if remain_books <= 0:
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
            if remain_books <= 0:
                break
            if book_chk[bid]:
                continue
            remain_books -= 1
            book_chk[bid] = True
            ans_lib_list[-1].books.append(bid)
        if len(ans_lib_list[-1].books) == 0:
            ans_lib_list.pop(len(ans_lib_list)-1)
    return ans_lib_list

score = calc_score()
ans_lib_list = update_ans()
eprint(len(ans_lib_list))
mutate_cnt = 0
for i in range(10000000):
    if i % 1000 == 0:
        eprint("mutated", mutate_cnt, "in", i, "tries", "score is ", score)
        sys.stderr.flush()
        
    randidx = random.randint(0, outL-1)
    a = lib_order[randidx]
    
    randlib = random.randint(0, L-1)
    while lib_chk[randlib]:
        randlib = random.randint(0, L-1)

    lib_order[randidx] = randlib

    tmp_score = calc_score()
    if tmp_score > score:
        mutate_cnt += 1
        score = tmp_score
        ans_lib_list = update_ans()
        lib_chk[a] = False
        lib_chk[randlib] = True
        f = open("./"+input_file+"_mutate.out", "w")
        print(len(ans_lib_list), file=f)
        for anslib in ans_lib_list:
            print(anslib.id, len(anslib.books), file=f)
            print(*anslib.books, file=f)
        f.close()
    else:
        lib_order[randidx] = a

    ri1, ri2 = random.randint(0, outL-1), random.randint(0, outL-1)
    while ri1 == ri2:
        ri1, ri2 = random.randint(0, outL-1), random.randint(0, outL-1)
    
    a, b = lib_order[ri1], lib_order[ri2]
    book_chk = [False] * B
    libA, libB = libs[a], libs[B]
    for i in range(0, outL):
        if i == a or i == b:
            continue
        for bid in ans_lib_list[i].books:
            book_chk[bid] = True
    
    unreadA = []
    for bid in libA.books:
        if book_chk[bid]:
            continue
        unreadA.append(bid)
    
    unreadB = []
    for bid in libB.books:
        if book_chk[bid]:
            continue
        unreadB.append(bid)
    
    unreadA_B = list(set(unreadA) - set(unreadB)).sort(key=lambda bid: books[bid].S)
    unreadAnB = list(set(unreadA) & set(unreadB)).sort(key=lambda bid: books[bid].S)
    unreadB_A = list(set(unreadB) - set(unreadA)).sort(key=lambda bid: books[bid].S)
    x, y, z = 0, 0, 0
    while x+y+z < len(ans_lib_list[ri1].books)+len(ans_lib_list[ri2].books):
        