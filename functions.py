import aiohttp
import requests
import asyncio

async def fetch_user_info(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            if data["status"] != "OK":
                return None
            return data["result"][0]
        


async def get_upcoming_contests():
    url="https://codeforces.com/api/contest.list"
    response=requests.get(url=url)
    if response.status_code!=200:
        return None
    contests=response.json()["result"]
    upcoming=[c for c in contests if c["phase"] == "BEFORE"]
    upcoming=sorted(upcoming,key=lambda x: x["startTimeSeconds"])
    return upcoming

async def get_user_problem(handle):
    solved=set()

    async with aiohttp.ClientSession() as session:
        url=f"https://codeforces.com/api/user.status?handle={handle}"

        async with session.get(url=url) as resp:
            data=await resp.json()
    submissions=data.get("result",[])
    for sub in submissions:
        if sub.get("verdict")=="OK":
            problem=sub.get("problem",{})
            contest_id=problem.get("contestId")
            index=problem.get("index")
            solved.add(f"{contest_id}{index}")
    
    return solved


