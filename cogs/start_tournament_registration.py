from nextcord import slash_command, Interaction, TextChannel
from nextcord.ext.commands import Cog, Bot
import json


class StartTournamentRegistration(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Sends a message in some channel and adds a reaction below it
    @slash_command(
        name="start_tournament_registration",
        description="Start a registration for tournament",
        default_member_permissions=8
    )
    async def start_tournament_registration(self, interaction: Interaction):
        with open("config.json", "r") as file:
            config = json.load(file)

        channel = self.bot.get_channel(config["guild"]["tournaments_channel_id"])
        message = await channel.send(
            "||@everyone||\nA new tournament is hosted. Click on the reaction below to participate"
        )

        # Registering new tournament host message id
        with open("config.json", "r") as file:
            config = json.load(file)
        with open("config.json", "w") as file:
            config["guild"]["tournament_host_message_id"] = message.id
            file.write(json.dumps(config, indent=2))

        await message.add_reaction(emoji="💀")
        await interaction.send(f"Sent message in channel {channel.name}")


def setup(bot: Bot):
    bot.add_cog(StartTournamentRegistration(bot))
