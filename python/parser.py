from dataclasses import dataclass
from ui import UI, create_ui


@dataclass
class Parser:
    ui: UI = create_ui()


if __name__ == "__main__":
    pass

