from nextcord import slash_command, Interaction, SlashOption, TextChannel
from nextcord.ext.commands import Cog, Bot
import json


class SetMatchResultsChannel(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name="set_match_results_channel",
        default_member_permissions=8
    )
    async def set_log_channel(self, interaction: Interaction, channel: TextChannel = SlashOption("channel")):
        with open("config.json", "r") as file:
            config = json.load(file)

        with open("config.json", "w") as file:
            config["guild"]["match_results_channel_id"] = channel.id
            file.write(json.dumps(config, indent=2))

        await interaction.send(f"Successfully set a new match results channel: {channel.name}")


def setup(bot: Bot):
    bot.add_cog(SetMatchResultsChannel(bot))
