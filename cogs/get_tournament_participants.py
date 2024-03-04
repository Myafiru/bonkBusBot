from nextcord import slash_command, Interaction, Embed
from nextcord.ext.commands import Cog, Bot
import json


class GetTournamentRegistration(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Sends a message in some channel and adds a reaction below it
    @slash_command(
        name="get_tournament_registration",
        description="Checks the amount of reactions under last tournament hosting announcement"
    )
    async def start_tournament_registration(self, interaction: Interaction):
        # Getting tournament host message id
        with open("config.json", "r") as file:
            config = json.load(file)

        channel = self.bot.get_channel(config["guild"]["tournaments_channel_id"])
        message = await channel.fetch_message(config["guild"]["tournament_host_message_id"])
        participants = await message.reactions[0].users().flatten()

        embed = Embed(color=0xc93c3e)
        embed.title = "Tournament participants"
        embed.description = ""
        count = 0

        for name in participants:
            if not name.bot:
                embed.description += str(name).replace("_", r"\_") + "\n"
                count += 1

        embed.title += f" ({count})"
        await interaction.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(GetTournamentRegistration(bot))
