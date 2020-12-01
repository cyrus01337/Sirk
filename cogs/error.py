import discord
from discord.ext import commands
from discord.ext.commands import Cog

import typing

# noinspection PyRedundantParentheses
class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    """Pretty much from here:
    https://github.com/4Kaylum/DiscordpyBotBase/blob/master/cogs/error_handler.py"""

    async def send_to_ctx_or_author(self, ctx, text: str = None, *args, **kwargs) -> typing.Optional[discord.Message]:
        """Tries to reply the given text to ctx, but failing that, tries to reply it to the author
        instead. If it fails that too, it just stays silent."""

        try:
            return await ctx.send(text, *args, **kwargs)
        except discord.Forbidden:
            try:
                return await ctx.author.send(text, *args, **kwargs)
            except discord.Forbidden:
                pass
        except discord.NotFound:
            pass
        return None

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored_errors = (commands.CommandNotFound, commands.NotOwner)
        
        error = getattr(error, "original", error)

        if isinstance(error, ignored_errors):
            return

        setattr(ctx, "original_author_id", getattr(ctx, "original_author_id", ctx.author.id))
        owner_reinvoke_errors = (
            commands.MissingAnyRole, commands.MissingPermissions,
            commands.MissingRole, commands.CommandOnCooldown, commands.DisabledCommand
        )

        if ctx.original_author_id in self.bot.owner_ids and isinstance(error, owner_reinvoke_errors):
            return await ctx.reinvoke()
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        #elif isinstance(error, commands.NotOwner):
            #await ctx.send(embed = discord.Embed(title = "You are not an owner.", color = discord.Color.red()))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, discord.NotFound): await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.CommandOnCooldown): await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        else:
            c = bot.get_channel(783138336323403826) 
            embed = discord.Embed(
                title = "An error occurred!",
                description = f"Reported to the support server. Need more help? [Join the support server](https://discord.gg/7yZqHfG)\n```Error: \n{str(error)}```",
                timestamp = datetime.datetime.utcnow()
            )
            embed.set_footer(text = f"Caused by: {ctx.command}")
            await ctx.send(embed = embed)

            #Support server embed
            embed = discord.Embed(
                title = f"An error occured!",
                description = f"```{str(error)}```",
                timestamp = datetime.datetime.utcnow()
            )
            embed.add_field(
                name = "Details:",
                value = f"""
                Caused by: `{str(ctx.author)} [{int(ctx.author)}]`
                In guild: `{str(ctx.guild)} [{int(ctx.guild)}]`
                Command: `{ctx.command}`
                """
            )
            await c.send(embed = embed)

'''        # Command is on Cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            return await self.send_to_ctx_or_author(ctx, f"This command is on cooldown. **Try in `{int(error.retry_after)}` seconds**", delete_after=10.0)

        # Missing argument
        elif isinstance(error, commands.MissingRequiredArgument):#{error.param.name}
            return await self.send_to_ctx_or_author(ctx, str(error))

        # Missing Permissions
        elif isinstance(error, commands.MissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f"You're missing the required permission: `{error.missing_perms[0]}`")

        # Missing Permissions
        elif isinstance(error, commands.BotMissingPermissions):
            return await self.send_to_ctx_or_author(ctx, f"Sirk is missing the required permission: `{error.missing_perms[0]}`")

        # Discord Forbidden, usually if bot doesn't have permissions
        elif isinstance(error, discord.Forbidden):
            return await self.send_to_ctx_or_author(ctx, f"I could not complete this command. This is most likely a permissions error.")

        # User who invoked command is not owner
        elif isinstance(error, commands.NotOwner):
            return await self.send_to_ctx_or_author(ctx, f"You must be the owner of the bot to run this command.")
        
        raise error'''

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
