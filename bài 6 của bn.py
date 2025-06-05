import timeit
import math


def F_recursive(n, memo=None):
    if memo is None:
        memo = {0: 100, 1: 100}  # Khởi tạo memoization
    if n in memo:
        return memo[n]
    factorial_n = math.factorial(n)
    factorial_2n = math.factorial(2 * n)
    memo[n] = ((-1) ** n) * (F_recursive(n - 1, memo) / factorial_n + F_recursive(n // 5, memo) / factorial_2n)
    return memo[n]
def F_iterative(n):
    if n < 2:
        return 100
    F = [100] * (n + 1)  # Khởi tạo tất cả giá trị cho x < 2 bằng 100
    for i in range(2, n + 1):
        factorial_n = math.factorial(i)
        factorial_2n = math.factorial(2 * i)
        F[i] = ((-1) ** i) * (F[i - 1] / factorial_n + F[i // 5] / factorial_2n)
    return F[n]
def compare_methods(max_n):
    recursive_times = []
    iterative_times = []
    results = []
    for n in range(max_n + 1):
        recursive_time = timeit.timeit(lambda: F_recursive(n), number=1)
        recursive_times.append(recursive_time)
    
        iterative_time = timeit.timeit(lambda: F_iterative(n), number=1)
        iterative_times.append(iterative_time)
        recursive_result = F_recursive(n)
        iterative_result = F_iterative(n)
        results.append((n, recursive_result, iterative_result))
    return recursive_times, iterative_times, results
def main():
    try:
        n = int(input("Введите значение n: "))
        if n < 0:
            raise ValueError("Число должно быть неотрицательным.")
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
        return
    recursive_times, iterative_times, results = compare_methods(n)
    print("\nТаблица результатов:")
    print("=" * 90)
    header = f"{'n':<3} | {'Рекурсивное значение':<25} | {'Итеративное значение':<25} | {'Время рекурсии (с)':<20} | {'Время итерации (с)':<20}"
    print(header)
    print("-" * len(header))
    for n, recursive_result, iterative_result in results:
        print(
            f"{n:<3} | {recursive_result:<25.6f} | {iterative_result:<25.6f} | {recursive_times[n]:<20.6f} | {iterative_times[n]:<20.6f}")
    print("=" * 90)
    print("\nАнализ производительности:")
    print(f"Среднее время рекурсии: {sum(recursive_times) / len(recursive_times):.6f} сек")
    print(f"Среднее время итерации: {sum(iterative_times) / len(iterative_times):.6f} сек")
    faster = "рекурсивный" if sum(recursive_times) < sum(iterative_times) else "итеративный"
    print(f"\n{faster} метод работает быстрее в среднем")
if __name__ == "__main__":
    main()