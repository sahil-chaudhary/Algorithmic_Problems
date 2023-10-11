def generate_gray_code(n):
    # Base case: Gray code for n=1
    if n == 1:
        return ['0', '1']
    
    # Recursive case: Generate Gray code for n-1
    gray_code_n_minus_1 = generate_gray_code(n - 1)
    
    # Reflect and add 0's and 1's
    gray_code_n = []
    for code in gray_code_n_minus_1:
        gray_code_n.append('0' + code)
    for code in reversed(gray_code_n_minus_1):
        gray_code_n.append('1' + code)
    
    return gray_code_n

# Example usage:
n = 3 
gray_code = generate_gray_code(n)
for code in gray_code:
    print(code)
