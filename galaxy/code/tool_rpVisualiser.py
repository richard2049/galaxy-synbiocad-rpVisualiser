#!/usr/bin/env python3
"""
Created on Mar 19

@author: Pablo Carbonell, Melchior du Lac
@description: Query RPViz: pathway visualizer.

"""
import argparse
import io
import os
import json
import tarfile
import glob
import logging

import shutil
import tarfile
import tempfile
import subprocess
import random

import sys 
sys.path.insert(0, '/home/') 

'''
python -m rpviz.cli 6999994565578834569.tar temp_f/ --autonomous_html temp_f/testetst.html
'''
def main(fi_input, input_format, fi_output):
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        if input_format=='tar':
            subprocess.call(['python', '-m', 'rpviz.cli', fi_input, tmpOutputFolder, 
                '--autonomous_html', os.path.join(tmpOutputFolder, 'autonomous.html')])
        elif input_format=='sbml':
            with tempfile.TemporaryDirectory() as tmpInputFolder:
                inputTar = tmpInputFolder+'/tmp_input.tar.xz'
                with tarfile.open(inputTar, mode='w:gz') as tf:
                    info = tarfile.TarInfo('single.rpsbml.xml') #need to change the name since galaxy creates .dat files
                    info.size = os.path.getsize(fi_input)
                    tf.addfile(tarinfo=info, fileobj=open(fi_input, 'rb'))
                subprocess.call(['python', '-m', 'rpviz.cli', inputTar, tmpOutputFolder, 
                    '--autonomous_html', os.path.join(tmpOutputFolder, 'autonomous.html')])
        else:
            logging.error('Cannot identify the input/output format: '+str(input_format))
            return False
        shutil.copy(os.path.join(tmpOutputFolder, 'autonomous.html'), fi_output)


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
