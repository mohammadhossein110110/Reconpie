
from bs4 import BeautifulSoup
import requests
import dns.resolver
import socket
#import nmap
import re
import whois
import argparse
from urllib.parse import urlparse
import csv
 
#python main.py --text varzesh3.com
#python main.py --text digikala.com
#python main.py --text time.ir
#python main.py --text torob.com
#https://torob.com/browse/736/%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D9%87%D9%85%D8%B1%D8%A7%D9%87-%D8%A7%D9%88%D9%84/


parser = argparse.ArgumentParser(description='Process some inputs.')
parser.add_argument('--text', type=str, help='process some text')
args = parser.parse_args()

if args.text is not None:
    response = requests.get('https://www.' + args.text + '/')
else:
    print("Error: No value provided for --text argument.")



response = requests.get('https://www.' +args.text +'/')
domain = args.text
ip = "185.13.228.162"






# # # Dar Ovordan Link Haye Ba Pasvand Http Toye Code HTML Va Moratab Kardan An Ba BeautifulSoup
# def get_page_links():
#     soup = BeautifulSoup(response.content, "html.parser")
#     links = []
#     for link in soup.find_all("a"):
#         href = link.get("href")
#         if href is not None and href.startswith("http"):
#             links.append(href)
#     return links
    




# # # Dar Ovordan Link Haye Ba Pasvand Http Toye Code HTML Va Moratab Kardan An Ba BeautifulSoup
 
def get_AllLinks(url, depth, links_list): 
    if depth == 0: 
        return 
    try: 
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, 'html.parser') 
        links = soup.find_all('a', href=True) 
        for link in links: 
            links_list.append(link['href']) 
            get_AllLinks(link['href'], depth-1, links_list) 
    except Exception as e: 
        print(e)
        



print("-------------------------------------------------------------")











# Check Kardan Dorost Bodan Ya Nabodan Subdomain Ha. Ke Try Baes Mishe Az For Kharej Nashe Agar Subdomain Nabod
def dns_answers(domain, subdomain_name):
    try:
        answers = dns.resolver.query(subdomain_name + "." + domain, "A")
        for ip in answers:
            print(f"{subdomain_name}.{domain} - {ip}")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        print(f"No answer for {subdomain_name}.{domain}")


print("-------------------------------------------------------------")






# Khondan Subdomain Ha Baraye Test Az Roye sub.txt
def subdomain_txt():
    domain = args.text
    with open("Word/sub.txt", "r", encoding="utf-8") as f:
        for subdomain_name in f.readlines():
            subdomain_name = subdomain_name.strip()
            dns_answers(domain, subdomain_name)


    print("-------------------------------------------------------------")





# Agar Status Code Ba Har Kodom Az Adad Barabar Bod Va Elam Kardan Dashtam Error Ya Nadashtan An
def status_code():
    if response.status_code == 200:
         print("200 => Success!")
    elif response.status_code == 404:
        print("404 => Page not found.")
    elif response.status_code == 500:
        print("500 => Internal server error.")
    else:
        print("Unknown status code:", response.status_code)
    
    print("-------------------------------------------------------------")






# Dar Ovordan IP domain
def ip_address():
    ip_address = socket.gethostbyname(domain)
    print(f"The IP address of {domain} is {ip_address}")

    print("-------------------------------------------------------------")






# Scan Kardan Port Haye IP
def ports_scan():
    common_ports = [21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 194, 443, 445, 993, 995]

    for port in common_ports:  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print("Port {} is open".format(port))
        else:
            print("Port {} is closed".format(port))
    
    sock.close()

    print("-------------------------------------------------------------")








def regex(): 
    # Regex Email 
    response = requests.get('https://www.' +args.text +'/') 
    html_content = response.text 
 
    pattern_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" 
    emails = re.findall(pattern_email, html_content) 
    
    if emails: 
        for email in emails: 
            print(email) 
    else: 
        print("No email found") 
 

    # Regex Number 
    pattern_phonenumber = r"(\b09\d{9}\b)" 
    phones = re.findall(pattern_phonenumber, html_content) 

    if phones: 
        for phone in phones: 
            print(phone) 
    else: 
        print("No phone number found") 

    print("-------------------------------------------------------------")









# Ba Estefade Az Whois Etela'at An Site Morede Nazar Ra Az Jomle Address Email, Nam Malek, Zaman Kharid Damanae Va ... Be Dast Miayad
def who_is():
    who = whois.whois(domain)
    print(who)

    print("-------------------------------------------------------------")






url = 'https://www.' + args.text
depth = 3
links_list = []





get_AllLinks(url, depth, links_list)
# داده‌هایی که برای نوشتن به فایل CSV نیاز داریم
data = [['url']]  # عنوان ستون

# اضافه کردن لینک‌ها به داده‌ها
for link in links_list:
    data.append([link])

# نام فایل CSV
filename = "example.csv"

# نوشتن داده‌ها به فایل CSV
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    # ایجاد یک شیء نویسنده CSV
    csvwriter = csv.writer(csvfile)

    # نوشتن ردیف‌های داده
    csvwriter.writerows(data)







#python main.py --text time.ir
#python main.py --text torob.com



#crawl_site()
#links = get_page_links()
#print(links)
get_AllLinks(url, depth, links_list)
subdomain_txt()
status_code()
ip_address()
ports_scan()
regex()
who_is()
#argument()