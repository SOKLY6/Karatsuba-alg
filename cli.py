import questionary
from polynom_utils import Polynom, SlowPolynom, FastPolynom

def number_to_polynom(num_str: str) -> list[float]:
    return [float(d) for d in reversed(num_str)]

def polynom_to_number(poly: Polynom) -> str:
    digits = []
    carry = 0
    for coeff in poly.factors:
        val = coeff + carry
        digit = int(round(val)) % 10
        carry = int(round(val)) // 10
        digits.append(str(digit))
    while carry > 0:
        digits.append(str(carry % 10))
        carry //= 10
    while len(digits) > 1 and digits[-1] == '0':
        digits.pop()
    return ''.join(reversed(digits))

def cli():
    print("\nКАЛЬКУЛЯТОР ПОЛИНОМОВ\n")
    
    mode = questionary.select(
        "Выберите режим работы:",
        choices=[
            "1 - Прямое вычисление значения полинома",
            "2 - Вычисление по схеме Горнера",
            "3 - Классическое умножение полиномов",
            "4 - Умножение полиномов методом Карацубы",
            "5 - Умножение чисел (через полиномы)"
        ]
    ).ask()
    
    if mode.startswith("1"):
        print("\nПрямое вычисление значения полинома")
        coeffs_str = questionary.text("Введите коэффициенты полинома (начиная со старшей степени):").ask()
        coeffs = [float(c) for c in coeffs_str.split()]
        x = float(questionary.text("Введите x:").ask())
        
        p = Polynom(coeffs)
        result = p.direct_counting(x)
        print(f"\nРезультат: {result}")
        
    elif mode.startswith("2"):
        print("\nВычисление по схеме Горнера")
        coeffs_str = questionary.text("Введите коэффициенты полинома (начиная со старшей степени):").ask()
        coeffs = [float(c) for c in coeffs_str.split()]
        x = float(questionary.text("Введите x:").ask())
        
        p = Polynom(coeffs)
        result = p.gorner_counting(x)
        print(f"\nРезультат: {result}")
        
    elif mode.startswith("3"):
        print("\nКлассическое умножение полиномов")
        
        print("\nПервый полином:")
        coeffs1_str = questionary.text("Введите коэффициенты (начиная со старшей степени):").ask()
        coeffs1 = [float(c) for c in coeffs1_str.split()]
        
        print("\nВторой полином:")
        coeffs2_str = questionary.text("Введите коэффициенты (начиная со старшей степени):").ask()
        coeffs2 = [float(c) for c in coeffs2_str.split()]
        
        p1_slow = SlowPolynom(coeffs1)
        p2_slow = SlowPolynom(coeffs2)
        
        result = p1_slow * p2_slow
        
        print(f"\nРезультат: {result.factors}")
        
    elif mode.startswith("4"):
        print("\nУмножение полиномов методом Карацубы")
        
        print("\nПервый полином:")
        coeffs1_str = questionary.text("Введите коэффициенты (начиная со старшей степени):").ask()
        coeffs1 = [float(c) for c in coeffs1_str.split()]
        
        print("\nВторой полином:")
        coeffs2_str = questionary.text("Введите коэффициенты (начиная со старшей степени):").ask()
        coeffs2 = [float(c) for c in coeffs2_str.split()]
        
        p1_fast = FastPolynom(coeffs1)
        p2_fast = FastPolynom(coeffs2)
        
        result = p1_fast * p2_fast
        
        print(f"\nРезультат: {result.factors}")
            
    elif mode.startswith("5"):
        print("\nУмножение чисел (через полиномы)")
        
        num1 = questionary.text("Введите первое число:").ask().strip()
        num2 = questionary.text("Введите второе число:").ask().strip()
        
        coeffs1 = number_to_polynom(num1)
        coeffs2 = number_to_polynom(num2)
        
        p1 = FastPolynom(coeffs1)
        p2 = FastPolynom(coeffs2)
        
        result_poly = p1 * p2
        result = polynom_to_number(result_poly)
        expected = str(int(num1) * int(num2))
        
        print(f"\nРезультат: {result}")
        print(f"Ожидаемый результат: {expected}")
        
        if result == expected:
            print("Результаты совпадают")
        else:
            print("Ошибка в вычислениях!")

if __name__ == "__main__":
    cli()