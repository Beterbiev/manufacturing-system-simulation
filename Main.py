from Sample import *
from PseudoRandomGenerator import *
from RandomVariables import *
from ManufacturingSystem import *

class Main:

    def main():
        r1 = PseudoRandomGenerator(16, 13, 10)
        
        print('m: ', r1.get_m())
        print('xo: ', r1.get_xo())
        print('a: ', r1.get_a())

        ri1 = Sample(r1.congruential_method())

        rv1 = RandomVariables(ri1.get_sample())
        breakdown_time = rv1.exp(8)

        #---------------------------------------

        r2 = PseudoRandomGenerator(16, 9, 5)
        
        print('m: ', r2.get_m())
        print('xo: ', r2.get_xo())
        print('a: ', r2.get_a())

        ri2 = Sample(r2.congruential_method())

        rv2 = RandomVariables(ri2.get_sample())
        repair_time = rv2.exp(2)

        
        simulation = ManufacturingSystem(800, 10, 3, breakdown_time, repair_time)
        simulation.simulate()

    if __name__ == "__main__":
        main()
