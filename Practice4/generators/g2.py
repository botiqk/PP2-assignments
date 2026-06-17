n = int(input())
even_list = (x for x in range(n+1) if x % 2 == 0)

print(list(even_list))