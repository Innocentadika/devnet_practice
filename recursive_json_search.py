from test_data import *

def json_search(key, input_object):
    ret_val = []

    if isinstance(input_object, dict):
        for k, v in input_object.items():  # searching key in the dict
            if k == key:
                temp = {k: v}
                ret_val.append(temp)

            if isinstance(v, dict):
                ret_val.extend(json_search(key, v))

            elif isinstance(v, list):
                for item in v:
                    if not isinstance(item, (str, int)):
                        ret_val.extend(json_search(key, item))

    elif isinstance(input_object, list):
        # Iterate list because some APIs return JSON object in a list
        for val in input_object:
            if not isinstance(val, (str, int)):
                ret_val.extend(json_search(key, val))

    return ret_val


# Example usage (will depend on your test_data content)
print(json_search("issueSummary", data))
