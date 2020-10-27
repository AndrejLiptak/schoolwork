import math


class ComplexNumber:
    def __init__(self, real=0, imaginary=0):
        self.real = real
        self.imaginary = imaginary

    def re(self):
        return self.real

    def im(self):
        return self.imaginary

    def size(self):
        return math.sqrt(self.re() ** 2 + self.im() ** 2)


def sub(first, second):
    res = ComplexNumber(first.re() - second.re(), first.im() - second.im())
    return res
