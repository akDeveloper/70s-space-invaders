from engine import Engine
from renderer import SdlRenderer
from game import LoadState


def main():
    renderer = SdlRenderer(224, 260, 672, 780)
    engine: Engine = Engine(renderer)
    engine.run(LoadState(renderer))


if __name__ == "__main__":
    main()
