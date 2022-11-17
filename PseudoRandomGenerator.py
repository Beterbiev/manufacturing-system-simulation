class PseudoRandomGenerator:

    def __init__(self, b, xo, t):
        self.m = 2 ** b
        self.xo = xo
        self.a = 8 * t - 3

    def get_m(self):
        return self.m

    def get_xo(self):
        return self.xo

    def get_a(self):
        return self.a

    def congruential_method(self):
        #Se crea una lista para almacenar los numeros generados
        r = []
        
        #auxiliar
        x1 = self.xo

        #ciclo do while
        x1 = (self.a * x1) % self.m
        ri = x1 / (self.m - 1)
        ri = "{:f}".format(ri)
        r.append(ri)
        while(x1 != self.xo):
            x1 = (self.a * x1) % self.m
            ri = x1 / (self.m - 1)
            ri = "{:f}".format(ri)
            r.append(ri)

        #se imprime toda la lista con un salto de linea entre valores
        #print(*r, sep = "\n")

        #se imprime el tamaño de la lista
        print("Número de iteraciones del generador: " + str(len(r)))
        if len(r) == (self.m / 4):
            print("Ciclo completo")
        else:
            print("Ciclo incompleto")

        return r