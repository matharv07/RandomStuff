n = int(input())
x_list = []
y_list = []
for _ in range(n):
    inx, iny = map(int, input().split())
    x_list.append(inx)
    y_list.append(iny)
max_y = max(y_list)

limit = max_y + 1
spf = list(range(limit))
p = 2
while p * p < limit:
    if spf[p] == p:
        for i in range(p * p, limit, p):
            if spf[i] == i:
                spf[i] = p
    p += 1

prime_data = {} 

for index, value in enumerate(y_list):
    temp = value
    while temp > 1:
        p = spf[temp]
        count = 0
        while temp % p == 0:
            temp //= p
            count += 1
        
        if p not in prime_data:
            prime_data[p] = []
        prime_data[p].append((count, index))
        
final_exponents = {}

NUMBER = 998244353

for p, entries in prime_data.items():
    max_exp = 0
    for exp, index in entries:
        if exp > max_exp: max_exp = exp
        
    M = p ** (max_exp + 1)
    total_sum = 0
    for exp, index in entries:
        p_pow_e = p ** exp
        y_part = y_list[index] // p_pow_e
        inv_y = pow(y_part, -1, M)
        term = x_list[index] * inv_y
        if max_exp > exp:
            term *= (p ** (max_exp - exp))
        
        total_sum = (total_sum + term)
        
    total_sum %= M
    
    current_exp = max_exp
    while current_exp > 0 and total_sum % p == 0:
        total_sum //= p
        current_exp -= 1
        
    if current_exp > 0:
        final_exponents[p] = current_exp

final_Y = 1
for p, exp in final_exponents.items():
    term = pow(p, exp, NUMBER)
    final_Y = (final_Y * term) % NUMBER
    
final_X = 0
for i in range(n):
    y_val = y_list[i]
    inv_y = pow(y_val, NUMBER - 2, NUMBER)
    term = (x_list[i] * final_Y * inv_y) % NUMBER
    final_X = (final_X + term) % NUMBER
    
print(final_X)
print(final_Y)

