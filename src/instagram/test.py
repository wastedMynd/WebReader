from instagram.account_proxy import InvalidInstagramAccountProxyError, InstagramAccountProxy
import pytest


def test_invalid_instagram_account_proxy():

    # region given an account_name = None
    account_name = None
    # endregion

    # region when
    with pytest.raises(InvalidInstagramAccountProxyError):
        InstagramAccountProxy(account_name)
    # endregion when

    # region given an account_name = ""
    account_name = ""
    # endregion

    # region when
    with pytest.raises(InvalidInstagramAccountProxyError):
        InstagramAccountProxy(account_name)
    # endregion when

    # region given an account_name = "     "
    account_name = "     "
    # endregion

    # region when
    with pytest.raises(InvalidInstagramAccountProxyError):
        InstagramAccountProxy(account_name)
    # endregion when

    # region given an account_name = "invalid_account_does_not_exists"
    account_name = "invalid_account_does_not_exists"
    # endregion

    # region when
    with pytest.raises(InvalidInstagramAccountProxyError):
        InstagramAccountProxy(account_name)
    # endregion when


def test_valid_instagram_account_proxy():
    # region given an account_name = "WastedMynd"
    account_name = "WastedMynds"
    # endregion

    # region  when, InstagramAccountProxy(account_name) is constructed
    account_proxy = InstagramAccountProxy(account_name)
    # endregion

    # region then:
    assert account_proxy is not None
    assert type(account_proxy.get_username()) == str and len(account_proxy.get_username()) > 0
    assert type(account_proxy.get_password()) == str and len(account_proxy.get_password()) > 0
    #  endregion then
