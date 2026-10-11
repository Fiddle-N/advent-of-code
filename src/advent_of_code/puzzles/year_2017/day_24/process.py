from advent_of_code.common import read_file, timed_run


def parse(raw_components: str) -> list[tuple[int, int]]:
    components = []
    for component in raw_components.splitlines():
        port_0, port_1 = component.split("/")
        components.append((int(port_0), int(port_1)))
    return components


class BridgeBuild:
    def __init__(self):
        self._max_strength = 0
        self._max_depth_strength = (0, 0)

    def _build(
        self,
        components: list[tuple[int, int]],
        port: int = 0,
        strength: int = 0,
        depth: int = 1,
    ) -> None:
        for component in components:
            if port in component:
                new_components = components.copy()
                new_components.remove(component)

                component_list = list(component)
                component_list.remove(port)
                (other_port,) = component_list

                self._build(
                    components=new_components,
                    port=other_port,
                    strength=strength + sum(component),
                    depth=depth + 1,
                )
        if strength > self._max_strength:
            self._max_strength = strength
        if depth > self._max_depth_strength[0] or (
            depth == self._max_depth_strength[0]
            and strength > self._max_depth_strength[1]
        ):
            self._max_depth_strength = (depth, strength)

    def build(self, components: list[tuple[int, int]]) -> tuple[int, int]:
        self._build(components)
        return (self._max_strength, self._max_depth_strength[1])


def run():
    raw_components = read_file()
    components = parse(raw_components)
    builder = BridgeBuild()
    print(builder.build(components))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
