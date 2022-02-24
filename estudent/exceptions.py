
class LoginError(Exception):
    def __init__(self, response=None):
        self.response = response
        msg = 'Login failed. Check your student ID and password are correct. If your network is slow, increase timeout in estudent/client.py.'
        super().__init__(msg)
