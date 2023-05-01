from dataclasses import dataclass
from mbti_logic.function_old import Function, function


# this class contains all relevant the information on a type, including the function stack (and shadow), as well as
# it's short name, and the four Functions it can be. each function is populated automatically on instantiation, but
# must be activated manually. name is the only required argument.
@dataclass
class MBTI:
    name: str | None
    version: Function = function('introverted', 'extroverted', 'i', 'e')
    perceiving: Function = function('intuition', 'sensing', 'n', 's')
    judging: Function = function('thinking', 'feeling', 't', 'f')
    orientation: Function = function('judging', 'perceiving', 'j', 'p')
    stack: dict = None
    shadow: dict = None

    def __str__(self):
        fullnames = list(self.get_fullnames().values())
        return f"\n{self.name.upper()}\t->\t[ {self.version.active.fullname} {self.perceiving.active.fullname} " \
               f"{self.judging.active.fullname} {self.orientation.active.fullname} ]\n" \
               f"stack\t->\t[ {' > '.join(fullnames[:4])} ]\n" \
               f"shadow\t->\t[ {' > '.join(fullnames[4:])} ]\n"

    def set_name(self, name) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    # returns true if the inputted strings are all Attributes in their associated Functions, otherwise returns false
    def validate(self, v: str = None, p: str = None, j: str = None, o: str = None) -> bool:
        def sub_validate(query: str, function: Function) -> bool:
            if query is not None and query not in function.get_abbrevs():
                return False
            return True

        return sub_validate(v, self.version) and sub_validate(p, self.perceiving) and sub_validate(j, self.judging) \
            and sub_validate(o, self.orientation)

    # activates all Functions according to the short name
    def activate(self) -> bool:
        # python wizardry to split a string so that each character is assigned to each of the four variables
        v, p, j, o = tuple([*self.name])
        if self.validate(v, p, j, o):
            self.version.set_active(v)
            self.perceiving.set_active(p)
            self.judging.set_active(j)
            self.orientation.set_active(o)
            return True
        else:
            print("ERROR: INVALID TYPE DETECTED")
            return False

    # generates the full function stack (including shadow) based on the active Functions
    def generate_stack(self) -> bool:
        top_e_function = getattr(self, self.orientation.active.fullname).active.abbrev + 'e'
        top_i_function = getattr(self, self.orientation.get_opposite().fullname).active.abbrev + 'i'
        bottom_e_function = getattr(self, self.orientation.get_opposite().fullname).get_opposite().abbrev + 'e'
        bottom_i_function = getattr(self, self.orientation.active.fullname).get_opposite().abbrev + 'i'
        stacks = {
            "i": {1: top_i_function, 2: top_e_function, 3: bottom_i_function, 4: bottom_e_function},
            "e": {1: top_e_function, 2: top_i_function, 3: bottom_e_function, 4: bottom_i_function}
        }
        self.stack = stacks.get(self.version.active.abbrev)
        self.shadow = stacks.get(self.version.get_opposite().abbrev)
        if self.stack is None:
            return False
        return True

    # alternative way to access shadow functions. built using the current stack
    def generate_shadow(self) -> bool:
        if self.stack is None:
            return False
        shadow = {}
        current_version = self.version.active.abbrev
        for key, value in self.stack.items():
            current_version = self.version.find_opposite(current_version).abbrev
            shadow[key + 4] = value[:-1] + current_version
        self.shadow = shadow
        return True

    # convert the stack from abbreviations to full function names using a reference key. can optionally not include the
    # shadow stack, but will include it by default
    def get_fullnames(self, full: bool = True) -> dict:
        def convert_abbrev(stack: dict, new_stack: dict = {}) -> dict:
            reference = {
                'i': 'introverted',
                'e': 'extroverted',
                'n': 'intuition',
                's': 'sensing',
                't': 'thinking',
                'f': 'feeling',
                'p': 'perceiving',
                'j': 'judging'
            }
            for key, function in stack.items():
                f, v = tuple([*function])
                new_stack[key] = f"{reference.get(v)} {reference.get(f)}"
            return new_stack

        full_stack = convert_abbrev(self.stack)
        if full:
            return convert_abbrev(self.shadow, full_stack)
        return full_stack


# change an mbti's type, and therefore stack using this. requires an instance of the mbti to change, and an optional
# new name to base the change off of. can also be used to deactivate an mbti Functions if None or no name field is
# passed in.
def update_type(mbti: MBTI, name: str = None) -> MBTI | None:
    cached_mbti: MBTI = mbti
    mbti.set_name(name)
    mbti.version.set_active(None)
    mbti.perceiving.set_active(None)
    mbti.judging.set_active(None)
    mbti.orientation.set_active(None)
    if name is None:
        mbti.stack = None
        mbti.shadow = None
        return mbti
    if mbti.activate() and mbti.generate_stack() and mbti.generate_shadow():
        return mbti
    return cached_mbti


# used to create an instance of a MBTI class. if no name is passed in, it will create a mbti with deactivated
# functions and no stacks
def mbti_type(name: str = None) -> MBTI | None:
    if name is None:
        mbti = MBTI(name=None)
        return mbti
    if len(name) != 4:
        print("ERROR: INVALID TYPE NAME LENGTH")
        return
    mbti = MBTI(name=name)
    if mbti.activate() and mbti.generate_stack() and mbti.generate_shadow():
        return mbti
    return None


if __name__ == "__main__":
    def print_type(type: MBTI) -> None:
        if type is not None:
            print(type)
    intp = mbti_type('intp')
    print_type(intp)
    update_type(intp, "esfp")
    print_type(intp)
    update_type(intp, "abcd")
    print_type(intp)
