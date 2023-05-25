import pyazurehelper.az_subscription as az_sub


def test_main():
    assert az_sub.check_valid_subscription_id("00000000-0000-0000-0000-000000000000") is not False
