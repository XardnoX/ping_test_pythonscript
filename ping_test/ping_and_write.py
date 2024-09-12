import os

def ping_test():
    # The target you want to ping
    target = "google.com"

    # Set the number of pings and reduce delay by reducing timeout (-w option)
    response = os.popen(f"ping -n 15 -w 50 {target}").read()  # 100ms timeout

    # Write the response to a file
    with open("ping_result.txt", "w") as file:
        file.write(response)

if __name__ == "__main__":
    ping_test()