
# Задание 1
def fact(n):
    if n ==1:
        return 1
    return n*fact(n-1)

n = int(input())
x = 1
for i in range(1,n+1):
    x *= i
print(fact(n))
print(x)

# Задание 2

a = [int(i) for i in input().split()]
nlist = []
def squer(a):
    if not a:
        return
    nlist.append(a[0]**2)
    return squer(a[1:])
squer(a)
print(nlist)