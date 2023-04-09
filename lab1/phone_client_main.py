from phone_client import PhoneClient

client = PhoneClient()

while True:
    command = input("Type API command:")

    if command.startswith("HELP"):
        print("HELP - list of methods\n GET <name> - get phone number of person\n GETALL - all numbers\n EXIT - close client")
    elif command.startswith("GETALL"):
        client.getall()
    elif command.startswith("GET"):
        name = command.split()[1]
        client.get(name)
    elif command.startswith("EXIT"):
        client.close()
        break
    else:
        print("Command is undefined")