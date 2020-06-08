#!/usr/bin/env python3
"""
Created on Mar 19

@author: Pablo Carbonell, Melchior du Lac
@description: Query RPViz: pathway visualizer.

"""

import argparse
import tempfile
import os
import logging
import shutil
import docker
import subprocess



##
#
#
def main(inputTar,
         input_format,
         outputHTML):
    docker_client = docker.from_env()
    image_str = 'brsynth/rpvisualiser-standalone:dev'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        shutil.copy(inputTar, tmpOutputFolder+'/input.dat')
        command = ['/home/tool_rpVisualiser.py',
                   '-input',
                   '/home/tmp_output/input.dat',
                   '-input_format',
                   str(input_format),
                   '-output',
                   '/home/tmp_output/output.dat']
        container = docker_client.containers.run(image_str,
                                                 command,
                                                 detach=True,
                                                 stderr=True,
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        err_str = err.decode('utf-8')
        print(err_str)
        if not 'ERROR' in err_str:
            shutil.copy(tmpOutputFolder+'/output.dat', outputHTML)
        container.remove()




##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper for galaxy to generate HTML')
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-input', type=str)
    parser.add_argument('-output', type=str)
    params = parser.parse_args()
    main(params.input, params.input_format, params.output)
