import aiohttp
import asyncio 
async def CheckLinktreeUsername(Session, Username, Proxy):
    url = "https://linktr.ee/validate/username"
    payload = {"username": Username}
    headers = {
        'content-type': 'application/json',
    }

    if Proxy == False:
        try:
            async with Session.post(url,json=payload,headers=headers) as response:
                if response.status != 200: 
                    return 0
                
                response_object = await response.json()
                response_object['Username'] = Username
                return response_object
        except:
            return 0
    else:
        p=f"http://{Proxy["username"]}:{Proxy["password"]}@{Proxy["ip"]}"
        try:
            async with Session.post(url,json=payload,headers=headers,proxy=p) as response:
                if response.status != 200:
                    return 0
                
                response_object = await response.json()
                response_object['Username'] = Username
                return response_object
        except:
            return 0

sleepTime = 0
async def CheckDiscordUsername(Session, Username, Proxy):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
    payload={"username": Username}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': '/',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': "application/json",
        'X-Discord-Locale': 'en-US',
        'X-Discord-Timezone': 'America/New_York',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com/',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }

    if Proxy == False:
        try:
            resp = await Session.post(url, json=payload, headers=headers)
            if resp.status == 200:
                resp = await resp.json()
                resp['Username'] = Username
                return resp
            else:
                return 0
        except:
            resp = {'taken': True}
            return 0
    else:
        p=f"http://{Proxy["username"]}:{Proxy["password"]}@{Proxy["ip"]}"
        try:
            resp = await Session.post(url, json=payload, proxy=p,headers=headers)
            if resp.status == 200:
                resp = await resp.json()
                resp['Username'] = Username
                return resp
            else:
                return 0
        except:
            return 0
        
async def CheckRobloxUsername(Session, Username, Proxy):
    url = f'https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={Username}'

    if Proxy == False:
        try:
            response = await Session.request("GET",url=url)
            if response.status == 200:
                data = await response.json()

                if data['code'] == 0:
                    return {'Username': Username, 'taken': False}
                if data['code'] == 1:
                    return {'Username': Username, 'taken': True}
                if data['code'] == 2:
                    return {'Username': Username, 'taken': True}
                if data['code'] == 10:
                    return {'Username': Username, 'taken': True}
            else:
                return 0
        except:
            return 0
    else:
        p=f"http://{Proxy["username"]}:{Proxy["password"]}@{Proxy["ip"]}"
        try:
            response = await Session.request("GET",url=url, proxy=p)
            if response.status == 200:
                data = await response.json()

                if data['code'] == 0:
                    return {'Username': Username, 'taken': False}
                if data['code'] == 1:
                    return {'Username': Username, 'taken': True}
                if data['code'] == 2:
                    return {'Username': Username, 'taken': True}
                if data['code'] == 10:
                    return {'Username': Username, 'taken': True}
            else:
                return 0
        except:
            return 0
        
async def CheckDiscordVanity(Session, Vanity, Proxy):
    url = f"https://discord.com/api/v9/invites/{Vanity}?with_counts=true&with_expiration=true"

    if Proxy == False:
        try:
            response = await Session.get(url=url)
            if response.status == 200:
                data = await response.json()
                data['Vanity'] = Vanity
                return data
            elif response.status == 404:
                data = await response.json()
                data["Vanity"] = Vanity
                return data
        except:
            return 0
    else:
        try:
            p=f"http://{Proxy["username"]}:{Proxy["password"]}@{Proxy["ip"]}"
            response = await Session.get(url=url, proxy=p)
            if response.status == 200:
                data = await response.json()
                data['Vanity'] = Vanity
                return data
            elif response.status == 404:
                data = await response.json()
                data['Vanity'] = Vanity
                return data
        except:
            exit()
            return 0
        
async def CheckMinecraftUsername(Session, Username):
    url = f'https://api.mojang.com/users/profiles/minecraft/{Username}'

    try:
        async with Session.get(
            url
        ) as response:
            response = await response.json()
            response['Username'] = Username
            return response
    except:
        return 0
    
async def CheckGithubUsername(Session, Username, Proxy):
    url = f"https://github.com/signup_check/username?value={Username}"
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    if Proxy == False:
        try:
            async with Session.get(url=url, headers=headers) as response:
                response = await response.text()
                return response
        except:
            return 0
    else:
        p=f"http://{Proxy["username"]}:{Proxy["password"]}@{Proxy["ip"]}"
        
        try:
            async with Session.get(url=url, headers=headers, proxy=p) as response:
                response = await response.text()
                return response
        except:
            return 0
        
