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

def ControllLoop(ip: str) -> None:
    while True:
        prompt = input(f"""
┌──({ip}㉿Cyvo)-[~]
└─$ """)
        
        if prompt.strip().lower() == "exit":
            break

def MainLoop(ip: str) -> None:
    while True:
        prompt: str = input("[+]: ")

        if prompt.strip().lower() == "exit":
            break



try:
    ip: str = input("Enter the target IP: ")
    print(f"Connecting to {ip}")
    response = requests.get(f"http://{ip}:6789", timeout=5)
    if response.status_code == 200:
        print("Connection Succeed")
        MainLoop(ip)
    else:
        print(f"Connection failed with status code: {response.status_code}")
except requests.RequestException:
    print("Execution Failed")
except KeyboardInterrupt:
    print("\nProcess Cancelled")
