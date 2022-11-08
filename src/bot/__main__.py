import crescent
import flare
import hikari

import db
import utils

bot = utils.Bot()

flare.install(bot)


@bot.include
@crescent.event
async def on_starting(_: hikari.StartingEvent) -> None:
    bot._db = db.Database(migrations_folder="migrations")

    await bot._db.connect(
        host=utils.CONFIG.db_host,
        database=utils.CONFIG.db,
        user=utils.CONFIG.db_user,
        password=utils.CONFIG.db_password,
    )

    if bot._db.must_create_migrations():
        bot._db.create_migrations()
    if await bot._db.must_apply_migrations():
        await bot._db.apply_migrations()


bot.plugins.load_folder("src.bot.plugins")

bot.run()
