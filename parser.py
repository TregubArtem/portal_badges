import requests
from pyquery import PyQuery


class PortalPageParser:
    def __init__(self, credentials):
        self.domain = credentials.domain
        self.endpoint = credentials.endpoint_profile

    def get_points(self, credentials, sender):
        html = requests.get(
            url=self.domain + self.endpoint + str(sender.profile_id),
            headers=credentials.get_profile_headers(sender),
            verify=False
        ).text

        query = PyQuery(html)

        name = query(".personal-name__title").text().split(" ")[0]
        points = query(".profile__user--points").text()

        return str(name) + ":\t" + str(points)
