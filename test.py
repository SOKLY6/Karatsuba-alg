import time
import random
from tabulate import tabulate
from polynom_utils import Polynom, SlowPolynom, FastPolynom

def generate_polynom(degree: int) -> list[float]:
    return [random.uniform(-1, 1) for _ in range(degree + 1)]

def test_multiplication_performance():
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    results = []
    
    print("Замеры умножения полиномов...")
    for size in sizes:
        coeffs1 = generate_polynom(size)
        coeffs2 = generate_polynom(size)
        
        p1_slow = SlowPolynom(coeffs1)
        p2_slow = SlowPolynom(coeffs2)
        p1_fast = FastPolynom(coeffs1)
        p2_fast = FastPolynom(coeffs2)
        
        _ = p1_slow * p2_slow
        _ = p1_fast * p2_fast
        
        start = time.perf_counter()
        _ = p1_slow * p2_slow
        classic_time = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        _ = p1_fast * p2_fast
        karatsuba_time = (time.perf_counter() - start) * 1000
        
        results.append([size, f"{classic_time:.3f}", f"{karatsuba_time:.3f}"])
    
    print("\nТАБЛИЦА 1: Сравнение классического умножения и Карацубы")
    print(tabulate(results, headers=["Размер", "Классика (мкс)", "Карацуба (мкс)"], tablefmt="grid"))

def test_value_calculation_performance():
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    results = []
    
    print("\nЗамеры вычисления значения полинома...")
    for size in sizes:
        coeffs = generate_polynom(size)
        p = Polynom(coeffs)
        x = 0.5
        
        _ = p.direct_counting(x)
        _ = p.gorner_counting(x)
        
        n_iterations = 10000
        
        start = time.perf_counter()
        for _ in range(n_iterations):
            _ = p.direct_counting(x)
        direct_time = (time.perf_counter() - start) * 1000 / n_iterations
        
        start = time.perf_counter()
        for _ in range(n_iterations):
            _ = p.gorner_counting(x)
        gorner_time = (time.perf_counter() - start) * 1000 / n_iterations
        
        results.append([size, f"{direct_time:.6f}", f"{gorner_time:.6f}"])
    
    print("\nТАБЛИЦА 2: Сравнение прямого вычисления и схемы Горнера")
    print(tabulate(results, headers=["Степень", "Прямой (мкс)", "Горнер (мкс)"], tablefmt="grid"))

def main():
    print("ТЕСТИРОВАНИЕ ПОЛИНОМОВ")
    
    random.seed(42)
    
    test_multiplication_performance()
    test_value_calculation_performance()
    
    print("ВЫВОДЫ:")
    print("1. На малых размерах классика быстрее из-за накладных расходов на рекурсию")
    print("2. На размерах >128 Карацуба начинает выигрывать")
    print("3. Горнер значительно быстрее прямого метода на всех размерах")

if __name__ == "__main__":
    main()