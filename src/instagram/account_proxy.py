import os
import instapy


class InvalidInstagramAccountProxyError(ValueError):
    pass


class InstagramAccountProxy(object):

    def __init__(self, account_name: str = None):
        if account_name is None or account_name == "" or account_name == " "*len(account_name):
            raise InvalidInstagramAccountProxyError(account_name, "is an invalid account!")

        self.username: str = os.environ.get(f"{account_name.upper()}_USERNAME")
        if self.username is None:
            raise InvalidInstagramAccountProxyError(account_name, "is an invalid account!")

        self.password: str = os.environ.get(f"{account_name.upper()}_PASSWORD")
        if self.password is None:
            raise InvalidInstagramAccountProxyError(account_name, "is an invalid account!")


    def get_username(self):
        return self.username

    def get_password(self):
        return self.password


if __name__ == '__main__':
    instagram_account_proxy = InstagramAccountProxy(account_name="WastedMynds")
    session = instapy.InstaPy(
        username=instagram_account_proxy.get_username(),
        password=instagram_account_proxy.get_password()
    )
    session.login()