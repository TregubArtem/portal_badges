import random
import time

import requests
import urllib3

from classes import Sender, Credentials
from parser import PortalPageParser
from utils import read_file_by_lines, get_random_item


def get_credentials():
    result = Credentials()

    file = open("credentials.txt", "r")

    result.method = file.readline().strip()
    result.domain = file.readline().strip()
    result.endpoint_badges = file.readline().strip()
    result.endpoint_profile = file.readline().strip()
    result.key_recipient = file.readline().strip()
    result.key_badge = file.readline().strip()
    result.key_message = file.readline().strip()
    result.key_token = file.readline().strip()
    result.prefix_cookie = file.readline().strip()

    file.close()

    return result


def get_senders():
    result = []

    file = open("senders.txt", "r")

    while True:
        profile_id = file.readline().strip()

        if len(profile_id) == 0:
            break

        token = file.readline().strip()
        cookie = file.readline().strip()

        result.append(Sender(profile_id, token, cookie))

    file.close()

    random.shuffle(result)

    return result


def get_recipients_profile_ids(senders):
    result = []

    for sender in senders:
        result.append(sender.profile_id)

    random.shuffle(result)

    return result


def get_badges():
    result = [8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 26, 27, 28, 29, 38, 39]

    random.shuffle(result)

    return result


def send_request(credentials, attempt):
    try:
        response = requests.request(
            method=credentials.method,
            url=credentials.domain + credentials.endpoint_badges,
            headers=credentials.get_badges_headers(attempt),
            data=credentials.get_data(attempt),
            verify=False
        )
        success = response.status_code == 200

        if success:
            json = response.json()

            success = bool(json.get("status", "false"))
            error = str(json.get("message", ""))

        else:
            error = str(response.status_code)

    except Exception as e:
        success = False
        error = str(e)

    print(
        ("++++" if success else " ---") +
        "\t\t| " + str(attempt.sender) +
        " \t\t| " + str(attempt.recipient) +
        " \t\t\t| " + str(attempt.badge) +
        " \t\t| " + str(attempt.message) +
        ("" if success else "\t\t<<<\t<<<\t" + error)
    )

    time.sleep(1)

    return success


def get_points(credentials, senders):
    result = ""

    parser = PortalPageParser(credentials)

    for sender in senders:
        result += parser.get_points(credentials, sender)
        result += "\t\t"

    return result


def main():
    credentials = get_credentials()

    senders = get_senders()
    recipients = []

    badges = get_badges()
    replicas = read_file_by_lines("replicas.txt", True)
    messages = []

    attempts_all = 0
    attempts_success = 0

    points_before = get_points(credentials, senders)

    print("success\t\t|sender\t\t| recipient\t\t| badge\t\t| message")
    print("------------|-----------|---------------|-----------|-------------------------")

    for _ in badges:
        for sender in senders:
            if sender.can_send_more(badges):
                attempts_all += 1

                if len(recipients) <= 1:
                    recipients = get_recipients_profile_ids(senders)

                if len(messages) == 0:
                    messages = read_file_by_lines("messages-ru.txt", True)

                replica = get_random_item(replicas, False)
                message = get_random_item(messages, True)

                attempt = sender.new_attempt(badges, recipients)
                attempt.message = replica + " " + message
                attempt.is_request_success = send_request(credentials, attempt)

                if attempt.is_request_success:
                    attempts_success += 1

    print("\nATTEMPTS:\t" + str(attempts_all) + "\nSUCCESS:\t" + str(attempts_success))

    points_after = get_points(credentials, senders)

    print("\nRESULTS:")
    print(points_before)
    print(points_after)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

main()
