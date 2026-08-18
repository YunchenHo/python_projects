board = [[''] * 9 for _ in range(9)]
for row in board:
    print(row)


def square_kw(x, **kwargs):
    if kwargs.get('test'):
        return 'test'
    return x ** 2
print(square_kw(3, test=True))
print(square_kw(3, test=False))
print(square_kw(3, test=6)) # 也視為True
print(square_kw(3, othertest=True))# 沒有test
# 如果 test=True 被傳入，那 get('test') 就是 True，所以會回傳字串 'test'
# 如果 test=False 被傳入，那 get('test') 就是 False，所以會回傳 9
# 如果 kwargs 裡面沒有 test 這個鍵，或值是 False，那就正常回傳平方。


def f(arg, *args, **kwargs):
    print(arg)
    print('args:', args)
    print('kwargs:', kwargs)
f('hi', 'yo', 'hey', test='yes', name='Python')
# args: 接收「多個參數」，會形成一個 tuple
# kwargs: 接收「多個關鍵字參數」，會形成一個 dict


def squares(n):
    for i in range(n+1):
        yield i ** 2

for val in squares(3):
    print(val, end=' ')
print('\n')


def primes(n):
    if n < 2:
        return
    n_is_prime = True
    for i in primes(n - 1):
        yield i
        if n % i == 0:
            n_is_prime = False
    if n_is_prime:
        yield n

for p in primes(20):
    print(p, end=' ')
#end: 控制印完之後要加上什麼字串。預設值是換行符號\n

