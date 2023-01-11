
class Function:

    def __init__(self, attrs, abbrevs):
        self.abbrevs: dict = abbrevs
        self.attrs: dict = attrs

    def get_fullname(self, abbrev: str) -> str | None:
        return self.attrs.get(abbrev)

    def get_abbrev(self, fullname: str) -> str | None:
        return self.abbrevs.get(fullname)

    def get_function(self, query: str) -> str | None:
        return

    def get_opposite(self, query: str) -> str | None:
        abbrevs = list(self.attrs.keys())
        attrs = list(self.abbrevs.keys())
        if query == abbrevs[0]:
            return abbrevs[1]
        elif query == abbrevs[1]:
            return abbrevs[0]
        elif query == attrs[0]:
            return attrs[1]
        elif query == attrs[1]:
            return attrs[0]
        else:
            return None


def instantiate(attribute1: str, abbrev1: str, attribute2: str, abbrev2: str) -> Function:
    return Function(attrs={abbrev1: attribute1, abbrev2: attribute2},
                    abbrevs={attribute1: abbrev1, attribute2: abbrev2})


if __name__ == '__main__':
    judging: Function = instantiate('thinking', 't', 'feeling', 'f')
    print(judging)
    print(judging.get_abbrev('thinking'))
    print(judging.get_fullname('t'))
    print(judging.get_opposite('t'))
    print(judging.get_opposite('thinking'))
    print(judging.get_opposite('intuition'))
    print(judging.get_fullname('n'))



