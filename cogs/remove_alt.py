from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext.commands import Cog, Bot
from sql_requests import remove_alt


class RemoveAlt(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Removes alt account from database
    @slash_command(
        name="remove_alt",
        description="Remove your alt account"
    )
    async def remove_alt(self, interaction: Interaction, alt: str = SlashOption(name="alt_account")):
        user_id = str(interaction.user.id)
        response = await remove_alt(user_id, alt)

        if response:
            await interaction.send(f"Successfully removed account `{alt}` from your profile")
        else:
            await interaction.send(f"No account `{alt}` was found in your profile", ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(RemoveAlt(bot))
