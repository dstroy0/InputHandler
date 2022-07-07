import json

sub_dict = {"a": 1, "b": 2}
data = {"1": {**sub_dict}, "2": {**sub_dict}}
print(json.dumps(data, indent=2), "\n")
data["1"]["a"] = 2
print(json.dumps(data, indent=2), "\n")
data["2"]["a"] = 2
print(json.dumps(data, indent=2), "\n")
data["1"]["b"] = 1
print(json.dumps(data, indent=2), "\n")
data["2"]["b"] = 1
print(json.dumps(data, indent=2), "\n")
