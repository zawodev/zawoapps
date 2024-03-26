from requests import post
from json import loads
from time import sleep
wbc = dict()

def getList():
    global wbc
    with open("webhook.json","r") as wbf:
        wl = loads(wbf.read())
        wbf.close()
    wbc = wl["webhook_content"]
    return wl["webhookList"]


def sendWebhookMessage(wb):
    data = {
        "avatar_url":wbc["avatar_url"],
        "username":wbc["username"],
        "content":wbc["message"]
    }
    rs = post(wb,json=data)
    if rs.status_code == 429:
        print(f"rate limit :pensive: zostalo {rs.json()['retry_after']} ")

webhookList = getList()
while True:
    for wb in webhookList:
        sendWebhookMessage(wb)
        sleep(0.5)