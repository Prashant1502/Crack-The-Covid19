import flask
import pandas as pd
import pgeocode
import geopy.distance

app = flask.Flask(__name__, template_folder='templates')

@app.route('/')
def main():
    if flask.request.method == "GET":
        return(flask.render_template('test1.html'))
    
@app.route('/', methods=['POST'])
def getQuery():
    query = flask.request.form['query']
    df_icmrlab = pd.read_csv("C://Users//Administrator//Desktop//Project//webapp//model//ICMRLabDetails.csv")
    nomi = pgeocode.Nominatim('in')
    df_query = nomi.query_postal_code(query)
    lat = df_query.latitude
    lon = df_query.longitude
    query_point = (lat,lon,0.0)
    index = 0
    count = 0
    min_dis = 100000.0
    for itr in df_icmrlab['location']:
        res = itr[1:-1]
        res = tuple(map(float, res.split(',')))
        dis = geopy.distance.geodesic(query_point, res).km
        if dis<min_dis:
            min_dis = dis
            index = count
        count+=1
    near_lab = df_icmrlab.loc[index,'address']
    Type = df_icmrlab.loc[index,'type']
    min_dis = "{:.2f}".format(min_dis)
    city = df_icmrlab.loc[index,'city']
    state = df_icmrlab.loc[index,'state']


    return flask.render_template('test1.html',original_input={'query':query}, dist=min_dis, result=near_lab, unit="kms",Type=Type,Min_Dist="Minimum Distance from your pin code is: ",Lab="The nearest lab is: ",Type_of="Type of lab: ",City_of="City: ",City=city,State_of="State: ",State=state)

if __name__ == '__main__':
    app.run()
