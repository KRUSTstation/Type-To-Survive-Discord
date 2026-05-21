import discord

_registry: list[type[discord.ui.View]] = []

class PersistentView(discord.ui.View):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _registry.append(cls)

    def __init__(self):
        super().__init__(timeout=None)

def register_all(bot: discord.Client):
    for view_cls in _registry:
        bot.add_view(view_cls())