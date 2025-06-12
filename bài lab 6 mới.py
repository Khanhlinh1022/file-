import math
import time
from functools import lru_cache
def F_rec(n):
   
    if n < 2:
        return 100
    sign = -1 if n % 2 else 1
    term1 = F_rec(n - 1) / math.factorial(n)
    term2 = F_rec(n // 5) / math.factorial(2 * n)
    return sign * (term1 + term2)
def F_iter(n):
    if n < 2:
        return 100
    results = [100] * (n + 1)  
    factorials = [1] * (2*n + 1)  
    for i in range(1, 2*n + 1):
        factorials[i] = factorials[i-1] * i
    for i in range(2, n + 1):
        sign = -1 if i % 2 else 1
        term1 = results[i-1] / factorials[i]
        term2 = results[i//5] / factorials[2*i]
        results[i] = sign * (term1 + term2)
    return results[n]

def compare(n_max):
   
    print(f"{'n':<5} | {'Iterative':<25} | {'Recursive':<25} | {'Iter Time (ms)':<15} | {'Rec Time (ms)':<15}")
    print("-" * 90)
    for n in range(n_max + 1):
        start_iter = time.perf_counter()
        fi = F_iter(n)
        time_iter = (time.perf_counter() - start_iter) * 1000
        try:
            start_rec = time.perf_counter()
            fr = F_rec(n)
            time_rec = (time.perf_counter() - start_rec) * 1000
            
            print(f"{n:<5} | {fi:<25.14e} | {fr:<25.14e} | {time_iter:<15.5f} | {time_rec:<15.5f}")
        except RecursionError:
            print(f"{n:<5} | {fi:<25.14e} | {'RecursionError':<25} | {time_iter:<15.5f} | {'-':<15}")
if __name__ == "__main__":
    compare(20)