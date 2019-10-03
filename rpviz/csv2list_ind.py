# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 09:35:28 2019

@author: anael
"""


from .smile2picture import picture,picture2
from .smarts2tab import smarts2tab
from .tsv2name import id2name,smile2name
import os
import csv
import pandas as pd



    
def csv2list2(csvfolder,path,datapath,selenzyme_table,d,namesdict):
    """Does exactly the same than sbml2list but with the output of RP2paths"""
    
    # READ CSV FILE WITH INFO    (solution)
    csvfileinf=os.path.join(csvfolder,"solution.csv")
    datainf=[]
    with open(csvfileinf, 'r') as csvFile:
        reader = csv.reader(csvFile)   
        for row in reader:
            datainf.append(row)
    csvFile.close()
    
    # READ COMPOUNDS.TXT FILE WITH SMILES 
    txtfile=os.path.join(csvfolder,"path","out1","compounds.txt")
    datacompounds = pd.read_csv(txtfile, sep="\t", header=None)
 
    
    revers={}
    name=str(path)
    
    LR=[] #List of reactions
    Lreact=[]
    Lprod=[]
  
    for i in range(len(datapath)):
        Lr=[]
        Lp=[]
        if datapath[i][0]==str(path):#if good pathway
            LR.append((datapath[i][1][:-2]))#problème with the last 0
            reactants=list((datapath[i][3]).split(":"))
            for j in reactants :
                for l in range(int(j[0])): #if they are several reactants
                    Lr.append(j.split('.')[1])
            Lreact.append(Lr)
            products=list((datapath[i][4]).split(":"))
            for j in products :
                for l in range(int(j[0])): #if they are several products
                    Lp.append(j.split('.')[1])
            Lprod.append(Lp)


    #SET SPECIES NAMES
    species_name={}
    
    for i in range(len(Lreact)):
        for j in range(len(Lreact[i])):
            if 'MNX' in Lreact[i][j]:
                species_name[Lreact[i][j]]=id2name(d,Lreact[i][j]) #query metanetx DB
            else : 
                species_name[Lreact[i][j]]=Lreact[i][j] #query metanetX, CIR, PubChem DB
       
        
    # GET NODES INFORMATION
   
    reac_smiles={}
    dic_types={}
    rule_score={}
    rule_id={}
    
    for r in LR: #for each reaction
        dic_types[r]="reaction"
        for i in datainf:     
            if i[1]==r.split("/")[0]: #problem with the last 0   
                reac_smiles[r]=i[2]
                rule_score[r]=i[12]
                rule_id[r]=i[10]
    
    # To individualize each reactant
    Listprod=[]
    for j in range(len(Lprod)):
        for i in range(len(Lprod[j])):
            Listprod.append(Lprod[j][i]) 
            species_name[Lprod[j][i]]=Lprod[j][i]
    
    Listreact=[] #name_path__nboccur
    for j in range(len(Lreact)):
        for i in range(len(Lreact[j])):
            if Lreact[j][i] not in Listprod : #if not an intermediate product
                Lreact[j][i]+=LR[j]
            Listreact.append(Lreact[j][i])#name_path_nboccur
                
    # SET ATTRIBUTES
    
    sp_names={} #keys in dict were juste name, not name_path_nboccur
    sp_smiles={} 
    roots={}
    for reac in Listreact:
        dic_types[reac]="reactant"
        for key in species_name.keys():
            if key in reac:
                sp_names[reac]=species_name[key]
        for i in range(len(datacompounds)):
            if datacompounds[0][i] in reac:
                sp_smiles[reac]=datacompounds[1][i]
    
    for prod in Listprod:
        if "TARGET" in prod :
            roots[prod]="target"
        dic_types[prod]="product"
        for i in range(len(datacompounds)):
            if datacompounds[0][i] in prod:
                sp_smiles[prod]=datacompounds[1][i]
                try :
                    sp_names[prod]=namesdict[species_name[prod]]
                except :
                    sp_names[prod]=smile2name(sp_smiles[prod],species_name[prod],d)
                

    
    image=picture(sp_smiles)
    image2=picture2(reac_smiles)[0]
    image2big=picture2(reac_smiles)[1]
    
    if selenzyme_table=='Y':
            data_tab=smarts2tab(reac_smiles)
    else :
        data_tab={i:"" for i in reac_smiles}
     
    
    
    #Attributes not available with the csv
    species_links=dfG_prime_o=dfG_prime_m=dfG_uncert=flux_value\
    =fba_obj_name={}
    RdfG_o=RdfG_m=glob_score=0

    return(LR, Lreact, Lprod, name, sp_smiles, reac_smiles,image,image2,\
    sp_names, species_links,roots,dic_types,image2big,data_tab,\
    dfG_prime_o,dfG_prime_m, dfG_uncert, flux_value, rule_id,rule_score,\
    fba_obj_name,RdfG_o,RdfG_m,glob_score,revers)