import time
import math
import os.path
import sys

class fraction():
    def __init__(self, num, den):
        self.num = num
        self.den = den
    
    def __add__(self, other):
        ret_frac = fraction(self.num * other.den + self.den * other.num, self.den * other.den)
        ret_frac.deduct()
        return ret_frac
    
    def __sub__(self, other):
        ret_frac = fraction(self.num * other.den - self.den * other.num, self.den * other.den)
        ret_frac.deduct()
        return ret_frac
    
    def __isub__(self, other):
        ret_frac = fraction(self.num * other.den - self.den * other.num, self.den * other.den)
        ret_frac.deduct()
        return ret_frac
    
    def __mul__(self, other):
        #print("mul")
        #print("%s %s %s %s" % (type(self.num), type(self.den), type(other.num), type(other.den)))
        ret_frac = fraction(self.num * other.num, self.den * other.den)
        ret_frac.deduct()
        return ret_frac.fix_frac()
    
    def __imul__(self, other):
        ret_frac = fraction(self.num * other.num, self.den * other.den)
        ret_frac.deduct()
        return ret_frac.fix_frac()
    
    def __truediv__(self, other):
        ret_frac = fraction(self.num * other.den, self.den * other.num)
        ret_frac.deduct()
        return ret_frac.fix_frac()
    
    def __itruediv__(self, other):
        ret_frac = fraction(self.num * other.den, self.den * other.num)
        ret_frac.deduct()
        return ret_frac.fix_frac()
    
    def __neg__(self):
        return fraction(-self.num, self.den)
    
    def __repr__(self):
        if self.num % self.den == 0:
            return "%+d" % (self.num // self.den)
        else:
            if self.num < 0:
                return "-(%d/%d)" % (-self.num, self.den)
            else:
                return "+(%d/%d)" % (self.num, self.den)
        #return "<fraction num:%s den:%s>" % (self.num, self.den)
    
    def __str__(self):
        if self.num % self.den == 0:
            return "%+d" % (self.num // self.den)
        else:
            if self.num < 0:
                return "-(%d/%d)" % (-self.num, self.den)
            else:
                return "+(%d/%d)" % (self.num, self.den)

    def reciprocal_fraction(self):
        return fraction(self.den, self.num)

    def fix_frac(self):
        if self.den < 0:
            self.num *= -1
            self.den *= -1
        return self

    def deduct(self):
        g = math.gcd(self.num, self.den)
        self.num //= g
        self.den //= g
        return self.fix_frac()


def def_filename():
    filename = 'input.txt'
    return filename


def error_handle(error_code, line = 0):
    filename = def_filename()
    line = str(line)
    messages = [
        filename + " does not exists.",
        "Nothing is written in " + filename + ".",
        "Number of coefficient written in " + filename + " is wrong in line : " + line,
        "Please write characters of only ([0-9]|-|/|.) in " + filename + ". (line : " +  line + ")",
        "Only integers are valid as numelator or denometor, line : " + line,
        "'/' appears more than two times at somewhere of line " + line,
        "This Simultaneous Equation has no solutions."
    ]

    print("[ ! ] " + messages[error_code])
    print("[ ! ] Press Ctrl + C .")

    while True:
        pass


def get_all_of_file(filename):
    if not os.path.exists(filename):
        error_handle(0, filename)
    f = open(filename, 'r')
    all_list = f.readlines()
    if all_list == []:
        error_handle(1, filename)

    f.close()
    return all_list


def get_elements(all_line):
    elements = []
    for line in all_line:
        line_split = line.split()
        elements.append(line_split)
        if not len(elements[0]) == len(line_split):
            error_handle(2, len(elements))
    
    return elements


def string_float_to_fraction(sf: str):
    place_of_dot = sf.find('.')
    length = len(sf)

    sd = int(sf.replace('.', ''))
    
    ret_frac = fraction(sd, 10 ** (length - place_of_dot - 1))
    ret_frac.deduct()

    return ret_frac


def elements_to_fraction(elements):
    line_num = 0
    fraction_lines = []
    
    for element_line in elements:
        fraction_line = []
        for element in element_line:
            #insert validation of char here.

            if element.count('/'):
                if element.count('.'):
                    error_handle(4, line_num)
                if not element.count('/') == 1:
                    error_handle(5, line_num)
                frac_elem = element.split('/')
                frac = fraction(int(frac_elem[0]), int(frac_elem[1]))
                fraction_line.append(frac)
            elif element.count('.'):
                frac = string_float_to_fraction(element)
                fraction_line.append(frac)
            else:
                fraction_line.append(fraction(int(element), 1))
        line_num += 1
        fraction_lines.append(fraction_line)

    return fraction_lines


def deduction_frac_line(frac_line):
    if is_zero_filled_equation(frac_line):
        return frac_line

    length = len(frac_line)
    num_den_line = []
    num_line = []
    den_line = []
    div_num_den = []

    for f in frac_line:
        num_line.append(f.num)
        den_line.append(f.den)
    num_den_line.append(num_line)
    num_den_line.append(den_line)
    
    for i in range(2):
        while True:
            #print(num_den_line)
            if num_den_line[i].count(0) == length - 1:
                break
            
            for j in range(length):
                #print("passed")
                if not num_den_line[i][j] == 0:
                    start_index = j
                    break

            min = num_den_line[i][start_index]
            
            #find smallest number from num or den.
            for num_or_den in num_den_line[i][start_index:]:
                #remove value 0
                if num_or_den == 0:
                    continue
                if abs(min) > abs(num_or_den):
                    min = num_or_den
            min_index = num_den_line[i].index(min)
            
            # do % min for all num or den
            for j in range(length):
                if j == min_index:
                    continue
                num_den_line[i][j] %= min

        #find GCD of num or den
        for nonzero_index in range(length):
            if not num_den_line[i][nonzero_index] == 0:
                break
        div_num_den.append(num_den_line[i][nonzero_index])
    
    div_frac = fraction(div_num_den[0], div_num_den[1])
    for i in range(length):
        frac_line[i] /= div_frac

    return frac_line


def is_zero_filled_equation(fraction_line):
    row = len(fraction_line)
    
    for i in range(row):
        if not fraction_line[i].num == 0:
            break
        if i == row - 1:
            return True
    
    return False


# swap equation
# fm .... fraction_matrix
# vol ... var_order_list
def swap_line(fm, swap_from, swap_to):
    # variant name is so long ... :(
    fm[swap_from], fm[swap_to] = fm[swap_to], fm[swap_from] 
    """
    tmp = fraction_matrix[swap_to]
    fraction_matrix[swap_to] = fraction_matrix[swap_from]
    fraction_matrix[swap_from] = tmp
    """
    return fm


# swap variant
# fm .... fraction_matrix
# vol ... var_order_list
def swap_row(fm, swap_from, swap_to, vol):
    line = len(fm) 

    for i in range(line):
        fm[i][swap_from], fm[i][swap_to] = fm[i][swap_to], fm[i][swap_from]
    
    vol[swap_from], vol[swap_to] = vol[swap_to], vol[swap_from]
    return fm, vol


def make_diagonal_element_nonzero(fraction_matrix, var_order_list):
    line = len(fraction_matrix)
    row = len(fraction_matrix[0])

    for line_index in range(line):
        if fraction_matrix[line_index][line_index].num == 0:
            for i in range(line_index, line):
                swap_line(fraction_matrix, line_index, i)
                if fraction_matrix[line_index][line_index].num != 0:
                    break
                
                if i == line - 1:
                    for i in range(line_index, row - 1):
                        swap_row(fraction_matrix, line_index, i, var_order_list)
                        if fraction_matrix[line_index][line_index].num != 0:
                            break
                            
                    # failed to swap line and row
                    if fraction_matrix[line - 1][row - 1].num != 0 and str(fraction_matrix[line - 1]).count("+0") == row - 1:
                        error_handle(6)
                    break

    return fraction_matrix, var_order_list


def make_fundamental_matrix(fraction_matrix, var_order_list):
    row = len(fraction_matrix[0])
    line = len(fraction_matrix)
    
    for line_index, fraction_line in enumerate(fraction_matrix):
        if is_zero_filled_equation(fraction_line):
            continue

        # make diagonal element non-zero
        fraction_matrix, var_order_list = make_diagonal_element_nonzero(fraction_matrix, var_order_list)
        
        # plus an equation to target equation
        for target_line_index, target_fraction_line in enumerate(fraction_matrix):
            
            if is_zero_filled_equation(target_fraction_line):
                continue
            if line_index == target_line_index:
                continue

            # make 0 for same variant position of other fraction-line
            mul_frac = fraction_matrix[target_line_index][line_index] / fraction_matrix[line_index][line_index]
            for i in range(row):
                # delete zero-filled equations
                fraction_matrix[target_line_index][i] -= (fraction_matrix[line_index][i] * mul_frac)
            
            # deduction for an equation
            fraction_matrix[target_line_index] = deduction_frac_line(fraction_matrix[target_line_index])
    
    # delete zero-filled equations
    for i in range(line)[::-1]:
        if is_zero_filled_equation(fraction_matrix[i]):
            del fraction_matrix[i]
            line -= 1

    # make diagonal elements 1/1
    for i in range(line):
        reciprocal = fraction_matrix[i][i].reciprocal_fraction()

        for j in range(row):
            fraction_matrix[i][j] *= reciprocal

    return fraction_matrix, var_order_list


def print_equations(fraction_matrix):
    row = len(fraction_matrix[0])
    line = len(fraction_matrix)

    print("[ + ] This program will solve next equations.\n")

    for i in range(line):
        sys.stdout.write('{ ')
        for j in range(row):
            if j == row - 1:
                sys.stdout.write(' = ' + str(fraction_matrix[i][j])[1:])
            else:
                if j == 0:
                    sys.stdout.write(str(fraction_matrix[i][j])[1:])
                else:
                    sys.stdout.write(str(fraction_matrix[i][j]))
                sys.stdout.write(chr(ord('A') + j))
        sys.stdout.write('\n')
    sys.stdout.write('\n')


def print_solution(fraction_matrix, var_order_line):

    #there is no meaningful equation.
    if fraction_matrix == []:
        error_handle(6)

    row = len(fraction_matrix[0])
    line = len(fraction_matrix)

    if line >= row:
        error_handle(6)

    describe_count = 0
    normal_count = 0
    def_var_count = 0

    print("[ + ] The Simultaneous equations are solved.")
    print("[ + ] Solutions are listed below.\n")

    # repeat for lines (A=, B=, ...)
    for i in range(row - 1):
        describe_count = 0
        sys.stdout.write("%s = " % chr(ord('A') + i))

        var_index = var_order_line.index(i)

        if 0 <= var_index < line:

            for frac_index, frac in enumerate(fraction_matrix[normal_count][line:row-1]):
                if frac.num == 0:
                    continue
                
                if abs(frac.num) != abs(frac.den):
                    if describe_count == 0 and -frac.num >= 0:
                        sys.stdout.write(str(-frac)[1:])
                    else:
                        sys.stdout.write(str(-frac))
                else:
                    if describe_count != 0 or -frac.num < 0:
                        sys.stdout.write(str(-frac)[0])
                        
                sys.stdout.write(chr(ord('a') + frac_index))

                describe_count += 1

            last_frac = fraction_matrix[normal_count][row - 1]
            if last_frac.num != 0:
                if describe_count == 0 and last_frac.num >= 0:
                    sys.stdout.write(str(last_frac)[1:])
                else:
                    sys.stdout.write(str(last_frac))
            else:
                if describe_count == 0:
                    sys.stdout.write('0')
            
            normal_count += 1

        elif line <= var_index < row - 1:
            
            sys.stdout.write(chr(ord('a') + def_var_count))
            def_var_count += 1

        else:
            error_handle(6)

        sys.stdout.write("\n")
    
    if def_var_count > 0:
        if def_var_count == 1:
            sys.stdout.write("( 'a' is a real number. )\n")
        else:
            sys.stdout.write('( ')
            for i in range(def_var_count - 1):
                sys.stdout.write(chr(ord('a') + i) + ', ')
            sys.stdout.write("and %s are real numbers independent each other. )\n" % chr(ord('a') + def_var_count - 1))
    sys.stdout.write('\n')
    

def main():
    start_time = time.time()

    # read everything from input file
    filename = def_filename()
    all_line = get_all_of_file(filename)
    print("[ + ] Reading elements from %s is completed." % filename)

    # extract elements from text
    all_elements = get_elements(all_line)

    # construct matrix of equations
    fraction_matrix = elements_to_fraction(all_elements)

    #print equations
    print_equations(fraction_matrix)
    print("[ + ] Solving equations, please wait...")

    # manage variants' order for swap positions of variants.
    var_order_list = list(range(len(fraction_matrix[0])))

    # make fundamental_matrix from fraction_matrix 
    fraction_matrix, var_order_list = make_fundamental_matrix(fraction_matrix, var_order_list)

    end_time = time.time()

    print_solution(fraction_matrix, var_order_list)
    print("[ + ] Solving took %f[sec]." % (end_time - start_time))
    input("[ + ] Press Enter to exit.")


if __name__=="__main__":
    main()
