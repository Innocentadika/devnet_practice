import requests
import hashlib


query_char = str(input("Enter Your Password: "))

def request_api_data (first5_char):
    url = "https://api.pawnedpasswords.com/range/"+first5_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}! Check the API and try again.")
    return res

#Getting hashes that match the response
def get_password_leaks_count(hashes, hash_to_check):
    #creating a tuple
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0

def pawend_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8").hexdigit().upper)
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

leak_count = pawend_api_check(query_char)

if count:
    print(f"Your password hass been leaked {count}time!")
else:
    print("Your password is secure, not leaked in any data breaches.")