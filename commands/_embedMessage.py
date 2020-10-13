#Syntax for fields goes like so:
import discord
import enum
import datetime

class discordColours(enum.Enum):
    red = discord.Colour.red()
    green = discord.Colour.green()
    blue = discord.Colour.blue()
    #white = discord.Colour.white()

#returns the embed object
def create(titleString, descriptionString, colourString):
    return discord.Embed(
        title = titleString, 
        description = descriptionString,
        colour = discordColours[colourString].value,
        timestamp = datetime.datetime.utcnow()
        )

"""Adds a field. Pass in the message, title of the field, value, and if it's inline or not"""
def addField(embedMsg, titleString, valueString, inlineBool):
    embedMsg.add_field(name = titleString, value = valueString, inline = inlineBool)

"""Adds an image. Pass in the url"""
def addImage(embedMsg, url):
    embedMsg.set_image(url = url)

"""Adds a footer. Pass in a value for the footer"""
def setFooter(embedMsg, valueString):
    embedMsg.set_footer(text = valueString)