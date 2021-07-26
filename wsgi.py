
import json
import os
from frontend import init_app, socketio

app = init_app()

if __name__=='__main__':

	#os.environ['GEVENT_SUPPORT'] = 'True'

	#app.run(debug=True, port=1000)
	socketio.run(app, host="0.0.0.0",  debug=True, port=1000)

	# para verificar en linux: ss -tulpn
