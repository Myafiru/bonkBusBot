from nextcord import slash_command, Interaction, Embed
from nextcord.ext.commands import Cog, Bot


class Members(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Shows all member @tags in embed
    @slash_command(
        name="display_members",
        description="Displays all server members with their @tags in embed"
    )
    async def display_members(self, interaction: Interaction):
        embed = Embed(color=0xc93c3e)
        embed.title = f"Members"
        embed.description = ""
        count = 0

        for name in interaction.guild.members:
            if not name.bot:
                embed.description += str(name).replace("_", r"\_") + "\n"
                count += 1

        embed.title += f" ({count})"
        await interaction.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Members(bot))
