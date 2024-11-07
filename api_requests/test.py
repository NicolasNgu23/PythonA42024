from requests import Session, HTTPError

class TEST():
    def __init__(self):
        self.session = Session()
        self.base_url = "https://19wkp9x12d.execute-api.eu-west-1.amazonaws.com/dev"
        self.api_key = "a28c9ecb-6257-477b-8dc7-e0dfbd73d0a1aa"

    def get_user(self):
        res = self.session.get(
            url=f"{self.base_url}/manageUser"
        )
        print("Response Text:", res.text)

    def get_token(self, email):
        headers = {
            'x-api-key': self.api_key,
            'email': email
        }
        res = self.session.get(
            url=f"{self.base_url}/manageEmail",
            headers=headers
        )
        print("Response Text:", res.text)
        print("Status Code:", res.status_code)


test = TEST()
test.get_user()
test.get_token("user_a86342c9-53e5-4780-9220-be129a38e021@example.com")
