import os
import time
import urllib.request
import datetime

notificationSent = False

websiteName = "sarimahmed.tech"


def sendNotification():
    global notificationSent
    global notificationSentAt

    if notificationSent:
        if notificationSentAt + (15 * 60) <= datetime.datetime.now().timestamp():
            os.system(
                f'notify-send "⚠️  Website Changed ⚠️ " "{websiteName}\'s homepage has a problem, check it out."'
            )
            notificationSentAt = datetime.datetime.now().timestamp()

        else:
            pass
    else:
        os.system(
            f'notify-send "⚠️  Website Changed ⚠️ " "{websiteName}\'s homepage has a problem, check it out."'
        )

        notificationSent = True
        notificationSentAt = datetime.datetime.now().timestamp()


def setCurrentAsLastState():
    lastStateFile = open("lastState.txt", "w")

    currentState = (
        str(urllib.request.urlopen(f"https://{websiteName}").read())
        .replace(" ", "")
        .replace("\n", "")
    )

    lastStateFile.write(currentState)

    lastStateFile.close()


while True:
    # time.sleep(60 * 15)
    time.sleep(1)
    try:
        lastStateFile = open("lastState.txt", "r")

        lastState = str(lastStateFile.read()).replace(" ", "").replace("\n", "")

        try:
            connection = urllib.request.urlopen(f"https://{websiteName}", timeout=5)
            currentState = str(connection.read()).replace(" ", "").replace("\n", "")

            if currentState == lastState:
                print("All Good.")
                notificationSent = False
            else:
                sendNotification()
                print("Not Good.")
        except Exception as ex:
            print(ex)
            print("Disconnection")
            connection.close()

    except FileNotFoundError:
        setCurrentAsLastState()
