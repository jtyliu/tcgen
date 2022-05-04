from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def generate(self, case_num):
        pass

    def p(self, *args):
        self.output += " ".join(map(str, args))
        self.output += "\n"

    print = p

    def get_test_cases(self, N):
        ret = []
        for case_num in range(N):
            self.output = ""
            self.generate(case_num)
            ret.append(self.output)
        return ret

    def get_test_case(self):
        self.output = ""
        self.generate(1)
        return self.output
