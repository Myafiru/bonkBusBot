from nextcord import slash_command, Interaction, Embed
from nextcord.ext.commands import Cog, Bot
from sql_requests import get_tournaments


class Tournaments(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Displays all tournaments in embeds
    @slash_command(
        name="tournaments",
        description="See information about tournament"
    )
    async def tournaments(self, interaction: Interaction):
        tourney_list = await get_tournaments()

        if len(tourney_list) == 0:
            await interaction.send("There are no tournaments yet")
        else:
            embeds = list()
            for tourney in tourney_list:
                embed = Embed(color=0xc93c3e)
                embed.title = tourney[1]

                embed.add_field(name="Link", value=tourney[2])
                embed.add_field(name="Hosting period", value=tourney[3])
                embed.add_field(name="Amount of players", value=tourney[4])
                embed.add_field(name="Winner", value=tourney[5])
                embed.add_field(name="2nd place", value=tourney[6])
                embed.add_field(name="3rd place", value=tourney[7])
                embeds.append(embed)

            await interaction.send(embeds=embeds)


def setup(bot: Bot):
    bot.add_cog(Tournaments(bot))
