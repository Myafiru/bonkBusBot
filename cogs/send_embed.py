from nextcord import slash_command, Interaction, SlashOption, Embed, TextChannel
from nextcord.ext.commands import Cog, Bot


class SendEmbed(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Sends bot embed
    @slash_command(
        name="send_embed",
        description="Send bot embed in channel",
        default_member_permissions=8
    )
    async def send_embed(
        self,
        interaction: Interaction,
        channel: TextChannel = SlashOption(name="channel"),
        title: str = SlashOption(name="embed_title"),
        description: str = SlashOption(name="embed_description")
    ):
        embed = Embed(color=0xc93c3e)
        embed.title = title
        embed.description = description

        await channel.send(embed=embed)
        await interaction.send(f"Sent embed in channel {channel}")


def setup(bot: Bot):
    bot.add_cog(SendEmbed(bot))
