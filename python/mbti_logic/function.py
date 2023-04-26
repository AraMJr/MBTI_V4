from dataclasses import dataclass


# An Attribute is a subset of a Function, and has a name and abbreviation.
@dataclass
class Attribute:
    abbrev: str
    fullname: str

    # returns true if a query is equal to either the abbreviation or fullname of the Attribute, otherwise returns false.
    def match(self, query: str) -> bool:
        if self.fullname == query or (self.abbrev == query and self.abbrev is not None):
            return True
        return False


# A Function acts as a variable which can only be certain Attributes, or None. The attrs are the Attributes it can be,
# and the active is the Attribute it currently is. a Function being activated means that it now has a "value". A
# deactivated Function (for all tense and purposes) returns None when asking for its value.
@dataclass
class Function:
    attrs: list[Attribute]
    active: Attribute | None = None

    # returns the abbreviations for all possible Attributes the Function can actively be
    def get_abbrevs(self) -> list[str]:
        abbrevs = []
        for attr in self.attrs:
            abbrevs.append(attr.abbrev)
        return abbrevs

    def get_full_names(self) -> list[str]:
        fullnames = []
        for attr in self.attrs:
            fullnames.append(attr.fullname)
        return fullnames

    # selects an Attribute from attrs to make active based on a match to a query string argument.
    # If no match is found, it returns None. if query is None, then it deactivates the Function and returns None.
    # the Function can still be reactivated later.
    def set_active(self, query: str = None) -> Attribute | None:
        if query is None:
            self.active = None
            return None
        for attr in self.attrs:
            if attr.match(query):
                self.active = attr
                return self.active

    # returns the first Attribute in attrs that is not activated. best used when attrs has a length of 2, as it does in
    # this program
    def get_opposite(self) -> Attribute | None:
        for attr in self.attrs:
            if attr is not self.active:
                return attr

    # returns the first Attribute in attrs that does not match the inputted query. if None are found, returns None.
    def find_opposite(self, query: str) -> Attribute | None:
        for attr in self.attrs:
            if not attr.match(query):
                return attr

    # sets the active Attribute to the opposite Attribute (first Attribute which is not the currently active Attribute).
    def flip(self) -> Attribute | None:
        self.active = self.get_opposite()
        return self.active


# used to instantiate an instance of the Function class. can optionally make an attribute active on initialization.
def function(attribute1: str, attribute2: str, abbrev1: str = None, abbrev2: str = None, active: str = None) \
        -> Function:
    attrs = [Attribute(abbrev=abbrev1, fullname=attribute1), Attribute(abbrev=abbrev2, fullname=attribute2)]
    for attr in attrs:
        if active is not None and attr.match(active):
            active = attr
    return Function(
        attrs=[Attribute(abbrev=abbrev1, fullname=attribute1), Attribute(abbrev=abbrev2, fullname=attribute2)],
        active=active)


if __name__ == "__main__":
    judging = function("thinking", "feeling", "t", "f")
    print(judging)
    judging.set_active("thinking")
    print(judging.active)
    print(judging.get_opposite())
    print(judging.find_opposite("t"))
    judging.flip()
    print(judging.active)

