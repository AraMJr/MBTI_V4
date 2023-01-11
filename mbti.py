from dataclasses import dataclass
import function


class MBTI:

    def __init__(self, name):
        self.name: str = name
        self.functions: dict | None = None
        self.stack: dict | None = None
        self.version: function.Function = function.instantiate('introversion', 'i', 'extroversion', 'e')
        self.perceiving: function.Function = function.instantiate('intuition', 'n', 'sensing', 's')
        self.judging: function.Function = function.instantiate('thinking', 't', 'feeling', 'f')
        self.orientation: function.Function = function.instantiate('judging', 'j', 'perceiving', 'p')
        self.populate_functions()
        self.generate_stack()

    def __str__(self):
        return f"{self.name} -> {list(self.functions.values())}\n{self.stack}"

    def populate_functions(self):
        if self.functions is None:
            self.functions = {}
        v, p, j, o = tuple([*self.name])
        self.functions['v'] = self.version.get_fullname(v)
        self.functions['p'] = self.perceiving.get_fullname(p)
        self.functions['j'] = self.judging.get_fullname(j)
        self.functions['o'] = self.orientation.get_fullname(o)

    def generate_stack(self):
        if self.stack is None:
            self.stack = {}


def mbti_type(name: str) -> MBTI | None:
    if len(name) != 4:
        print('ERROR: INVALID TYPE (LEN NOT EQUAL TO 4)')
        return
    return MBTI(name=name)


if __name__ == "__main__":
    intp = mbti_type("intp")
    if intp is not None:
        print(intp)

