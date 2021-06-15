from tcgen import *


class Gen_Smt(Generator):
    def generate(self, case_num):
        v = Integer(5, 10)
        self.p(v)
        self.p(Array(v))


print(Gen_Smt().generate_test_cases(5))