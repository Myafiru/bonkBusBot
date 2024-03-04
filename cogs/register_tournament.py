from nextcord import slash_command, Interaction, SlashOption, Member
from nextcord.ext.commands import Cog, Bot
from sql_requests import insert_tournament


class RegisterTournament(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Adds tournament to database
    @slash_command(
        name="register_tournament",
        description="Add tournament to the list",
        default_member_permissions=8
    )
    async def register_tournament(
            self, interaction: Interaction,
            name: str = SlashOption(name="name", description="Tournament name"),
            link: str = SlashOption(name="link", description="Link to tournament brackets"),
            date: str = SlashOption(name="date", description="Tournament hosting period"),
            players: int = SlashOption(name="player_count", description="Amount of players"),
            winner: Member = SlashOption(name="winner", description="Tournament winner"),
            second_place: Member = SlashOption(name="second_place", description="2nd place of tournament"),
            third_place: Member = SlashOption(name="third_place", description="3rd place of tournament")
    ):
        response = await insert_tournament(
            name,
            link,
            date,
            players,
            winner.mention,
            second_place.mention,
            third_place.mention
        )

        if response:
            await interaction.send(f"Registered {name}")
        else:
            await interaction.send("You did the inputs wrong")


def setup(bot: Bot):
    bot.add_cog(RegisterTournament(bot))
