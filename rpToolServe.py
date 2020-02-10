import rpTool
import tempfile
import glob
import os
import tarfile
import io
import logging

from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api

#######################################################
############## REST ###################################
#######################################################


app = Flask(__name__)
api = Api(app)


def stamp(data, status=1):
    appinfo = {'app': 'rpVisualiser', 'version': '1.0',
               'author': 'Thomas Duigou, Melchior du Lac, Pablo Carbonell, Anaelle Badier',
               'organization': 'BRS',
               'time': datetime.now().isoformat(),
               'status': status}
    out = appinfo.copy()
    out['data'] = data
    return out


class RestApp(Resource):
    """ REST App."""
    def post(self):
        return jsonify(stamp(None))
    def get(self):
        return jsonify(stamp(None))


class RestQuery(Resource):
    """ REST interface that generates the Design.
        Avoid returning numpy or pandas object in
        order to keep the client lighter.
    """
    def post(self):
        input_tar_bytes = request.files['input_tar']
        #pass the files to the rpReader
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            with tempfile.TemporaryDirectory() as tmpInputFolder:
                #save the bytes tar into folder
                with open(tmpInputFolder+'/tmp_input.tar', 'wb') as it:
                    it.write(input_tar_bytes.read())
                #run the script
                rpTool.subprocess_run(tmpInputFolder+'/tmp_input.tar', tmpOutputFolder)
                #write the results of the folder into a TAR
                with tarfile.open(tmpInputFolder+'/tmp_output.tar', mode='w:xz') as tf:
                    for file_path in glob.glob(tmpOutputFolder+'/*'):
                        if os.path.isdir(file_path):
                            tf.add(file_path, recursive=True, arcname=file_path.split('/')[-1])
                        else:
                            info = tarfile.TarInfo(file_path.split('/')[-1])
                            info.size = os.path.getsize(file_path)
                            tf.addfile(tarinfo=info, fileobj=open(file_path, 'rb'))     
                return send_file(tmpInputFolder+'/tmp_output.tar', as_attachment=True, attachment_filename='rpVisualiser.tar', mimetype='application/x-tar')


api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True, threaded=True)
