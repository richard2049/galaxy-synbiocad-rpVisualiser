# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:02:54 2019

@author: anael
"""

import json
import os
import glob
from bs4 import BeautifulSoup
import networkx as nx
import pandas as pd
from .color_grad import linear_gradient

def html(outfolder,folder,scores,scores_col,dict_net):
    """Create the visualizer. 
    Input : network and dictionaries
    Output : network_elements.js, network_viewer.js, index.html"""
        
    ##Append color dictionaries
    
    for score in scores:
        L=[]
        dic=sorted(scores[score].items(), key=lambda x: float(x[1])) #Compare float not str
      
        for e in dic:
            L.append(e[0]) #list of pathways sorted by score
 
        nb_diff_col=len(set(list(scores[score].values()))) #how many different values for each score
        hex = linear_gradient("#3a46d5","#da3c29",nb_diff_col)["hex"] #list of colors from blue to red
        
        col={}
        if L!=[]:
            col[L[0]]=hex[0] #1st path 1st color
            c=0
            for i in range(1,len(L)):
                if scores[score][L[i]]!=scores[score][L[i-1]]: #if same score, same color
                    c+=1
                col[L[i]]=hex[c]
            
            
            scores_col["col_"+score]=col
        
    ##Append elements in a js file for network
   
    with open(os.path.join(os.path.abspath(outfolder),"network_elements.js"),"w") as jsoutfile: 
        jsoutfile.write("pathdic="+json.dumps(dict_net)+"; \n")
        jsoutfile.write("scores ="+json.dumps(scores)+"\n")
        jsoutfile.write("scores_col ="+json.dumps(scores_col)+"\n")
        jsoutfile.close()
    
        
    htmlfile= open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"new_html","template.html"))
    soup = BeautifulSoup(htmlfile, 'html.parser')   
  
    ##Update selectbox with scores
    select_script=soup.find(id="selectbox")

    for i in scores:
        new_tag=soup.new_tag("option")
        new_tag["value"]=i
        new_tag.append(i)
        select_script.append(new_tag)
    
    #Pathway table        
    pathways = ["<a href='"+str(f)+".csv' download>"+str(f)+"</a>" for f in folder] #link to csv for each path
    d={'Pathway':pathways}
    df=pd.DataFrame(d)
    df["Select"]=['' for f in folder]
    df["Score"]=[''for f in folder]
    
    html_str=df.to_html(index=False)
    html_str=html_str.replace("&lt;","<").replace("&gt;",">")
                
    table=soup.find(id="table_path")
    table.append(BeautifulSoup(html_str, 'html.parser'))  
      
        
    htmlfile.close()
        
    html = soup.prettify("utf-8")

    with open(os.path.join(os.path.abspath(outfolder),'index.html'), "wb") as file:
        file.write(html)    
        file.close()
        
