def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def multiplicative_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None 
    else:
        return x % m  

# a = 56
# b = 98 
# answer 14, 7

a = int(input("Enter a: "))
b = int(input("Enter b: "))


gcd_result = gcd(a, b)
print(f"GCD of {a} and {b} is {gcd_result}")

inverse = multiplicative_inverse(a, b)
if inverse:
    print(f"Multiplicative inverse of {a} mod {b} is {inverse}")
else:
    print(f"Multiplicative inverse of {a} mod {b} does not exist")
