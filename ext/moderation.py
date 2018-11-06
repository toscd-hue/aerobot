import discord
from discord.ext import commands
import datetime
import typing


class Moderation:
    """Cogs made for moderation.

    Include various other stuff as well.
    """

    def __init__(self, bot):
        self.bot = bot
        self.toscd = bot.get_guild(288455332173316106)

    @commands.command()
    async def getuserid(self, ctx, user: discord.User):
        """Get a user's ID. If the bot cannot find the person, try making sure capitalization is followed
        or use the full ping including the discriminator.
        """

        await self.bot.say(f'{ctx.author.mention} **||** That user\'s ID is **`{user.id}`**')

    @commands.command()
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def addrole(self, ctx, role: commands.Greedy[discord.Role], user: discord.Member, *, reason='None'):
        """Adds a role to a user.

        /addrole [role, if multi-word use quotes] [member] {reason: optional}
        You can pass more than one role in at the same time, make sure it is between member and /addrole.
        """

        await user.add_roles(*role)
        em = discord.Embed(colour=discord.Colour.green(), description='Logging Entry - `/addrole`')
        em.add_field(name=f'Member:', value=f'{user.mention}')
        em.add_field(name='Role(s) added:', value=', '.join(role))
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await (self.toscd.get_channel(288467626890362880)).send(embed=em)
        await user.send('A recipt of a moderator action has been sent to you:', embed=em)

    @commands.command()
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def addrole(self, ctx, role: commands.Greedy[discord.Role], user: discord.Member, *, reason='None'):
        """Adds a role to a user.

        /removerole [role, if multi-word use quotes] [member] {reason: optional}
        You can pass more than one role in at the same time, make sure it is between member and /removerole.
        """

        await user.remove_roles(*role)
        em = discord.Embed(colour=discord.Colour.red(), description='Logging Entry - `/removerole`')
        em.add_field(name=f'Member:', value=f'{user.mention}', inline=True)
        em.add_field(name='Role(s) removed:', value=', '.join(role), inline=True)
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await (self.toscd.get_channel(288467626890362880)).send(embed=em)
        await user.send('A recipt of a moderator action has been sent to you:', embed=em)

    @commands.command(name='kick', aliases=['boot'])
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def _kick(self, ctx, user: discord.Member, *, reason='None'):
        """Kicks a user

        /kick [user] {reason: optional}
        """

        em = discord.Embed(colour=discord.Colour.orange(),
                           description='Logging Entry - `/kick`\n\nAppeals can be sent in the '
                                       '[verification server](http://discord.gg/JHTyKYA)')
        em.add_field(name='Kicked member', value=f'{user.mention}')
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await user.send(embed=em)
        await (self.toscd.get_channel(288467626890362880)).send('You can appeal by DMing me once you join '
                                                                'the Auth server by using `/appeal [contents]`.',
                                                                embed=em)
        await user.kick(reason=f'Action by {ctx.author}')

    @commands.command(name='ban')
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def _ban(self, ctx, user: discord.Member, *, reason='None'):
        """Bans a user

        /ban [user] {reason: optional}
        """

        em = discord.Embed(colour=discord.Colour.orange(),
                           description='Logging Entry - `/ban`\n\nAppeals can be sent in the '
                                       '[verification server](http://discord.gg/JHTyKYA)')
        em.add_field(name='Banned member', value=f'{user.mention}')
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await user.send(embed=em)
        await (self.toscd.get_channel(288467626890362880)).send('You can appeal by DMing me once you join '
                                                                'the Auth server by using `/appeal [contents]`',
                                                                embed=em)
        await user.ban(reason=f'Action by {ctx.author}')

    @commands.command(name='mute', aliases=['blackmail', 'bm'])
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def _mute(
            self,
            ctx,
            user: discord.Member,
            time: typing.Optional[int]=3600,
            *, reason='None'
    ):
        """Mutes a user.

        /mute [user] {time in seconds: optional, def: 3600s} {reason: optional}
        """

        em = discord.Embed(colour=discord.Colour.orange(),
                           description='Logging Entry - `/mute`\n\nAppeals can be sent to me!')
        em.add_field(name='Muted member', value=f'{user.mention}', inline=True)
        em.add_field(name='Time:', value=f'{time}', inline=True)
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        muted = self.toscd.get_role(289194167463182337)

        await user.add_roles(muted, reason=f'Action by {ctx.author}')
        await __import__('asyncio').sleep(time)
        await user.remove_roles(muted, reason='Unmute.')
        await user.send('You have been unmuted.')

    @commands.command
    async def appeal(self, ctx, *, contents):
        """You can send an appeal to the mods using this command.
        Please be as detailed as you can in the details.
        """

        em = discord.Embed(colour=discord.Colour.dark_magenta(), description='Appeal Entry')
        em.add_field(name='Member:', value=f'{ctx.author}, ID `{ctx.author.id}`')
        em.add_field(name='Contents:', value=f'{contents}')
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()

        await (self.toscd.get_channel(297442649168936961)).send(embed=em)
        await ctx.author.send('Your appeal was successfully sent.')


def setup(bot):
    bot.add_cog(Moderation(bot))
