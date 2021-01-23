import random


class Attempt:
    def __init__(self, sender, recipient_id, badge_id):
        self.sender = sender.profile_id
        self.recipient = recipient_id
        self.badge = badge_id
        self.message = ""

        self.token = sender.token
        self.cookie = sender.cookie

        self.is_request_success = False

    def __str__(self):
        return "Attempt{" \
               + self.sender \
               + "; " + self.recipient \
               + "; " + self.badge \
               + "; " + self.message \
               + "; " + str(self.is_request_success) \
               + "}"


class Sender:
    def __init__(self, profile_id, token, cookie):
        self.profile_id = profile_id
        self.token = token
        self.cookie = cookie
        self.attempts = dict()
        self.recipients_rating = dict()

    def __str__(self):
        return "Sender{" + self.profile_id + "; " + self.token + "}"

    def can_send_more(self, badges):
        return len(self.attempts) < len(badges)

    def new_attempt(self, badges, recipients):
        while True:
            badge_index = random.randint(0, len(badges) - 1)
            badge = badges[badge_index]

            attempt = self.attempts.get(badge)

            if attempt is None:
                while True:
                    recipient_index = random.randint(0, len(recipients) - 1)
                    recipient = recipients[recipient_index]

                    if recipient != self.profile_id:
                        recipient_rating = self.recipients_rating.get(recipient)
                        if recipient_rating is None:
                            recipient_rating = 0

                        minimum_rating = len(recipients)

                        for value in self.recipients_rating.values():
                            if value < minimum_rating:
                                minimum_rating = value

                        if recipient_rating <= minimum_rating:
                            self.recipients_rating[recipient] = recipient_rating + 1

                            attempt = Attempt(self, recipient, badge)
                            self.attempts[badge] = attempt

                            return attempt


class Credentials:
    def __init__(self):
        self.method = ""
        self.domain = ""
        self.endpoint_badges = ""
        self.endpoint_profile = ""
        self.key_recipient = ""
        self.key_badge = ""
        self.key_message = ""
        self.key_token = ""
        self.prefix_cookie = ""

    def __str__(self):
        return "Credentials{" \
               + self.method \
               + "; " + self.domain \
               + "; " + self.endpoint_badges \
               + "; " + self.key_recipient \
               + "; " + self.key_badge \
               + "; " + self.key_message \
               + "; " + self.key_token \
               + "; " + self.prefix_cookie \
               + "}"

    def get_badges_headers(self, attempt):
        return {
            "Cookie": self.prefix_cookie + "=" + str(attempt.cookie)
        }

    def get_profile_headers(self, sender):
        return {
            "Cookie": self.prefix_cookie + "=" + str(sender.cookie)
        }

    def get_data(self, attempt):
        return {
            self.key_recipient: str(attempt.recipient),
            self.key_badge: str(attempt.badge),
            self.key_message: str(attempt.message),
            self.key_token: str(attempt.token)
        }
