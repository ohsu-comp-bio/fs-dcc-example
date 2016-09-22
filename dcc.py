from flask import Flask, request, jsonify, Response
import requests
import json
app = Flask(__name__)

@app.route('/v1/projects', methods = ['GET'])
def projectsList():

  #http://$(docker-machine ip icgc):5000/dataframe/transpose/57e2cab4b526284a625657c6

  r = requests.get('http://192.168.99.100:5000/keyspaces?names=ICGC-Project')
  ksid = json.loads(r.content)['keyspaces'][0]['id']

  r = requests.get('http://192.168.99.100:5000/dataframes?keyspaceIds='+str(ksid))
  dfid = json.loads(r.content)['dataframes'][0]['id']

  r = requests.get('http://192.168.99.100:5000/dataframe/transpose/'+str(dfid))

  fsdict = json.loads(r.content)
  content = {'hits':[{k:v} for k,v in fsdict["contents"].items()]}

  resp = Response(str(content))

  resp.headers['last-modified'] = 'filler time'
  resp.headers['cache-control'] = 'max-age: filler' 

  return resp


if __name__ == '__main__':
    app.run(debug=True)
