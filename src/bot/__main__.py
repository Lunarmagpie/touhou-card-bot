import utils

bot = utils.Bot(utils.CONFIG.token)

bot.plugins.load_folder("src.bot.plugins")

bot.run()
