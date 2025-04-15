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

import requests

def ControlLoop(ip: str) -> None:
    path = "C:\\"

    while True:
        try:
            command = input(f"\n┌──({ip}㉿Cyvo)-[{path}]\n└─$ ").strip()

            if command.lower() == "exit":
                print("Exiting control loop.")
                break

            if command.lower().startswith("cd"):
                temp_path = path

                if command.strip() == "cd ..":
                    if "\\" in path.rstrip("\\"):
                        path = "\\".join(path.rstrip("\\").split("\\")[:-1]) + "\\"
                else:
                    new_dir = command[3:].strip().strip("\"")
                    if new_dir.startswith("\\") or ":" in new_dir:
                        new_path = new_dir
                    else:
                        new_path = path + new_dir + "\\"
                    response = requests.post(
                        f"http://{ip}/cmd",
                        data=f'cd "{new_path}" && cd',
                        headers={"Content-Type": "text/plain"},
                        timeout=5
                    )

                    if response.status_code == 200 and "The system cannot find the path specified" not in response.text:
                        path = new_path
                    else:
                        print("Error: Path not found. Staying in current directory.")
                        path = temp_path
                continue

            full_cmd = f'cd "{path}" && {command}'
            response = requests.post(
                f"http://{ip}/cmd",
                data=full_cmd,
                headers={"Content-Type": "text/plain"},
                timeout=5
            )
            print("Response:\n", response.text)

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

if __name__ == "__main__":
    connect_and_run()
