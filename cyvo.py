import requests


# Intro
print("""
 ██████╗██╗   ██╗██╗   ██╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██║   ██║██╔═══██╗
██║      ╚████╔╝ ██║   ██║██║   ██║
██║       ╚██╔╝  ╚██╗ ██╔╝██║   ██║
╚██████╗   ██║    ╚████╔╝ ╚██████╔╝
 ╚═════╝   ╚═╝     ╚═══╝   ╚═════╝ 

                                 
Creator: IzanamiiDevv.
""")

def Run_Connection(ip: str) -> None:
    while True:
        prompt = input(f"""
┌──({ip}㉿Cyvo)-[~]
└─$ """)
        if prompt.strip().lower() == "exit":
            break
        else:
            print(f"Command '{prompt}' sent to {ip} (simulation)")

ip: str = input("Enter the target IP: ")
try:
    response = requests.get(f"http://{ip}:8080", timeout=5)
    if response.status_code == 200:
        Run_Connection(ip)
    else:
        print(f"Connection failed with status code: {response.status_code}")
except requests.RequestException:
    print("Execution Failed")
