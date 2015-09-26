import urllib, json
from pprint import pprint

with open('crimedata.json') as data_file:
	data = json.load(data_file)

return_data = {}

for arr in data["data"]:
	id_number = arr[0]
	crime_type = arr[10]
	addr = arr[15]
	city = arr[16]
	if addr is None:
		continue
	else:
		address = addr + ", " + city + ","
	key = YOUR_KEY
	address_array = address.split()
	url = "https://maps.googleapis.com/maps/api/geocode/json?address="
	for s in address_array:
		url += s + "+"

	url += "UT&Key=" + key

	response = urllib.urlopen(url)
	new_data = json.loads(response.read())

	if (new_data["status"] == "OK"):
		lat = new_data["results"][0]["geometry"]["location"]["lat"]
		lng = new_data["results"][0]["geometry"]["location"]["lng"]
	elif (new_data["status"] == "OVER_QUERY_LIMIT"):
		print("Over limit. Stopped at number " + id_number)
		break;
	else:
		print("ERROR: " + new_data["status"] + " at: " + id_number)
		break;

	address = address + " UT"
	return_data[id_number] = {}
	return_data[id_number]["crime"] = crime_type
	return_data[id_number]["address"] = address
	return_data[id_number]["lat"] = lat
	return_data[id_number]["lng"] = lng
	print(return_data[id_number])

with open('simpledata.json', 'w') as fp:
    json.dump(return_data, fp)