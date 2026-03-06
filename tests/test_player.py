from player import AdaptivePlayer, PlayStep


class FakeInput:
    def __init__(self) -> None:
        self.clicks = []
        self.typed = []

    def click(self, x: int, y: int, button: str = "left") -> None:
        self.clicks.append((x, y, button))

    def typewrite(self, text: str) -> None:
        self.typed.append(text)


class FakeLocator:
    def __init__(self, mapping: dict[str, tuple[int, int]]) -> None:
        self.mapping = mapping

    def find_by_text(self, text: str):
        return self.mapping.get(text)


def test_adaptive_player_prefers_text_target() -> None:
    input_backend = FakeInput()
    locator = FakeLocator({"Odeslat": (100, 200)})
    player = AdaptivePlayer(input_backend, locator)

    player.play([PlayStep(action="click", payload={"x": 1, "y": 2, "target_text": "Odeslat"})])

    assert input_backend.clicks == [(100, 200, "left")]


def test_adaptive_player_types_text() -> None:
    input_backend = FakeInput()
    locator = FakeLocator({})
    player = AdaptivePlayer(input_backend, locator)

    player.play([PlayStep(action="type", payload={"text": "Ahoj"})])

    assert input_backend.typed == ["Ahoj"]
