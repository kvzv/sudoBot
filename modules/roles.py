import discord
from discord.ext import commands
import json

class Roles:
    """
    Role relaated Commands
    """

    def __init__(self, client, config):
        self.client = client
        self.config = config

    @commands.command(pass_context=True)
    async def listdistro(self, ctx):
        """List available joinable user roles."""
        _rolesList = '\n'.join(map(str, self.config["user_roles"]))

        return await ctx.send('```🌶 Dostepne rangi:\n' + _rolesList + '\n```')

    @commands.command(pass_context=True)
    async def joindistro(self, ctx, *, distro : str):
        """Add yourself to a joinable user role."""
        server = ctx.message.guild
        member = ctx.message.author

        if distro.lower() == 'debian':
            distro = 'Debian'

        roles = self.config["user_roles"]

        serverRoles = []
        memberRoles = []

        for _id, role in enumerate(server.roles):
            serverRoles.append(role.name)

        for _id, role in enumerate(member.roles):
            memberRoles.append(role.name)

        if distro.lower() in map(str.lower, serverRoles):
            if distro.lower() in map(str.lower, roles):
                if distro.lower() in map(str.lower, memberRoles):
                    return await ctx.send("🌶 Juz posiadasz ta range.")
                else:
                    try:
                        lowarr = [item.lower() for item in serverRoles]
                        index = lowarr.index(distro.lower())
                        newrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                        await member.add_roles(newrole, reason="Pepper: 🌶 Dodane przez uzytkownika.")
                        return await ctx.send("Added {} to group {}.".format(member.display_name, newrole.name))
                    except Exception as e:
                        raise Exception(e)
                        return
            else:
                return await ctx.send("🌶 Taka ranga nie istnieje :fearful:")
        else:
            return await ctx.send("🌶 Taka ranga nie istnieje :fearful:")


    @commands.command(pass_context=True)
    async def distrostats(self, ctx, *, rolename : str=None):
        """Show role statistics"""
        server = ctx.message.guild
        roles = self.config["user_roles"]
        emotes = {}

        serverRoles = []
        for _id, role in enumerate(server.roles):
            serverRoles.append(role.name)

        for _id, emote in enumerate(server.emojis):
            name = emote.name
            name.replace(" ","")
            emotes[str(name)] = emote.url

        role = rolename
        if ( role != None ):
            if ( role.lower() in map(str.lower, roles) ):
                lowarr = [item.lower() for item in serverRoles]
                index = lowarr.index(role.lower())
                thisrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                if ( thisrole != None ):
                    try:
                        image = emotes[thisrole.name.lower()]
                    except:
                        image = ''
                    embed = discord.Embed(title=thisrole.name, color = thisrole.colour)
                    embed.set_thumbnail(url=image)
                    embed.add_field(name = "Member Count", value = "{}".format(len(thisrole.members), inline=True))
                    embed.add_field(name = "Color (RGB)", value = "({},{},{})".format(thisrole.colour.r, thisrole.colour.g, thisrole.colour.b))
                    return await ctx.send(embed = embed) 
            else:
                return await ctx.send("🌶 Taka ranga nie istnieje (lub nie jest publiczna) :fearful:")
        else:
            stats = []
            string = ""
            for role in roles:
                lowarr = [item.lower() for item in serverRoles]
                index = lowarr.index(role.lower())
                thisrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                if ( thisrole != None ):
                    stats.append(thisrole)
            stats.sort(key=lambda x: len(x.members), reverse=True)
            embed = discord.Embed(title="Distro Statistics")
            for role in stats:
                try:
                    image = emotes[role.name.lower()]
                except:
                    image = ''
                embed.add_field(name = "{}".format(role.name), value = "{}".format(len(role.members)), inline=False)

            return await ctx.send(embed = embed)

    @commands.command(pass_context=True)
    async def leavedistro(self, ctx, *, distro : str):
        """Remove yourself to a joinable user role."""
        server = ctx.message.guild
        member = ctx.message.author

        if distro.lower() == 'debian':
            distro = 'Debian'

        roles = self.config["user_roles"]

        serverRoles = []
        memberRoles = []

        for _id, role in enumerate(server.roles):
            serverRoles.append(role.name)

        for _id, role in enumerate(member.roles):
            memberRoles.append(role.name)

        if distro.lower() in map(str.lower, serverRoles):
            if distro.lower() in map(str.lower, roles):
                if distro.lower() in map(str.lower, memberRoles):
                    try:
                        lowarr = [item.lower() for item in serverRoles]
                        index = lowarr.index(distro.lower())
                        deletedrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                        await member.remove_roles(deletedrole, reason="Pepper: 🌶 Usunieto przez uzytkownika.")
                        return await ctx.send("🌶 Wyrzucono {} z grupy {}.".format(member.display_name, deletedrole.name))
                    except Exception as e:
                        raise Exception(e)
                        return
                else:
                    return await ctx.send("🌶 Nie posiadasz tej rangi.")
            else:
                return await ctx.send("🌶 Taka ranga nie istnieje :fearful:")
        else:
            return await ctx.send("🌶 Taka ranga nie istnieje :fearful:")

def setup(client):
    client.add_cog(Roles(client, client.config))
