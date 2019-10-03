# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:56:48 2019

@author: anael
"""

#import pandas as pd
import cirpy
import pubchempy as pcp


def smile2name(smiles,id,d):
    """Gives a name for products compounds"""
    try: #explore metanetx database
        name=d[id.split('_')[0]] #try if it's in metanetx DB
    except :
        try: #explore pubchem database
            CID=pcp.get_compounds(smiles, 'smiles')[0].cid
            name=pcp.Compound.from_cid(CID).synonyms[0]       
        except:
            try :#query cirpy database
                name=cirpy.query(smiles,'names')[0].value[0]
            except :
                name=id
    return(name)
    
    

    
def id2name(d,id):
    """Gives a name for metanetx compounds"""
    try:
        name=d[id]
    except :
        name=id
    return(name)
    

