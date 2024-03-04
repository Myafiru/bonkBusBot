from nextcord import slash_command, Interaction, SlashOption, Member, Embed, DefaultAvatar
from nextcord.ext.commands import Cog, Bot
from sql_requests import get_user


class Profile(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Displays information about member of the server in embed
    @slash_command(
        name="profile",
        description="Displays information about user"
    )
    async def profile(self, interaction: Interaction, user: Member = SlashOption(name="user")):
        embed = Embed(color=0xc93c3e)
        embed.set_author(name=user.name, icon_url=user.avatar)

        user_data = await get_user(str(user.id))

        embed.add_field(name="Alt accounts", value="\n".join(user_data[1].split("#")))
        embed.add_field(name="Won tournaments", value="\n".join(user_data[2]))
        embed.add_field(name="Won games", value=user_data[3])
        embed.add_field(name="Lost games", value=user_data[4])
        embed.add_field(name="Total games", value=user_data[3] + user_data[4])

        if user_data[3] + user_data[4] != 0:
            embed.add_field(
                name="Win rate",
                value=f'{user_data[3] / (user_data[3] + user_data[4]) * 100:.2f}%'
            )
        else:
            embed.add_field(name="Win rate", value="N/A")

        embed.set_image(user.avatar)
        await interaction.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Profile(bot))
