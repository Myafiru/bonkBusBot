from nextcord import slash_command, Interaction, SlashOption, Embed, Member
from nextcord.ext.commands import Cog, Bot
from sql_requests import match_results
import json


class MatchResult(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Logs the results in member profiles and database
    @slash_command(
        name="match_result",
        description="Result of tournament match",
        default_member_permissions=8
    )
    async def match_result(
            self, interaction: Interaction,
            winner: Member = SlashOption(name="winner"),
            winner_score: int = SlashOption("winner_score"),
            loser: Member = SlashOption(name="loser"),
            loser_score: int = SlashOption(name="loser_score"),
            final_match: bool = SlashOption(name="final_match")
    ):
        with open("config.json", "r") as file:
            config = json.load(file)

        channel = self.bot.get_guild(config["guild"]["guild_id"]).get_channel(config["guild"]["match_results_channel_id"])
        embed = Embed(color=0xc93c3e)
        embed.title = "Match results"

        embed.add_field(name=winner.name, value=winner_score)
        embed.add_field(name=loser.name, value=loser_score)
        embed.description = f"{winner.mention} has won the match"
        embed.set_image(winner.avatar.url)

        await match_results({
            "winner": {
                "playerDiscordID": winner.id,
                "score": winner_score
            },
            "loser": {
                "playerDiscordID": loser.id,
                "score": loser_score
            }
        })

        if final_match:
            embed.description = f"{winner.mention} has won the tournament :trophy:"
            guild = self.bot.get_guild(config["guild"]["guild_id"])
            role = guild.get_role(config["guild"]["tournament_winner_role_id"])
            await guild.get_member(winner.id).add_roles(role)

        await interaction.send(f"Sent embed in channel {channel.name}")
        await channel.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(MatchResult(bot))
