import requests

print("Please input your cookie")
auth_cookie = input()

def get_message_ids(num):
    url = f"https://privatemessages.roblox.com/v1/messages?pageNumber={num}&pageSize=20&messageTab=Inbox"

    headers = {
        "Cookie": f".ROBLOSECURITY={auth_cookie}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        message_ids = [message["id"] for message in data["collection"]]
        return message_ids
    else:
        print(f"Failed to fetch messages: {response.status_code}")
        return []

def mark_messages_as_read(message_ids):
    url = "https://privatemessages.roblox.com/v1/messages/mark-read"
    s = requests.session()
    s.cookies[".ROBLOSECURITY"] = auth_cookie
    s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login").headers['X-CSRF-TOKEN']
    headers = {
        "Cookie": f".ROBLOSECURITY={auth_cookie}",
    }

    data = {
        "messageIds": message_ids
    }
    response = s.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"Messages marked as read successfully (PAGE {num+1}).")
    else:
        try:
            error_data = response.json()
            error_message = error_data["errors"][0]["message"]
            print(f"Failed to mark messages as read: {response.status_code} - {error_message}")
        except:
            print(f"Failed to mark messages as read: {response.status_code}")

def get_total_messages_because_im_retarded(auth_cookie, page):
    url = f'https://privatemessages.roblox.com/v1/messages?pageNumber={page}&pageSize=20&messageTab=Inbox'
    headers = {'Cookie': f'.ROBLOSECURITY={auth_cookie}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["totalPages"]
    else:
        print(f"Error: Unable to fetch messages. Status Code: {response.status_code}")
        return None

total_pages = get_total_messages_because_im_retarded(auth_cookie, 1)
num = 0
while not num+1 == total_pages:
    message_ids = get_message_ids(num)
    if message_ids:
        mark_messages_as_read(message_ids)
    num+=1