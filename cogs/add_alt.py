from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext.commands import Cog, Bot
from sql_requests import add_alt


class AddAlt(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Adds alt account in database
    @slash_command(
        name="add_alt",
        description="Add your alt account"
    )
    async def add_alt(self, interaction: Interaction, alt: str = SlashOption(name="alt_account")):
        user_id = str(interaction.user.id)
        response = await add_alt(user_id, alt)

        if response == "InvalidName":
            await interaction.send("Invalid username: username is non-ascii or too long", ephemeral=True)
        elif response == "AlreadyInDB":
            await interaction.send("This account is already in your profile", ephemeral=True)
        elif response == "AltsListLimit":
            await interaction.send("You have reached the limit of alt accounts (40)", ephemeral=True)
        else:
            await interaction.send(f"Successfully added alt account `{alt}` to your profile")


def setup(bot: Bot):
    bot.add_cog(AddAlt(bot))
