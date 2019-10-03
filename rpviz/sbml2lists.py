#!/usr/bin/env python
# coding: utf-8
'''To visualize a SBML file
Comment : most difficult script to understand'''

import libsbml
import os
from .smile2picture import picture,picture2
from .smarts2tab import smarts2tab
from .tsv2name import id2name, smile2name


def sbml2list(sbml_file, selenzyme_table, d, namesdict, pathway_id='rp_pathway'):
    """Extracts everything from sbml and returns lists and dictionaries"""
    #open the SBML using libsbml
    doc = libsbml.readSBML(sbml_file)
    name = os.path.basename(sbml_file)
    #return the model from the SBML document using libsbml
    model = doc.model
    #we will use the groups package to return the retropath pathway
    #that is all the reactions that are associated with the heterologous 
    #pathway
    groups = model.getPlugin('groups')
    #in the rpFBA script, rp_pathway is the default name
    rp_pathway = groups.getGroup(pathway_id)
    annotation = rp_pathway.getAnnotation()
    ibisba_annotation = annotation.getChild('RDF').getChild('Ibisba').getChild('ibisba')
    RdfG_o = ibisba_annotation.getChild('dfG_prime_o').getAttrValue('value')
    RdfG_m = ibisba_annotation.getChild('dfG_prime_m').getAttrValue('value')
    glob_score = ibisba_annotation.getChild('global_score').getAttrValue('value')
    rlist = []
    LR = []
    dfG_prime_o = {}
    dfG_prime_m = {}
    dfG_uncert = {}
    flux_value = {}
    rule_id = {}
    rule_score = {}
    reac_smiles = {}
    fba_obj_name = {}
    revers = {}
    #loop through all the members of the rp_pathway
    for member in rp_pathway.getListOfMembers():
        #fetch the reaction according to the member id
        reaction = model.getReaction(member.getIdRef())
        rlist.append(reaction)
        #extract rule id from reaction
        annotation = reaction.getAnnotation()
        ibisba_annotation = annotation.getChild('RDF').getChild('Ibisba').getChild('ibisba')
        rule_ID = ibisba_annotation.getChild('rule_id').getChild(0).toXMLString()
        #Test to see of that is the target reaction --> TODO: use the id of the reaction instead (i.e. targetSink)
        if rule_ID:
            reaction_id = rule_ID
        else:
            reaction_id='target_reaction'
        LR.append(reaction_id) #name of reaction node : reaction_ruleID
        #get the annotation of the reaction
        #includes the MIRIAM annotation and the IBISBA ones
        annotation = reaction.getAnnotation()
        ibisba_annotation = annotation.getChild('RDF').getChild('Ibisba').getChild('ibisba')
        #extract dG_prime_o of the ibisba annotation values
        dfG_prime_o[reaction_id] = ibisba_annotation.getChild('dfG_prime_o').getAttrValue('value')
        #extract dG_prime_m of the ibisba annotation values
        dfG_prime_m[reaction_id] = ibisba_annotation.getChild('dfG_prime_m').getAttrValue('value')
        #extract dG_prime_o of the ibisba annotation values
        dfG_uncert[reaction_id] = ibisba_annotation.getChild('dfG_uncert').getAttrValue('value')
        #extract rule id from reaction
        rule_id[reaction_id] = ibisba_annotation.getChild('rule_id').getChild(0).toXMLString()
        #extract rule score from reaction
        rule_score[reaction_id] = ibisba_annotation.getChild('rule_score').getAttrValue('value')
        #extract fba_RPFBA_obj value
        flux_value[reaction_id] = ibisba_annotation.getChild('fba_rpFBA_obj').getAttrValue('value')
        smiles = ibisba_annotation.getChild('smiles').getChild(0).toXMLString()
        if smiles!='None' and smiles!='':
            reac_smiles[reaction_id] = smiles.replace('&gt;&gt;','>>')
        #Extract name of biomass objective
        biom_obj_name=ibisba_annotation.getChild(6).toXMLString()
        biom_obj_name=(biom_obj_name).split(":")[1].split("units")[0]
        fba_obj_name[reaction_id]=biom_obj_name
        #extract reversibility of the reaction
        revers[reaction_id]=reaction.getReversible()

    Lreact=[]
    Lprod=[]
    for reaction in range(len(rlist)):
        Lreact.append([p.species for p in rlist[reaction].reactants]) #get list of reactants id
        Lprod.append([p.species for p in rlist[reaction].products]) #get list of products id
    Listprod=[]
    for j in range(len(Lprod)):
        for i in range(len(Lprod[j])):
            Listprod.append(Lprod[j][i])
    dic_types={}
    Listreact=[]
    for j in range(len(LR)):
        dic_types[LR[j]]='reaction'
        for i in range(len(Lreact[j])):
            if Lreact[j][i] not in Listprod : #if it's not a intermediary product
                Lreact[j][i]+=str(LR[j]) #name of reactant node is molecule_reactionid
                dic_types[Lreact[j][i]]='reactant'
            Listreact.append(Lreact[j][i])
    for p in Listprod:
        dic_types[p]='product'
    Lelem=[]
    for i in Listprod:
        Lelem.append(i)
    for j in Listreact:
        Lelem.append(j)
    mem = []

    for member in rp_pathway.getListOfMembers():
        reac = model.getReaction(member.getIdRef())
        for rea in reac.getListOfReactants(): #get reactants
            mem.append(rea.getSpecies())
        for pro in reac.getListOfProducts(): #get products
            mem.append(pro.getSpecies())

    species_links={}
    species_names={}
    species_smiles={}
    #loop through all the members of the rp_pathway
    for member in list(set([i for i in mem])):
        #fetch the species according to the member id
        reaction = model.getSpecies(member)
        spname=reaction.getName()
        if spname:
            if member not in Lelem:
                for elem in Lelem:
                        if member in elem: #check the new name of the node
                            species_names[elem]=spname
            else :
                species_names[member]=spname

        #get the annotation of the species
        #includes the MIRIAM annotation and the IBISBA ones
        annotation = reaction.getAnnotation()
        ibisba_annotation = annotation.getChild('RDF').getChild('Ibisba').getChild('ibisba')
        #extract one of the ibisba annotation values
        smiles = ibisba_annotation.getChild('smiles').getChild(0).toXMLString()
        if smiles:
            if member not in Lelem:
                for elem in Lelem:
                    if member in elem: #check the new name of the node (ex : MNXM4 is in MNXM4_ReactionID)
                        species_smiles[elem] = smiles
            else:
                species_smiles[member] = smiles
        link_annotation=annotation.getChild('RDF').getChild('Description').getChild('is').getChild('Bag')
        for i in range(link_annotation.getNumChildren()):
            str_annot = link_annotation.getChild(i).getAttrValue(0) #Here we get the attribute at location "0". It works since there is only one
            if str_annot.split('/')[-2]=='metanetx.chemical':
                if member not in Lelem:
                    for elem in Lelem:
                        if member in elem: #check the new name of the node
                            species_links[elem] = str_annot
                else:
                    species_links[member]=str_annot #here is the MNX code returned

    image=picture(species_smiles)
    image2=picture2(reac_smiles)[0]
    image2big=picture2(reac_smiles)[1]
    if selenzyme_table=='Y':
        data_tab=smarts2tab(reac_smiles)
    else :
        data_tab={i:"" for i in reac_smiles}

    roots={}

    for i in range(len(Lprod)):
        for j in Lprod[i]:
            if 'TARGET' in j:
                roots[j]="target"

    roots[LR[-1]]="target_reaction"

    for i in range(len(LR)):
        for j in range(len(Lreact[i])):
            id=species_names[Lreact[i][j]]
            species_names[Lreact[i][j]]=id2name(d,id)
        for p in range(len(Lprod[i])):
            smiles=species_smiles[Lprod[i][p]]
            id = Lprod[i][p]
            try :
                species_names[Lprod[i][p]]=namesdict[id]
            except :
                species_names[Lprod[i][p]]=smile2name(smiles, id,d)

    return(LR, Lreact, Lprod, name, species_smiles, reac_smiles,image,image2,\
    species_names, species_links,roots,dic_types,image2big,data_tab,\
    dfG_prime_o,dfG_prime_m, dfG_uncert, flux_value, rule_id,rule_score,\
    fba_obj_name,RdfG_o,RdfG_m,glob_score,revers)
