from typing import Any

class Polynom:
    def __init__(self, factors: list[float]) -> None:
        self.factors: list[float] = factors
        self.deg_polynom = len(factors) - 1

    def direct_counting(self, x: float) -> float:
        sum = 0
        for i in range(self.deg_polynom, -1, -1):
            sum += self.factors[self.deg_polynom - i] * x**i
        return sum

    def gorner_counting(self, x: float) -> float:
        sum = self.factors[0]
        for i in range(1, self.deg_polynom + 1):
            sum *= x
            sum += self.factors[i]
        return sum
    
    def __add__(self, other: 'Polynom') -> 'Polynom':
        if not isinstance(other, Polynom):
            return NotImplemented

        l1 = self.factors
        l2 = other.factors
        length = max(len(l1), len(l2))
        res_coeffs = [0.0] * length

        for i in range(length):
            v1 = l1[i] if i < len(l1) else 0.0
            v2 = l2[i] if i < len(l2) else 0.0
            res_coeffs[i] = v1 + v2

        return Polynom(res_coeffs)

    def __sub__(self, other: 'Polynom') -> 'Polynom':
        if not isinstance(other, Polynom):
            return NotImplemented

        l1 = self.factors
        l2 = other.factors
        length = max(len(l1), len(l2))
        res_coeffs = [0.0] * length

        for i in range(length):
            v1 = l1[i] if i < len(l1) else 0.0
            v2 = l2[i] if i < len(l2) else 0.0
            res_coeffs[i] = v1 - v2

        return Polynom(res_coeffs)
    


class SlowPolynom(Polynom):
    def __mul__(self, other: Any) -> Polynom:
        if not isinstance(other, Polynom):
            raise TypeError
        
        result_deg = self.deg_polynom + other.deg_polynom
        new_polynom_list = [0.0] * (result_deg + 1)
        
        for i in range(len(self.factors)):
            for j in range(len(other.factors)):
                new_polynom_list[i + j] += self.factors[i] * other.factors[j]
                
        return Polynom(new_polynom_list)


class FastPolynom(Polynom):
    def __mul__(self, other: Any) -> Polynom:
        if not isinstance(other, Polynom):
            raise TypeError
        
        return karatsuba_multiply(self, other)


def karatsuba_multiply(p1: Polynom, p2: Polynom) -> Polynom:
    factors1 = p1.factors.copy()
    factors2 = p2.factors.copy()
    
    while factors1 and abs(factors1[-1]) < 1e-10:
        factors1.pop()
    while factors2 and abs(factors2[-1]) < 1e-10:
        factors2.pop()
    
    n1 = len(factors1)
    n2 = len(factors2)
    
    if n1 == 0 or n2 == 0:
        return Polynom([0.0])
    
    if n1 <= 32 or n2 <= 32:
        result_deg = (n1 - 1) + (n2 - 1)
        result = [0.0] * (result_deg + 1)
        for i in range(n1):
            for j in range(n2):
                result[i + j] += factors1[i] * factors2[j]
        return Polynom(result)
    
    n = max(n1, n2)
    m = n // 2
    
    factors1_padded = factors1 + [0.0] * (n - n1)
    factors2_padded = factors2 + [0.0] * (n - n2)
    
    a0 = Polynom(factors1_padded[:m])
    a1 = Polynom(factors1_padded[m:])
    b0 = Polynom(factors2_padded[:m])
    b1 = Polynom(factors2_padded[m:])
    
    p0 = karatsuba_multiply(a0, b0)
    p2 = karatsuba_multiply(a1, b1)
    
    a0_plus_a1 = a0 + a1
    b0_plus_b1 = b0 + b1
    p1 = karatsuba_multiply(a0_plus_a1, b0_plus_b1)
    
    gamma = p1 - p0 - p2
    
    gamma_shifted = Polynom([0.0] * m + gamma.factors)
    p2_shifted = Polynom([0.0] * (2 * m) + p2.factors)
    
    result = p0 + gamma_shifted + p2_shifted
    
    return result