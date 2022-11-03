import utils
import flare
import cards.card

bot = utils.Bot(utils.CONFIG.token)

flare.install(bot)

bot.plugins.load_folder("src.bot.plugins")

bot.run()
