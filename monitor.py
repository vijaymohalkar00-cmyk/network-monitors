import os

def check_host(ip):
    response = os.system(f"ping -c 1 {ip}")
    return "UP" if response == 0 else "DOWN"

if __name__ == "__main__":
    print(check_host("8.8.8.8"))
