import crescent


class Bot(crescent.Bot):
    ...


class Context(crescent.Context):
    app: Bot


class Plugin(crescent.Plugin):
    def app(self) -> Bot:
        return super().app
