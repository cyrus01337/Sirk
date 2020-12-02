import discord, random, json, time
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

tools = "/home/pi/Discord/Sirk/utils/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)


def rps_winner(userOneChoice, userTwoChoice):
    if userOneChoice == "\U0001faa8":
        if userTwoChoice == "\U00002702": return "You won!"
        if userTwoChoice == "\U0001faa8": return "Tie!"
        if userTwoChoice == "\U0001f4f0": return "I won!"
    elif userOneChoice == "\U00002702":
        if userTwoChoice == "\U00002702": return "Tie!"
        if userTwoChoice == "\U0001faa8": return "I won!"
        if userTwoChoice == "\U0001f4f0": return "You Won!"
    elif userOneChoice == "\U0001f4f0":
        if userTwoChoice == "\U00002702": return "I won!"
        if userTwoChoice == "\U0001faa8": return "You won!"
        if userTwoChoice == "\U0001f4f0": return "Tie!"
    else: return "error"
    
class games(commands.Cog):
    '''Game Commands'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def dice(self, ctx):
        '''Roll a dice'''
        dice = ['1', '2', '3', '4', '5', '6', 'off the table...\n*You Found The Mystery!*']
        embed = discord.Embed(title="Dice", description=f'The Dice Rolled {random.choice(dice)}', color=color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png")
        embed.set_footer(text=footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def quiz(self, ctx):
        '''Take a halloween quiz'''
        qa = {
            "`What was Halloween originally called?`": "ALL HALLOWS EVE",
            "`What was candy corn originally called?`": "CHICKEN FEED",
            "`(Approx)How much money does the average American spend on Halloween every year?`\n**A) $45\nB) $60\nC) $85\nD) $100**": "C",
            "`(Approx)What percentage of kids like to recieve gum for halloween?`": "10",
            "`When is Halloween?`": "OCTOBER 31",
            "`What country was Trick-or-treating first done?`": "CANADA"
        }
        total_questions = len(qa)
        start_time = time.time()

        def check(message):
            return ctx.author == message.author and ctx.channel == message.channel

        for i, (question, answer) in enumerate(qa.items()):
            content = ""
            append = "Type your answer below"

            if i == 0:
                content += "Quest Started!\n"
            elif i == 2:
                append += " [Format: A|B|C|D]"
            else:
                content += "Correct!\n"
            content += (f"**Question {i+1})** {question}\n"
                        f"{append}")
            await ctx.send(content)

            try:
                message = await self.bot.wait_for("message", timeout=45.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Timeout Error")

            if message.content.upper() != answer:
                return await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}quest`")
        time_taken = time.time()- start_time
        await ctx.send(f"Correct!\nYou took **{time_taken:,.2f} seconds!**")

    
    @commands.cooldown(1,3,BucketType.user)
    @commands.command()
    async def rps(self, ctx):
        """Rock paper scissors, either play against the bot or against a user"""
        choices = ["\U0001f4f0", "\U0001faa8", "\U00002702"]
        s = m = await ctx.send(embed = discord.Embed(title = f"Rock, Paper, Scissors.", description = f" {str(ctx.author)} Choose your weapon!", color=color))
        for i in choices:
            await m.add_reaction(i)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in choices

        try:
            reaction = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
            reaction = reaction[0].emoji
            botChoice = random.choice(choices)
            result = rps_winner(reaction, botChoice)

            await s.edit(embed= discord.Embed(title = "Results:", description = f"I picked {botChoice} and you picked {reaction} \n\n{result}", color=color))

        except asyncio.TimeoutError: return await ctx.send("You didn't add a reaction in time!")

def setup(bot):
    bot.add_cog(games(bot))
