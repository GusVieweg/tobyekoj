def myjsonPutRequest(endpoint, data):
	myjsonEndPoint = "https://api.myjson.com/bins/eiums"
	data = {"row":lastRow}
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
	requests.put(myjsonEndPoint, json=data, headers=headers)