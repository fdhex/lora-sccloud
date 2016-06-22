# import dependencies
import os
import json
from flask import Flask
from flask import request
from flask.ext.mongoengine import MongoEngine
import untangle

# bootstrap the app
app = Flask(__name__)

# check if running in the cloud and set MongoDB settings accordingly
if 'VCAP_SERVICES' in os.environ:
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    mongo_credentials = vcap_services['mongodb'][0]['credentials']
    mongo_uri = mongo_credentials['uri']
else:
    mongo_uri = 'mongodb://localhost/db'

app.config['MONGODB_SETTINGS'] = {
    'host': mongo_uri
}

# bootstrap our app
db = MongoEngine(app)

class XmlBlob(db.Document):
    xml_blob = db.StringField(required=True)

# set the port dynamically with a default of 3000 for local development
port = int(os.getenv('PORT', '3000'))

# our base route which just returns a string
@app.route('/')
def hello_world():
    return 'Congratulations! Welcome to the Swisscom Application Cloud.'

@app.route('/lora', methods=['POST'])
def post_xml():
  # if request.headers['Content-Type'] == 'text/xml':
    # return request.data
    xml_new_blob = request.data
    for xml_obj in XmlBlob.objects:
        xml_obj.delete()
    xml_blob_doc = XmlBlob(xml_blob=xml_new_blob)
    xml_blob_doc.save()
    return 'XML Blob saved'
  # else:
  #   return 'This endpoint requires a text/xml content-type header'

@app.route('/lora', methods=['GET'])
def get_latest_xml():
  if not XmlBlob.objects.first() == None:
    latest_xml_blob = XmlBlob.objects[0].xml_blob
    xml_obj = untangle.parse(latest_xml_blob)
    payload_hex = xml_obj.DevEUI_uplink.payload_hex.cdata
    dev_eui = xml_obj.DevEUI_uplink.DevEUI.cdata
    time = xml_obj.DevEUI_uplink.Time.cdata
    msg = 'Received payload: {0} with DevEUI: {1} and time: {2}'.format(payload_hex, dev_eui, time)
    return msg
  else:
    return 'No data saved'

# start the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)