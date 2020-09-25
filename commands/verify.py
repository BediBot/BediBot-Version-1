import os

os.environ['UW_API_KEY'] = ''
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def emailTest(ctx):
    email = ctx.content.split(" ")[1]

    if email.endswith('@uwaterloo.ca'):
        userID = email[:email.rfind('@')]





    userData = uw_driver.directory_people_search(userID)

    await ctx.channel.send(userData.get('department'))