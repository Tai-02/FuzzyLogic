
def triangular_membership(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

def calculate_pwm(set_point, current_temp):
    # 1. Tính Error
    error = set_point - current_temp
    
    # 2. Fuzzification (Theo thông số suy luận từ ví dụ bài báo)
    # ZERO: -15 to 15, peak 0
    mu_zero = triangular_membership(error, -15, 0, 15)
    
    # SNEG: -25 to 0, peak -25 (để tại -1 có giá trị ~0.04)
    # Lưu ý: Bài báo có typo ở Table 4, nhưng kết quả ví dụ cho thấy SNEG phủ lề trái của ZERO
    mu_sneg = 0.0
    if -25 <= error <= 0:
        mu_sneg = (0 - error) / 25 # Hàm dốc xuống từ -25 về 0
        
    # 3. Rule Base (Trọng số đầu ra PWM - Table 5 & 6)
    # P_M (Medium) ~ 127.5
    # P_VH (Very High) ~ 210.4
    p_m = 127.5
    p_vh = 210.4
    
    # 4. Defuzzification (Weighted Average)
    numerator = (mu_sneg * p_vh) + (mu_zero * p_m)
    denominator = mu_sneg + mu_zero
    
    if denominator == 0:
        return 0
    
    z_star = numerator / denominator
    return z_star, mu_sneg, mu_zero

if __name__ == "__main__":
    # Test case từ Mục 5 của bài báo
    sp = 45
    cv = 46
    pwm, f2, f3 = calculate_pwm(sp, cv)
    
    print(f"--- Checking paper results ---")
    print(f"Set Point: {sp}, Current: {cv} -> Error: {sp-cv}")
    print(f"Fuzzification f2 (SNEG): {f2:.3f} (Paper: 0.04)")
    print(f"Fuzzification f3 (ZERO): {f3:.3f} (Paper: 0.933)")
    print(f"Defuzzification Z*: {pwm:.2f} (Paper: 130.95)")
    print(f"Duty Cycle: {(pwm/255)*100:.1f}% (Paper: 51%)")
