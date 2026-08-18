import random

# return guess and ans is ?A?B
def check(guess, ans):
    A = sum(1 for x, y in zip(guess, ans) if x == y)
    B = sum(1 for x in guess if x in ans) - A
    return '{}A{}B'.format(A,B)

S = ["7654", "6742" ,"9876", "1234", "2345", "3456", "4567", "5678", "6789", "7890", "8901", "9012", "0123", "3457", "4568", "5679", "6780", "7891", "8902", "9013", "0124", "1235", "2346", "3458", "4569", "5670", "6781", "7892", "8903", "9014"]

ans = "1234"
print("Answer: ", ans)

while True:
    if len(S) == 0:
        print("No solution!")
        break

    guess = random.choice(S)
    cmd = check(guess, ans)
    print(guess," ",cmd)

    if cmd == "4A0B" :
        print("Congrats! The answer is", ans)
        break
    else:
        # update S: remove all element x in S such that check(x,ans) ≠ cmd
        S = [ x for x in S if check(x, ans) != cmd]