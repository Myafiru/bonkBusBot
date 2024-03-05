from time import mktime
import nextcord as nc
from nextcord.ext.commands import Bot
import traceback
import json

with open("config.json", "r") as config:
    config = json.load(config)

bot = Bot(intents=nc.Intents.all())

cogs = [
    "cogs.add_alt",
    "cogs.display_members",
    "cogs.get_tournament_participants",
    "cogs.match_result",
    "cogs.profile",
    "cogs.register_tournament",
    "cogs.remove_alt",
    "cogs.send_embed",
    "cogs.send_message",
    "cogs.set_log_channel",
    "cogs.set_match_results_channel",
    "cogs.set_tournaments_channel",
    "cogs.start_tournament_registration",
    "cogs.tournaments"
]

bot.load_extensions(cogs)


@bot.event
async def on_ready():
    await bot.sync_all_application_commands()
    print("YEEE IT'S RUNNIN' BABY")


@bot.event
async def on_application_command_error(interaction: nc.Interaction, error):
    log_channel = bot.get_guild(config["guild"]["guild_id"]).get_channel(config["guild"]["logs_channel_id"])
    full_error = "".join(traceback.format_exception(error.__class__, error, error.__traceback__))

    await interaction.send(
        "An error occurred while running a command.\nGoofy ass Saph will check it.",
        ephemeral=True
    )
    await log_channel.send(
        f"||<@{config['admin_id']}>||\n"
        "An error occurred while running a command.\n"
        f"`Command`: {interaction.application_command.name}\n"
        f"`Error`: {full_error}\n"
        f"`Time`: <t:{int(mktime(interaction.created_at.timetuple()))}:f>\n"
    )


if __name__ == "__main__":
    bot.run(config["bot_token"])
