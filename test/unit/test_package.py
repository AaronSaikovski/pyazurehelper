import pyazuretoolkitaz_subscription as az_sub


def test_main():
    sub_test_str: str = "00000000-0000-0000-0000-000000000000"
    assert az_sub.check_valid_subscription_id(sub_test_str) is not False
