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

import sys 
sys.path.insert(0, '/home/rpviz/') 

## Hack to have a single HTML file
#
#
def makeSingleHTML(input_folder):
    #find and open the index file 
    htmlString = open(input_folder+'/index.html', 'rb').read() 
    #open and read JS files and replace them in the HTML
    jsReplace = ['js/jquery-3.4.1.min.js', 
                 'js/cytoscape-3.12.1.min.js', 
                 'js/jquery-ui-1.12.1.min.js',
                 'js/chroma-2.1.0.min.js',
                 'js/jquery.tablesorter-2.31.2.min.js',
                 'js/dagre-0.8.5.min.js',
                 'js/cytoscape-dagre-2.2.1.js',
                 'js/viewer.js']
    for js in jsReplace:
        jsString = open(input_folder+'/'+js, 'rb').read()
        ori = b'src="'+js.encode()+b'">'
        rep = b'>'+jsString
        htmlString = htmlString.replace(ori, rep)
    #open and read style.css and reaplce it in the HTML
    cssReplace = ['css/jquery.tablesorte.theme.default-2.31.2.min.css',
                  'css/viewer.css']
    for css in cssReplace:
        cssBytes = open(input_folder+'/css/viewer.css', 'rb').read() 
        ori = b'<link href="'+css.encode()+b'" rel="stylesheet" type="text/css"/>'
        rep = b'<style type="text/css">'+cssBytes+b'</style>'
        htmlString = htmlString.replace(ori, rep)
    ### replac the network
    netString = open(input_folder+'/network.json', 'rb').read()
    ori = b'src="'+'network.json'.encode()+b'">'
    rep = b'>'+netString
    htmlString = htmlString.replace(ori, rep)
    return htmlString


def main(fi_input, input_format, fi_output):
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        if input_format=='tar':
            subprocess.call(['python', '-m', 'rpviz.cli', fi_input, tmpOutputFolder])
        elif input_format=='sbml':
            with tempfile.TemporaryDirectory() as tmpInputFolder:
                inputTar = tmpInputFolder+'/tmp_input.tar.xz'
                with tarfile.open(inputTar, mode='w:gz') as tf:
                    info = tarfile.TarInfo('single.rpsbml.xml') #need to change the name since galaxy creates .dat files
                    info.size = os.path.getsize(fi_input)
                    tf.addfile(tarinfo=info, fileobj=open(fi_input, 'rb'))
                subprocess.call(['python', '-m', 'rpviz.cli', inputTar, tmpOutputFolder])
        else:
            logging.error('Cannot identify the input/output format: '+str(input_format))
        with open(fi_output, 'wb') as outF:
            outF.write(makeSingleHTML(tmpOutputFolder))


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
