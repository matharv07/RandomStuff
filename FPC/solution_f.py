def check_power(number, denom, power):
    if number % denom == 0:
        return check_power(number//denom, denom, power + 1)
    return power


n = int(input())
x_list = []
y_list = []
for _ in range(n):
    rx, ry = map(int, input().split())
    x_list.append(rx)
    y_list.append(ry)
max_y = max(y_list)

is_prime = [[True, 0] for _ in range(max_y + 1)]
is_prime[0][0] = is_prime[1][0] = False

p = 2
while p * p <= max_y:
    if is_prime[p][0]:
        for i in range(p * p, max_y + 1, p):
            is_prime[i][0] = False
    p += 1

for y_item in y_list:
    for num, prime_entry in enumerate(is_prime):
        if prime_entry[0] and num >= 2:
            prime_entry[1] = max(check_power(y_item, num, 0), prime_entry[1])

final_Y = 1
for number, p in enumerate(is_prime):
    if p[0]:
        final_Y *= number**p[1]

final_X = 0
for iteration, x_item in enumerate(x_list):
    final_X += x_item * (final_Y // y_list[iteration])

MOD = 998244353

import math

mod_Y = 1
mod_X = 0

common = math.gcd(final_X, final_Y)
reduced_X = final_X // common
reduced_Y = final_Y // common

mod_X = reduced_X % MOD
mod_Y = reduced_Y % MOD

print(mod_X)
print(mod_Y)