from collections import defaultdict


list1 = []

for i in range(10):
    list1.append(i)

for i in list1:
    if i%2 == 0:
        list1.remove(i)

print(list1)
