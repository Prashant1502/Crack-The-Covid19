
import http.client    
conn = http.client.HTTPSConnection("covid-19-data.p.rapidapi.com")

headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "78025ca761mshf56243fdf00bfc3p196952jsnd6c25f4f7dc5"
        }

conn.request("GET", "/help/countries?format=json", headers=headers)

res = conn.getresponse()
data = pd.DataFrame(res)
country_name = data['name'].tolist()