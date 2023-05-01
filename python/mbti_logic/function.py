from dataclasses import dataclass
from functools import singledispatchmethod


@dataclass
class Attribute:
    fullname: str
    abbrev: str

    def match(self, query: str) -> bool:
        if self.fullname == query or (self.abbrev == query and self.abbrev is not None):
            return True
        return False


@dataclass(order=True)
class Function:
    active: Attribute
    inactive: Attribute

    def get_active(self) -> Attribute:
        return self.active

    def get_inactive(self) -> Attribute:
        return self.inactive

    # returns both active and inactive attributes, sorted by fullname
    def get_attrs(self) -> list[Attribute]:
        attrs: list[Attribute] = [self.active, self.inactive]
        attrs.sort(key=lambda x: x.fullname)
        return attrs

    # returns the abbreviations for all possible Attributes the Function can actively be, sorted by fullname
    def get_abbrevs(self) -> list[str]:
        abbrevs = []
        attrs = self.get_attrs()
        for attr in attrs:
            abbrevs.append(attr.abbrev)
        return abbrevs

    # returns the fullnames for all possible Attributes the Function can actively be, sorted by fullname
    def get_fullnames(self) -> list[str]:
        fullnames = []
        attrs = self.get_attrs()
        for attr in attrs:
            fullnames.append(attr.fullname)
        return fullnames

    # switches active and inactive attributes
    def toggle(self) -> None:
        self.active, self.inactive = self.inactive, self.active

    # activates the attribute with the matching attr, and returns False if it had to toggle, and True if it did not

    @singledispatchmethod
    def activate(self, attr):
        raise TypeError(f"type [{type(attr)}] not supported for method [activate]")

    @activate.register
    def _(self, attr: str) -> bool:
        if self.inactive.match(attr):
            self.toggle()
            return False
        return True

    @activate.register
    def _(self, attr: Attribute) -> bool:
        return self.activate(attr.fullname)


def function(active: str, inactive: str, active_abbrev: str = None, inactive_abbrev: str = None):
    return Function(active=Attribute(fullname=active, abbrev=active_abbrev),
                    inactive=Attribute(fullname=inactive, abbrev=inactive_abbrev))


if __name__ == "__main__":
    judging = function("thinking", "feeling", "t", "f")
    print(judging)
    judging.activate("thinking")
    print(judging.active)
    print(judging.inactive)
    judging.toggle()
    print(judging.active)

