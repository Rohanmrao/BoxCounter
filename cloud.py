import urllib.request
import requests

def prowler_cloud_pull():

	URL='https://api.thingspeak.com/channels/1596814/fields/1.json?api_key='
	KEY='8XU625IJNSHL5LHS'
	HEADER='&results=2'
	NEW_URL=URL+KEY+HEADER

	get_data = requests.get(NEW_URL).json()

	print(NEW_URL)

	fetched_data = get_data['feeds']
   
	cloud_db = []
	timestamp_db = []

	for x in fetched_data:
		cloud_db.append(x['field1'])
		timestamp_db.append(x['created_at'])

	
	for i in range(0,len(cloud_db)):
		print("Retrieved box count:",cloud_db[i],"at",timestamp_db[i])

if __name__ == '__main__':
	
	print("Running Fetch...")
	prowler_cloud_pull()

