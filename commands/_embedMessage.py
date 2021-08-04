# Syntax for fields goes like so:
import discord
import enum
import datetime


class DiscordColours(enum.Enum):
    red = discord.Colour.red()
    green = discord.Colour.green()
    blue = discord.Colour.blue()


# white = discord.Colour.white()


# returns the embed object
def create(title_string: str, description_string: str, colour_string: str):
    returnMessage = discord.Embed(
        title = title_string,
        description = description_string,
        colour = DiscordColours[colour_string].value,
        timestamp = datetime.datetime.utcnow()
    )

    returnMessage.set_footer(text = "For any concerns, contact a BediBot dev: Aadi, Carson, Sahil, Zayd, & Joe")

    return returnMessage


# Adds a field. Pass in the message, title of the field, value, and if it's inline or not
def add_field(embed_msg: discord.embeds.Embed, title_string: str, value_string: str, is_inline: bool):
    embed_msg.add_field(name = title_string, value = value_string, inline = is_inline)


# Adds an image. Pass in the url
def add_image(embed_msg: discord.embeds.Embed, url: str):
    embed_msg.set_image(url = url)
