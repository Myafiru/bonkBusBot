from nextcord import slash_command, Interaction, SlashOption, TextChannel
from nextcord.ext.commands import Cog, Bot


class SendMessage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Sends bot message
    @slash_command(
        name="send_message",
        description="Send bot message in channel",
        default_member_permissions=8
    )
    async def send_message(self, interaction: Interaction,
                           channel: TextChannel = SlashOption(name="channel"),
                           message: str = SlashOption(name="message")):
        await channel.send(message)
        await interaction.send(f"Sent message in channel {channel}")


def setup(bot: Bot):
    bot.add_cog(SendMessage(bot))
