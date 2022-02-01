oneksi proxy ada di bawahnya.

PETUNJUK: Periksa url Anda. country=CH yang pertama mungkin harus mengatakan country=CN dan country=AT mungkin harus mengatakan country=AR. Kode saya mencerminkan itu.

from bs4 import BeautifulSoup
import requests
import json
import time

# LIST OF FREE PROXY APIS, THESE PROXIES ARE LAST TIME TESTED 50 MINUTES AGO
# PROTOCOLS: HTTP, HTTPS, SOCKS4 AND SOCKS5
list_of_proxy_content = [
    "https://proxylist.geonode.com/api/proxy-list?limit=150&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=50&country=CN&protocols=http%2Chttps%2Csocks4%2Csocks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=150&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=50&country=FR&protocols=http%2Chttps%2Csocks4%2Csocks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=150&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=50&country=DE&protocols=http%2Chttps%2Csocks4%2Csocks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=1500&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=50&country=AR&protocols=http%2Chttps%2Csocks4%2Csocks5",
    "https://proxylist.geonode.com/api/proxy-list?limit=150&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=50&country=IT&protocols=http%2Chttps%2Csocks4%2Csocks5",
]


# EXTRACTING JSON DATA FROM THIS LIST OF PROXIES
full_proxy_list = []
for proxy_url in list_of_proxy_content:

    proxy_json = requests.get(proxy_url).text
    proxy_json = json.loads(proxy_json)
    proxy_json = proxy_json["data"]

    full_proxy_list.extend(proxy_json)

    if not full_proxy_list:
        print("No proxies to check. Exiting...")
        exit
    else:
        print(f"Found {len(full_proxy_list)} proxy servers. Checking...\n")

# CREATING PROXY DICT
final_proxy_list = []
for proxy in full_proxy_list:

    # print(proxy)  # JSON VALUE FOR ALL DATA THAT GOES INTO PROXY

    protocol = proxy["protocols"][0]
    ip_ = proxy["ip"]
    port = proxy["port"]

    proxy = {
        "https": protocol + "://" + ip_ + ":" + port,
        "http": protocol + "://" + ip_ + ":" + port,
    }

    final_proxy_list.append(proxy)

# TRYING PROXY ON 3 DIFERENT WEBSITES
for proxy in final_proxy_list:

    print(proxy)
    try:
        # Use ipinfo.io to test proxy ip
        url = "https://ipinfo.io/json?token=67e01402d14101"
        r0 = requests.get(url, proxies=proxy, timeout=15)

        if r0.status_code == 200:
            # The 3-line block below only works on ipinfo.io
            output = r0.json()
            real_ip = output["ip"]
            print(f"GOOD PROXY [IP = {real_ip}] {proxy}\n")

            # Do something with the response
            html_page = r0.text
            soup = BeautifulSoup(r0.text, "html.parser")
            print(soup, "\n")

            r0.close()  # close the connection so it can be reused

            # Break out of the proxy loop so we do not send multiple successful
            # requests to the same url. Info needed was already obtained.
            # Comment out to check all possible proxies during testing.
            break
        else:
            # If the response code is something other than 200,
            # it means the proxy worked, but the website did not.
            print(f"BAD URL: [status code: {r0.status_code}]\n{r0.headers}\n")
            r0.close()

        time.sleep(5)  # Don't overload the server

    except Exception as error:
        print(f"BAD PROXY: Reason: {str(error)}\n")
