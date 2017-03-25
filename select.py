a = [1, 8, 10, 3, 9, 5, 4, 2, 7, 6]
a = [2, 1, 3, 4, 5]
a = [7, 3, 5, 6]
max = 9


def select(a, max):
    print("Running: N=" + str(len(a)) + "; array = ", a)
    n = len(a)
    sum = 0
    for i in a:
        sum += i
    print("sum = " + str(sum))
    if (sum <= max):
        return a
    else:
        start = select(a[0:n - 1], max)
        end = select(a[1:n], max)
        if (start > end):
            return start
        else:
            return end


result = select(a, max)

print("Final result = ", result)
