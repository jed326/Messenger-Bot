import json

with open('group_chat.json', 'r') as file:
    data = json.load(file)

    participants = data['participants']
    messages = data['messages']

    with open('input/everyone.txt', 'a+') as output:
        for message in messages:
            text = message.get('content', "")
            if text != "":
                output.write("%s\n" % text)

    for person in participants:
        name = person["name"]
        name_file = name.replace(" ", "")

        with open('input/%s.txt' % name_file, 'a+') as output:
            for message in messages:
                if message['sender_name'] == name:
                    text = message.get('content', "")
                    if text != "":
                        output.write("%s\n" % text)
