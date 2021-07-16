import sys
from fotorg.application import Application


def start_application() -> Application:
    app = Application()
    return app  # will return the application without starting the main loop.


def main() -> bool:
    return True


def init(test_mode: bool = False):
    if __name__ == '__main__':
        if not test_mode:
            start_application().mainloop()
        sys.exit(main())


init()
