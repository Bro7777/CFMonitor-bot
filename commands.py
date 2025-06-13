import discord
from discord.ext import commands
import os
import datetime
import random
import aiohttp
import asyncio

from config import *
from functions import *
from database import *



@Bot.tree.command(name="stats",description="Show statistics of a user")
async def stats(interaction:discord.Interaction,handle:str=None):
    await interaction.response.defer()
    discord_id=interaction.user.id
    if not handle:
        handle=get_handle(discord_id=discord_id)
        if not handle:
            stat_embed=discord.Embed(title="You don't have any account linked")
            await interaction.followup.send(embed=stat_embed)
            return
        handle=handle[1]
    
    user=await fetch_user_info(handle=handle)
    if not user:
        stat_embed=discord.Embed("❌ User not found.")
        await interaction.followup.send(embed=stat_embed)
        return
    stat_embed=discord.Embed(title=f"{handle}'s stats",description=f"[🔗 Profile link](https://codeforces.com/profile/{handle})")
    stat_embed.set_thumbnail(url=user.get("titlePhoto", ""))
    stat_embed.add_field(name="Rank", value=user.get("rank", "Unranked").title(), inline=True)
    stat_embed.add_field(name="Rating", value=str(user.get("rating", "N/A")), inline=True)
    stat_embed.add_field(name="Max Rating", value=str(user.get("maxRating", "N/A")), inline=True)
    stat_embed.add_field(name="Country", value=str(user.get("country", "N/A")), inline=True)
    stat_embed.add_field(name="Friend of", value=str(user.get("friendOfCount", "0"))+" users", inline=True)

    #stat_embed.set_footer(text=f"Contests joined: {user.get('contestCount', 'N/A')}")

    await interaction.followup.send(embed=stat_embed)

@Bot.tree.command(name="contests",description="Shows upcoming contests")
async def contests(interaction:discord.Interaction):
    await interaction.response.defer()
    contests=await get_upcoming_contests()

    contest_embed=discord.Embed(title="📅 Upcoming Contests")

    for con in contests:
        start_time=datetime.datetime.utcfromtimestamp(con["startTimeSeconds"])
        contest_id=con["id"]
        duration=con["durationSeconds"]//60
        link=f"https://codeforces.com/contests/{contest_id}"
        name=con["name"]
        name_link=f"[Click!]({link})"

        contest_embed.add_field(
                name=name,
                value=(
                    f"🕒 Date: <t:{int(con['startTimeSeconds'])}:f>\n"
                    f"⏲️ Before start: <t:{int(con['startTimeSeconds'])}:R>\n"
                    f"⌛ Duration: {duration} minutes \n"
                    f"🔗 Link: {name_link}"
                ),
                inline=False
            )
    
    await interaction.followup.send(embed=contest_embed)

@Bot.tree.command(name="link",description="Link your CF account to your discord account")
async def link(interaction:discord.Interaction,handle:str):
    await interaction.response.defer()
    problem_id=random.randint(1,2000)
    problem_index="A"
    url=f"https://codeforces.com/problemset/problem/{problem_id}/{problem_index}"
    user=await fetch_user_info(handle=handle)
    embed_title="✅ Account found"
    if not user:
        embed_title="❌ No account found"
    if embed_title=="✅ Account found":
        instructions_embed=discord.Embed(title=embed_title,description=
                                         f"🔐 Verification process for `{handle}` is started!\n"
                                         f"Submit a CPE to this problem in 60 seconds:\n"
                                         f"👉 [{problem_id}{problem_index}]({url})\n"
                                         )
    else:
        instructions_embed=discord.Embed(title=embed_title)
        await interaction.followup.send(embed=instructions_embed)
        return
    
    instructions_embed.set_thumbnail(url=user.get("titlePhoto", ""))
    instructions_embed.add_field(name="Handle",value=handle,inline=True)
    instructions_embed.add_field(name="Rank", value=user.get("rank", "Unranked").title(), inline=True)
    instructions_embed.add_field(name="Rating", value=str(user.get("rating", "N/A")), inline=True)
    instructions_embed.add_field(name="Verification Status", value="Waiting...", inline=True)
    message=await interaction.followup.send(embed=instructions_embed)

    for i in range(10):
        await asyncio.sleep(6)

        async with aiohttp.ClientSession() as session:
            check_url=f"https://codeforces.com/api/user.status?handle={handle}&count=1"

            async with session.get(url=check_url) as resp:
                if(resp.status!=200):
                    await interaction.followup.send("❌ API Error.Please try again later")
                    return
                data=await resp.json()
        
        submissions=data.get("result",[])
        success=False
        for sub in submissions:
            if (
                    sub.get("problem", {}).get("contestId") == problem_id and
                    sub.get("problem", {}).get("index") == problem_index and
                    sub.get("verdict") == "COMPILATION_ERROR"
                ):

                discord_id=str(interaction.user.id)
                link_handle(discord_id=discord_id,handle=handle)
                success=True
                #await interaction.followup.send(f"✅ Success! `{handle}` is now linked to {interaction.user.mention}.")
                break
        if success==True:
            break
    
    if success==True:
        instructions_embed.set_field_at(3,name="Verification Status",value=f"✅ Success! `{handle}` is now linked to {interaction.user.name}.")
        instructions_embed.color=discord.Colour.green()
        await message.edit(embed=instructions_embed)
    else:
        instructions_embed.set_field_at(3,name="Verification Status",value=f"❌ Fail! No CPE detected.Please try again")
        instructions_embed.color=discord.Colour.red()
        await message.edit(embed=instructions_embed)

@Bot.tree.command(name="suggest_problem",description="Suggest a problem")
async def suggest_problem(interaction:discord.Interaction,rating:int=None,problem_tag:str=None):
    await interaction.response.defer()
    discord_id=interaction.user.id
    user_handle=get_handle(discord_id=discord_id)[1]
    if user_handle:
        solved_problems=await get_user_problem(handle=user_handle)
    else:
        solved_problems=[]

    
    #for i in solved_problems:
        #print(i)
    async with aiohttp.ClientSession() as session:
        problem_url="https://codeforces.com/api/problemset.problems"
        async with session.get(problem_url) as resp:
            data=await resp.json()
        
        unsolved=[]
        for problem,problem_stats in zip(data["result"]["problems"],data["result"]["problemStatistics"]):
            pid=f"{problem.get('contestId')}{problem.get('index')}"

            if pid in solved_problems:
                continue
            if rating and problem.get("rating")!=rating:
                continue
            if problem_tag and problem_tag not in problem.get("tags", []):
                continue

            unsolved.append(problem)


        suggested_problem=random.choice(unsolved)
        p_title=f"{suggested_problem['contestId']}{suggested_problem['index']} : {suggested_problem['name']}"
        p_link=f"https://codeforces.com/problemset/problem/{suggested_problem['contestId']}/{suggested_problem['index']}"

        res_embed=discord.Embed(title="🧩 Suggested Problem",description=f"[{p_title}]({p_link})")


        if "rating" in suggested_problem:
                res_embed.add_field(name="Rating", value=str(suggested_problem["rating"]))
        if suggested_problem.get("tags"):
                res_embed.add_field(name="Tags", value=", ".join(suggested_problem["tags"]))

        await interaction.followup.send(embed=res_embed)

@Bot.tree.command(name="unlink",description="Unlink your CF account")
async def unlink(interaction:discord.Interaction):
    await interaction.response.defer()
    discord_id=interaction.user.id
    unlink_handle(discord_id=discord_id)
    answer_embed=discord.Embed(title="Account unlinked")
    await interaction.followup.send(embed=answer_embed)

@Bot.tree.command(name="user_list",description="Show Handle of the users in the server")
async def user_list(interaction:discord.Interaction):
    await interaction.response.defer()
    members=interaction.guild.members
    linked_users=[]
    print(members)
    for member in members:
        handle=get_handle(discord_id=member.id)
        print(member.id,handle)
        if handle!=None:
           handle=handle[1]
           user_data=await fetch_user_info(handle=handle)
           print(user_data)
           user_rating=str(user_data.get("rating", "N/A"))
           linked_users.append((member.name,handle,int(user_rating)))
    print(linked_users)
    header = f"{'User':<16} | {'Handle':<12} | Rating\n"
    separator = f"{'-'*16}-|{'-'*13}-|--------\n"
    rows = ""
    linked_users=sorted(linked_users,key=lambda x:x[2],reverse=True)
    for linked_member in linked_users:
        username=linked_member[0]
        member_handle=linked_member[1]
        member_rating=linked_member[2]
        rows += f"{username:<16} | {member_handle:<12} | {member_rating}\n"
    
    message = f"```{header}{separator}{rows}```"


    list_embed=discord.Embed(title="User Handles",description=message)
    await interaction.followup.send(embed=list_embed)



    
    







async def add_commands():
   Bot.tree.add_command(stats)
