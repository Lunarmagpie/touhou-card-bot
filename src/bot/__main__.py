import flare

import utils

bot = utils.Bot(utils.CONFIG.token)

flare.install(bot)

bot.plugins.load_folder("src.bot.plugins")

bot.run()
