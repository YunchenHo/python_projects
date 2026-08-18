import itertools
import functools
import random
from random import randint
from random import sample
from itertools import combinations


for ch in "abc":
    print(ch)

#it = iter(iterable)  # 產生疊代器
#next(it)             # 取下一個元素

lst = [1, 3, 7, 9]
it = iter(lst)
print(next(it))  # ➜ 1
print(next(it))  # ➜ 3
#如果沒有更多元素，再呼叫next(it) 會觸發StopIteration錯誤
print(next(it, 'no more'))  # 如果沒有元素，就回傳'no more'

#for迴圈其實就是在「背後」幫你呼叫iter()和next()
#使用while + next + try-except遍歷list
lst = [1, 3, 7, 9]
it = iter(lst)
while True:
    try:
        i = next(it)
    except StopIteration:
        break
    print(i)

#合併排序用iterator（generator 版本）
def merge(a, b):
    it_a, it_b = iter(a), iter(b)
    item_a = next(it_a, None)
    item_b = next(it_b, None)
    while item_a is not None and item_b is not None:
        if item_a <= item_b:
            yield item_a
            item_a = next(it_a, None)
        else:
            yield item_b
            item_b = next(it_b, None)

    # 為了把最後比完之後，還留在變數中的那個元素吐出來
    if item_a is not None: yield item_a
    if item_b is not None: yield item_b
    # 處理「尾端剩餘資料」的合併，避免遺漏還沒處理的元素
    for item in it_a: yield item
    for item in it_b: yield item

#出來的結果組成一個list
print(list(merge([1, 3, 5, 7], [2, 4, 6])))  # ➜ [1, 2, 3, 4, 5, 6, 7]

#Some Useful Tools
# 1.zip(iter1, iter2, ...)將多個iterable串在一起，逐項配對（最短長度為主）
lst_a = [1, 3, 5]
lst_b = ['a', 'b', 'c', 'd']
for item in zip(lst_a, lst_b):
    print(item)
# ➜ (1, 'a'), (3, 'b'), (5, 'c')

# 2.enumerate(iterable, start=0)將iterable中的元素和索引編號配對
lst = ['apple', 'banana', 'cherry']
for i, item in enumerate(lst):
    print(i, item)

# 3.map(func, iter1, iter2, ...)將多個iterable中的元素傳入func.
# lambda是Python的匿名函式，寫法簡潔，它等價於一個只有一行的def函式，但沒有函式名稱
scores = (40, 50, 60)
new_score = map(lambda x: int(10 * x**0.5), scores)
print(new_score) # <map object at 0x000002A2D57BBFD0>
# map() 回傳的是一個 懶惰（lazy）疊代器，它還沒有真正執行運算。
print(list(new_score)) # [63, 70, 77]

scores = (40, 50, 60)
for new_score in map(lambda x: int(10 * x**0.5), scores):
    print(new_score)

# List → 可以變成 Iterator（用 iter()）
# Generator ⊂ Iterator（是一種特殊的 iterator）
# map/filter/zip/range → 都是 Generator Tool（產生 iterator）
# (x for x in range(5)) → Generator Expression，邊用邊算
# [x for x in range(5)] → List Comprehension，一次產生所有值

characters = ('a','b','c','d','e','f','g')
result = ''.join(characters)
print(result)

print([int(10 * x**0.5) for x in range(0, 100, 5) if x % 2 == 0]) # → List Comprehension，一次產生所有值
gen = (int(10 * x**0.5) for x in range(0, 100, 5) if x % 2 == 0) # → Generator Expression，邊用邊算
print(list(gen))
print(next(gen, 'end'))
print(list(gen))

#itertools & functools
comb = itertools.combinations([1,2,3], 2)  # ➜ 所有兩個一組的組合
print(list(comb))  # ➜ [(1, 2), (1, 3), (2, 3)]
result = functools.reduce(lambda x, y: x + y, [1, 2, 3, 4])
print(result) # ➜ 10

#String Processing
print(chr(65))   # ➜ 'A'
print(ord('A'))  # ➜ 65

print('abc'[0])  # ➜ 'a'
print('abc'[-1]) # ➜ 'c'
print('abcde'[2:])  # ➜ 'cde'
print('abcde'[:2])  # ➜ 'ab'
print('abcde'[1:3]) # ➜ 'bc'
print('abc' in 'zabc') # ➜ True

#isdecimal(): 判斷字串是否完全由0–9的數字組成
print('123'.isdecimal())   # True，因為全是數字字元
'１２３'.isdecimal()  # True，全形數字也算
'123.0'.isdecimal()   # False，有小數點
'3²'.isdecimal()      # False，有非阿拉伯數字

#.isalnum(): 判斷字串是否只包含英文字母與數字（A-Z, a-z, 0–9），不能有空格或標點符號。
print('abc123'.isalnum())  # True

#.split('"') 表示以 " 為分隔符號把字串分成多段，回傳一個list。
print('<a href="...">'.split('"')) # ➜ ['<a href=', '...']

#.format()：格式化字串
print('Case {}: {}, {}'.format(1, 68.7, 'passed'))
# ➜ 'Case 1: 68.7, passed'


# 從 0 到 9 之間猜一個數字
def read_a_digit():
    ret = -1
    while True:
        try:
            ret = int(input('Input a digit: '))
        except ValueError:
            print('Not an integer')
            continue
        if 0 <= ret <= 9:
            return ret
        print(ret, 'is not in {0,...,9}.')

ans = randint(0, 9)  # 答案是 0~9 的隨機整數
guess = read_a_digit()

while guess != ans:
    if ans < guess:
        print(guess, 'is greater than the answer.')
    else:
        print(guess, 'is less than the answer.')
    guess = read_a_digit()
print('Congrats! The answer is', ans)

# 幾A幾B
def valid(s):
    if len(s)!=4:
        return False                     # 長度必須是 4
    if any(x not in '0123456789' for x in s):
        return False                     # 每個字元必須是數字
    if any(x==y for x, y in combinations(s,2)):
        return False                     # 不可以有重複數字
    return True

def read_four_distinct_digits():
    while True:
        ret = input('Input four distinct digits: ')
        if valid(ret):                  # 用剛剛的 valid 檢查
            return ret
        print(ret,'is not valid.')      # 無效就提示

ans = ''.join(sample('0123456789',4))
#sample: 從指定的序列中隨機選擇指定數量的元素(不重複)，並以列表的形式返回
#[3, 7, 1, 9] → '3719'

guess = read_four_distinct_digits()
while guess != ans:
    A = sum(1 for x, y in zip(guess, ans) if x == y)
    B = sum(1 for x in guess if x in ans) - A
    print(guess, 'is {}A{}B.'.format(A, B))
    guess = read_four_distinct_digits()
print('Congrats! The answer is', ans)



