# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:48:55 2019

@author: anael
"""

import argparse
import os
import csv
from .sbml2lists import sbml2list
from .csv2list_ind import csv2list2
from .network2json import network2
from .py2html import html
from .downloadcsv import downloadcsv
import networkx as nx
import tarfile
import tempfile
import uuid
import shutil,glob
import json

def arguments():
    parser = argparse.ArgumentParser(description='Visualizing a network from sbml')
    parser.add_argument('typeformat', 
                        help='Which format ? sbml/csv')
    parser.add_argument('inputtarfolder', 
                        help='Input folder with sbml files in tar format.')
    parser.add_argument('outfile',
                        help='html file.')
    parser.add_argument('--choice',
                        default="2",
                        help='What kind of input do you want ? \n 1/Single HTML file \n 2/Separated HTML files \n 3/View directly in Cytoscape \n 4/Generate a file readable in Cytoscape \n')
    parser.add_argument('--selenzyme_table',
                        default="N",
                        help='Do you want to display the selenzyme information ? Y/N')
    parser.add_argument('--filenames',
                        help='import a csv file matching id (CMPD...) and products names')
    return parser
    

def run(tarfolder,outfolder,typeformat="sbml",choice="2",selenzyme_table="N",filenames=''):
    """Main function that runs the tool"""
    print(typeformat)
    
    #Initialization
   
    scores={} #scores (thermodynamics values, FBA...)
    scores_col={} #scores colors (for gradient mapping)
    RdfG_o={}
    RdfG_m={}
    glob_score={}
    Path_flux_value={}
    Length={}
    dict_net={} #dictionary if the user provides a file to match ID and name of intermediate compounds
  
    #CREATE DICT WITH MNX COMPOUNDS ID->NAMES FROM METANETX DB
    reader = csv.reader(open(os.path.join(os.path.dirname(__file__),"chem_prop.tsv")),delimiter="\t")
    d={}
    for i in range(385): #skip 1st rows
        next(reader)
    for row in reader:
        d[row[0]]=list(row[1:])[0] #1st column = CMPD..., 2nd column=name
        
    #IF THERE IS A FILE FOR PRODUCTS NAMES
    try:
        namesdict={}
        with open(filenames, 'r') as csvFile:
                reader = csv.reader(csvFile,delimiter=';')       
                for row in reader:
                    namesdict[row[0]]=row[1] #row 0 : id (CMPD...), row 1 : name
    except:
        namesdict={}
    

    def readoutput(f,output,outfolder):
        """either from libsbml, or from readcsv"""
        G=nx.DiGraph() #new pathway = new network
        LR=output[0]
        Lreact=output[1]
        Lprod=output[2]
        name=output[3]
        species_smiles=output[4]
        reac_smiles=output[5]
        images=output[6] 
        images2=output[7] #small reaction image
        species_names=output[8]
        species_links=output[9] #link to metanetx for metabolic compounds
        roots=output[10] #for target reaction and target molecule
        dic_types=output[11]
        image2big=output[12] #zoom on reaction image
        data_tab=output[13] #selenzyme table 5st rows
        dfG_prime_o=output[14]
        dfG_prime_m=output[15]
        dfG_uncert=output[16]
        flux_value=output[17]
        rule_id=output[18] #RetroRules ID
        rule_score=output[19]
        fba_obj_name=output[20]
        
        RdfG_o[f]=output[21]
        RdfG_m[f]=output[22]
        glob_score[f]=output[23]
        if flux_value !={}:
            Path_flux_value[f]=list(flux_value.values())[-1]
        if 'target_reaction' in roots.keys(): 
            Length[f]=len(LR)-1 #pathway length doesn't include the "target reaction" node
        else :
            Length[f]=len(LR)
        revers=output[24]
        
        
        G=network2(G,LR,Lreact,Lprod,name,species_smiles,reac_smiles,images,\
                   images2,species_names,species_links,roots,dic_types,\
                   image2big,data_tab, dfG_prime_o,dfG_prime_m, dfG_uncert,\
                   flux_value, rule_id,rule_score, fba_obj_name,revers)
        
        #CREATE NETWORK DICTIONNARY
        js = nx.readwrite.json_graph.cytoscape_data(G)
        elements=js['elements']
        dict_net[name]=elements #dictionary with list of nodes and edges
                 
        downloadcsv(outfolder,f,LR,reac_smiles,Lreact,Lprod,species_names,dfG_prime_o,dfG_prime_m,dfG_uncert,flux_value,\
                    rule_id,rule_score,RdfG_o,RdfG_m, glob_score,Path_flux_value,roots)
                
        return(G,name,RdfG_o,RdfG_m,glob_score,Path_flux_value,Length)
        
    #READ AND EXTRACT TARFILE
    try:
        tar = tarfile.open(tarfolder) ##read tar file
        isFolder = False #the input is not a folder but a tar file
    except:
        isFolder = True
    with tempfile.TemporaryDirectory() as tmpdirname:
        if not isFolder:
            print('created temporary directory', tmpdirname) #create a temporary folder
            tar.extractall(path=tmpdirname)
            tar.close()
            infolder=tmpdirname
        else:
            infolder=tarfolder
            tmpdirname=tarfolder #the folder is directly the input, not temporary
       
        #DEPEND ON THE FORMAT
        if typeformat=='sbml':
    
            pathways=os.listdir(infolder) #1 sbml file per pathway
            for f in pathways: 
                print(f)
                file=os.path.join(infolder,f)   
                output=sbml2list(file, selenzyme_table,d,namesdict) #extract info from sbml
                data=readoutput(f, output,outfolder)
                RdfG_o=data[2]
                RdfG_m=data[3]
                glob_score=data[4]
                Path_flux_value=data[5]
                Length=data[6]
              
            
        if typeformat=='csv':
            """Input = output folder from RP2paths"""
            
            # READ CSV FILE WITH PATHWAYS (out_path.csv)
            csvfilepath=os.path.join(tmpdirname,"path","out1","out_paths.csv")
            datapath=[]
            with open(csvfilepath, 'r') as csvFile:
                reader = csv.reader(csvFile)       
                for row in reader:
                    datapath.append(row)
            csvFile.close()
            nbpath=int(datapath[-1][0])
   
            for path in range(1,nbpath+1): #for each pathway
                print(path)
                output=csv2list2(tmpdirname,path, datapath, selenzyme_table,d,namesdict)
                data=readoutput(path, output,outfolder)
                RdfG_o=data[2]
                RdfG_m=data[3]
                glob_score=data[4]
                Path_flux_value=data[5]
                Length=data[6]
                
            pathways=range(1,nbpath+1)
                
            
    scores["dfG_prime_o (kJ/mol)"]=RdfG_o
    scores["dfG_prime_m (kJ/mol)"]=RdfG_m
    scores["Global score"]=glob_score
    scores["flux_value (mmol/gDW/h)"]=Path_flux_value
    scores["length"]=Length
  

    if choice=="2":#view in separated files
        for f in glob.glob(os.path.join(os.path.dirname(__file__),'new_html','*')): #to copy the required files in the outfolder
            shutil.copy(f,outfolder)
        html(outfolder,pathways,scores,scores_col,dict_net)
        os.chdir( outfolder )
        return (os.path.join(os.path.abspath(outfolder), 'index.html'))
        
    elif choice=="5": #provide a tar file as output
        for f in glob.glob(os.path.join(os.path.dirname(__file__),'new_html','*')):
            shutil.copy(f,outfolder)
        html(outfolder,pathways,scores,scores_col,dict_net)
        #CREATE TAR FILE AS OUTPUT
        fid = str(uuid.uuid4())
        newtarfile = os.path.join(os.path.abspath(outfolder),fid+'.tar')
        files = os.listdir(outfolder)
        os.chdir( outfolder )        
        tFile = tarfile.open(newtarfile, 'w')
        for f in files:
            tFile.add(f)
        tFile.close()
        return(newtarfile)  
        
            

  
if __name__ == '__main__':
    parser = arguments()
    arg = parser.parse_args()
    run(arg.inputtarfolder,arg.outfile,arg.typeformat,arg.choice,arg.selenzyme_table,arg.filenames)
