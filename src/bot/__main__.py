import utils

bot = utils.Bot()

bot.plugins.load_folder("src.bot.plugins")

bot.run()
