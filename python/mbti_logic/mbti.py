from dataclasses import dataclass
from mbti_logic.function import Function, function


@dataclass
class MBTI:
    name: str | None
    version: Function = function(active="introversion", active_abbrev="i", inactive="extroversion", inactive_abbrev="e")
    perceiving: Function = function(active="intuition", active_abbrev="n", inactive="sensing", inactive_abbrev="s")
    judging: Function = function(active="thinking", active_abbrev="t", inactive="feeling", inactive_abbrev="f")
    orientation: Function = function(active="judging", active_abbrev="j", inactive="perceiving", inactive_abbrev="p")
    stack: list = None

    def __str__(self):
        if self.name is None:
            return ""
        return f"\n{self.name.upper()}\t->\t[ {self.version.active.fullname} {self.perceiving.active.fullname} " \
               f"{self.judging.active.fullname} {self.orientation.active.fullname} ]\n"  \
               f"stack\t->\t[ {' > '.join(self.stack[:4])} ]\n"  \
               f"shadow\t->\t[ {' > '.join(self.stack[4:])} ]"

    def valid(self) -> bool:
        if self.name is None:
            return False

        def validate(query: str, function: Function) -> bool:
            if query is not None and query not in function.get_abbrevs():
                return False
            return True

        v, p, j, o = tuple([*self.name])
        return validate(v, self.version) and validate(p, self.perceiving) and validate(j, self.judging) and \
               validate(o, self.orientation)

    def activate(self):
        try:
            v, p, j, o = tuple([*self.name])
            self.version.activate(v)
            self.perceiving.activate(p)
            self.judging.activate(j)
            self.orientation.activate(o)
            return True
        except:
            return False

    def generate_stack(self) -> bool:
        active_version = self.version.active.abbrev
        inactive_version = self.version.inactive.abbrev
        driver = getattr(self, self.orientation.active.fullname).active.abbrev
        passenger = getattr(self, self.orientation.inactive.fullname).active.abbrev
        child = getattr(self, self.orientation.inactive.fullname).inactive.abbrev
        infant = getattr(self, self.orientation.active.fullname).inactive.abbrev
        self.stack = [driver + active_version, passenger + inactive_version, child + active_version,
                      infant + inactive_version, driver + inactive_version, passenger + active_version,
                      child + inactive_version, infant + active_version]
        if self.stack is None:
            return False
        return True


def mbti(name: str, mbti: MBTI | None = None) -> MBTI | None:
    if len(name) == 4 and name is not None:
        if mbti is not None:
            new_mbti = mbti
            new_mbti.name = name
        else:
            new_mbti: MBTI = MBTI(name=name)
        if new_mbti.valid() and new_mbti.activate() and new_mbti.generate_stack():
            return new_mbti
    print(f"{name} is not a valid mbti type")


if __name__ == "__main__":
    def print_type(type: MBTI | None = None) -> None:
        if type is not None:
            print(type)
    test = mbti("intp")
    print_type(test)
    test = mbti("isfj", test)
    print_type(test)
    test = mbti("estp", test)
    print_type(test)

