import os
import sys
import httpx
from colorama import Fore, init
import json

init(autoreset=True)

fr = Fore.RED
fg = Fore.GREEN
fy = Fore.YELLOW
fw = Fore.WHITE
fre = Fore.RESET

proxy_sources = [
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt',
    'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
    'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt',
    'https://api.openproxylist.xyz/http.txt',
    'https://api.proxyscrape.com/v2/?request=displayproxies',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
    'https://www.proxydocker.com/en/proxylist/download?email=noshare&country=all&city=all&port=all&type=all&anonymity=all&state=all&need=all',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous',
    'http://worm.rip/http.txt',
    'https://proxyspace.pro/http.txt',
    'https://multiproxy.org/txt_all/proxy.txt',
    'https://proxy-spider.com/api/proxies.example.txt',
    'https://yeuem.online/sex?api=toibigay',
    'https://proxy.scdn.io/text.php'
]

if __name__ == "__main__":
    file = "proxy.txt"
    
    try:
        if os.path.isfile(file):
            os.system('cls' if os.name == 'nt' else 'clear')
            os.remove(file)
            print(f"{fr}File {file} đã tồn tại!\n{fy}Bắt đầu tải xuống {file} mới!\n")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{fy}Bắt đầu tải xuống {file}!\n")

        with open(file, 'a') as data:
            for proxy in proxy_sources:
                try:
                    response = httpx.get(proxy)
                    if proxy == 'https://yeuem.online/sex?api=toibigay':  # Xử lý API JSON đặc biệt
                        json_data = response.json()
                        if json_data["code"] == 0:
                            for key in json_data["data"]:
                                for proxy_address in json_data["data"][key]:
                                    data.write(proxy_address + '\n')
                    else:
                        data.write(response.text)
                    print(f" -| Đang lấy {fg}{proxy}{fre}")
                except Exception as e:
                    print(f"{fr}Lỗi khi lấy {proxy}: {str(e)}{fre}")
                    continue

        with open(file, 'r') as count:
            total = sum(1 for line in count)
        print(f"\n{fw}( {fy}{total}{fw} ) {fg}Proxy đã được tải xuống thành công.{fre}")
    
    except Exception as e:
        print(f"{fr}Lỗi xảy ra: {str(e)}{fre}")
        sys.exit(1)