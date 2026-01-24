
import requests   # python module that simplifies making web requests
def get_config():
    return requests.get("http://localhost/get_config").content
def set_config(dbhost):
    requests.get("http://localhost/config_action?dbhost="+dbhost)
save_dbhost = ""
def setUp():
    global save_dbhost
    save_dbhost = get_config()
def tearDown():
    global save_dbhost
    set_config(save_dbhost)
def test_setconfig():
    setUp()
    set_config("TESTVAL")
    assert get_config() == "ESTVAL"
    tearDown()
