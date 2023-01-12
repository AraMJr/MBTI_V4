from dataclasses import dataclass


@dataclass
class UI:
    main_line: str = 12*"><"
    main_menu: str = f"{main_line}\n|| MENU \n{main_line}\n"

    def interface(self, element: str) -> str:
        return str(input(getattr(self, element)))


def create_ui():
    return UI()


if __name__ == "__main__":
    ui = UI()
    user_input = ui.interface("main_menu")


