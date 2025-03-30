import os
import time
import requests
import datetime
import discord
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

TOKEN = "MTM1NTA0MDEzODg4NzE3MjE5Nw.GzZ2G0.d73ji8-0l78jdyz_awcBofpOM3kyFm8-TEP3TA"
CHANNEL_ID = 1355924705000816693

running_tasks = {}
waiting_users = {}
executor = ThreadPoolExecutor(max_workers=1000)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def send_discord_embed(tiktok_data):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="✨ **TĂNG FOLLOW THÀNH CÔNG** ✨", color=discord.Color.green())
        embed.add_field(name="🆔 **ID**", value=f"``{tiktok_data['user']['id']}``", inline=False)
        embed.add_field(name="📛 **Name**", value=f"**{tiktok_data['user']['nickname']}**", inline=False)
        embed.add_field(name="👤 **Username**", value=f"`@{tiktok_data['user']['uniqueId']}`", inline=False)
        embed.add_field(name="✅ **Verified**", value="✔️ *Đã xác minh*" if tiktok_data["user"]["verified"] else "❌ *Chưa xác minh*", inline=False)
        embed.add_field(name="📜 **Bio**", value=f"```{tiktok_data['user']['signature']}```", inline=False)
        embed.add_field(name="👥 **Followers**", value=f"**{tiktok_data['stats']['followerCount']}** Followers", inline=True)
        embed.add_field(name="🔄 **Following**", value=f"**{tiktok_data['stats']['followingCount']}** Đang Follow", inline=True)
        embed.add_field(name="❤️ **Likes**", value=f"**{tiktok_data['stats']['heartCount']}** Thích", inline=True)
        embed.add_field(name="🎥 **Videos**", value=f"**{tiktok_data['stats']['videoCount']}** Video", inline=True)
        await channel.send(embed=embed)

def get_tiktok_info(username):
    url = f"https://hoangkhiemtruong.cameraddns.net/tiktok/info.php?username={username}"
    response = requests.get(url).json()
    
    return response["data"] if response.get("code") == 0 else None

def buff_follow(username, user_id):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    try:
        print(f"🚀 Bắt đầu tăng follow cho @{username}...")
        access = requests.get('https://tikfollowers.com/free-tiktok-followers', headers=headers)
        session = access.cookies.get('ci_session', '')
        headers.update({'cookie': f'ci_session={session}'})
        token = access.text.split("csrf_token = '")[1].split("'")[0]

        data = f'{{"type":"follow","q":"@{username}","google_token":"t","token":"{token}"}}'
        search = requests.post('https://tikfollowers.com/api/free', headers=headers, data=data).json()

        if search.get('success'):
            data_follow = search['data']
            data = f'{{"google_token":"t","token":"{token}","data":"{data_follow}","type":"follow"}}'
            send_follow = requests.post('https://tikfollowers.com/api/free/send', headers=headers, data=data).json()

            if send_follow.get('o') == 'Success!' and send_follow.get('success'):
                tiktok_data = get_tiktok_info(username)
                print(f"✨ **TĂNG FOLLOW THÀNH CÔNG** ✨ @ {username}")
                bot.loop.create_task(send_discord_embed(tiktok_data))
            else:
                wait_time = int(send_follow['message'].split('You need to wait for a new transaction. : ')[1].split(' Minutes')[0]) * 60
                waiting_users[user_id] = time.time() + wait_time
                print(f"⏳ Hãy chờ {wait_time // 60} phút trước khi thử lại @{username}.")
                for i in range(wait_time, 0, -10):
                    print(f"⏳ Đang đợi {i // 60} phút {i % 60} giây...")
                    time.sleep(10)
                buff_follow(username, user_id)
        else:
            print(f"❌ Lỗi không xác định khi tăng follow cho @{username}.")
    except:
        print(f"❌ Lỗi không xác định khi tăng follow cho @{username}.")
    finally:
        running_tasks.pop((user_id, username), None)

def run_buff(user_id, username):
    if user_id in waiting_users:
        remaining_time = int(waiting_users[user_id] - time.time())
        if remaining_time > 0:
            print(f"⏳ Bạn vẫn phải chờ {remaining_time // 60} phút trước khi thử lại @{username}.")
            return
        else:
            del waiting_users[user_id]
    
    if (user_id, username) in running_tasks:
        print(f"🚀 Đang tăng follow cho @{username}, vui lòng chờ.")
        return

    future = executor.submit(buff_follow, username, user_id)
    running_tasks[(user_id, username)] = future

@bot.event
async def on_ready():
    print("✅ Bot Discord đã sẵn sàng!")
    user_id = "12345"
    username = "xdhoangg"
    run_buff(user_id, username)

if __name__ == "__main__":
    print("Chương trình đang chạy...")
    bot.run(TOKEN)
