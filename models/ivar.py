# -*- coding: utf-8 -*-
"""
    This file is part of iVar - DataBase of Genomics Variants

    Copyright (C) 2020 Federica Cestari, Enrico Tagliafico,
    Sara Castellano and Giovanni Faglioni
    Copyright (C) 2020 Universita di Modena e Reggio Emilia

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import datetime

from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=False)
DEFAULT_PAGINATE = myconf.take('iVarDB.default_paginate', cast=int) or 10
DEFAULT_CLASSIF = myconf.take('iVarDB.default_classif')
VCF_VARIANT_TEMPLATE = myconf.take('iVarDB.vcf_variant_template')
VCF_REANNOTATION_MAX_ROW = myconf.take('iVarDB.vcf_reannotation_max_rows', cast=int) or 0
CLINVAR_URL = myconf.take('iVarDB.clinvar_url') or "https://www.ncbi.nlm.nih.gov/clinvar/"
if CLINVAR_URL[:1]!='/':
    CLINVAR_URL = CLINVAR_URL +'/'
CLINVAR_HGVS = []
CLINVAR_HGVS = myconf.take('iVarDB.clinvar_hgvs').split(',') or None
SPECIAL_ATTRIBUTES = []
SPECIAL_ATTRIBUTES = myconf.take('iVarDB.special_attributes').split(',')

# dafaults view 
default_view = 'ivar.html'
default_subview = 'ivar_sub.html'

#Per logging activity
#import logging
#logger = logging.getLogger(request.application) #"web2py.app.EB")
#logger.setLevel(logging.DEBUG)

from iVarExporter import ExporterCSVLabel, ExporterTSVLabel
default_exportclasses=dict(csv=(ExporterCSVLabel, 'CSV')
                          ,tsv=(ExporterTSVLabel, 'TSV')
                          ,xml=False
                          ,html=False
                          ,json=False
                          ,csv_with_hidden_cols=False
                          ,tsv_with_hidden_cols=False
                           )
#        csv=(ExporterCSV, 'CSV'),
#        xml=(ExporterXML, 'XML'),
#        html=(ExporterHTML, 'HTML'),
#        tsv=(ExporterTSV, 'TSV (Excel compatible)')


def bootstrap_autocomplete(*args, **kwargs):
    widget = SQLFORM.widgets.autocomplete(*args, **kwargs)
    return lambda f, v: widget(f, v, _class='form-control', _type='text')


def representlabel(field,value):
    l=''
    for key,label in field.requires.options():
        if key==value:
            l=label
    return l

def requires_option(field):
    d= dict()
    s = field.requires.options()
    for key,label in field.requires.options():
        d[key]=label
    #return json.dumps(d)
    return XML(json.dumps(d))

"""
def options_widget(field,value,**kwargs):
    # Use web2py's intelligence to set up the right HTML for the select field
    # the widgets knows about the database model
    w = SQLFORM.widgets.options.widget
    xml = w(field,value,**kwargs)
    return xml
"""
# per editing inline (vcf)
def options_widget(field,value,**kwargs):
    return SQLFORM.widgets.options.widget(field,value,**kwargs)
def string_widget(field,value,**kwargs):
    return SQLFORM.widgets.string.widget(field,value,**kwargs)
def text_widget(field,value,**kwargs):
    return SQLFORM.widgets.text.widget(field,value,**kwargs)
def boolean_widget(field,value,**kwargs):
    return SQLFORM.widgets.boolean.widget(field,value,**kwargs)
def date_widget(field,value,**kwargs):
    v = value.strftime("%d/%m/%Y") if value else ''
    return SQLFORM.widgets.date.widget(field,v,**kwargs)
    
def set_of_values(field):
    #ritorna la lista del contenuto di un campo. uso:<field>.requires=IS_IN_SET(set_of_values(<fields>),zero=None,error_message=T('mandatory'))

    f =[]
    for row in db().select(field,distinct=True):
        f.append(row[field.name])
    return f

def string_to_list(string):
    #trasforma una stringa di forma "X"|"Y"|"Z"
    #in una lista (X,Y,Z)
    if not string:
        return list()
    if '"|"' in string:
        lista = string.split('"|"') #trasformo in lista
    else:
        lista = string
        lista = [lista]

    lis = list()
    for x in lista:
        if x[0]=='"':  #tolgo primo e ultimo carattere se sono "
            x = x[1:]
        if x[-1]=='"':
            x = x[:-1]
        x = x.strip()
        lis.append(x)

    return lis

def list_to_dict(lista):
    #trasforma una lista  "X":"L","X":"L","X":"L"
    #in un dizionario {X:L,X:L}
    if not lista:
        return dict()

    if not isinstance(lista,list):
        lista = [lista]

    diz = dict()
    for a in lista:
        if ":" in a:
            xl = a.split(":")
            # prendo l'ultimo : come separatore della label .. in caso prima ci siano dei ":" nelle formule.
            #x = xl[0] #field
            x = ':'.join(xl[:-1]) #field
            if x[0]=='"':  #il primo e l'ultimo carattere solo ""
                x = x[1:]
            if x[-1]=='"':
                x = x[:-1]
            #l = xl[1]  # lable
            l = xl[-1] # lable
            if l[0]=='"':  #il primo e l'ultimo carattere solo ""
                l = l[1:]
            if l[-1]=='"':
                l = l[:-1]
        else:
            x = a
            l = a
        x = x.strip()
        l = l.strip()
        diz[x] = l

    return diz

def string_to_date(str_date,format):
    if str_date:
        try:
            datetime.datetime.strptime(str_date, format)
        except Exception, e:
            return None
        else:
            return datetime.datetime.strptime(str_date, format)
    return None

def date_to_string(date,format):
    if date:
        try:
            date.strftime(format)
        except Exception, e:
            return None
        else:
            return date.strftime(format) 
    return None

#########################################

def head_title(titolo='',btn_prec=None):

    form_head  = FORM(
                        DIV(
                            DIV(
                                DIV(
                                    SPAN (
                                           A(' ' , _title=T('Back'), _class='btn btn-default btn-secondary btn-sm icon arrowleft icon-arrowleft glyphicon glyphicon-arrow-left'
                                                  , _href=btn_prec)
                                          ,XML('&nbsp;&nbsp;')
                                         ) if (btn_prec) else ''
                                   ,SPAN(titolo,_class="h5",_style="vertical-align:bottom")
                                   ,_class="card-title text-primary" ,_style="margin-bottom:0"
                                )
                                ,_class="card-body" ,_style="padding:10px 15px"
                            )
                            ,_class="card card-ivar"
                        )  
                   )
    return form_head


#####################
####   TABELLE   ####
#####################

#############
## VARIANT ##
#############

db.define_table('VARIANT'
                ,Field('gene'               ,'string' ,length = 20    ,label = T('Gene'))
                ,Field('id_hg19'            ,'string' ,length = 500   ,label = T('hg19'))
                ,Field('id_hg38'            ,'string' ,length = 500   ,label = T('hg38'))
                ,Field('classif'            ,'string' ,length = 2     ,label = T('Classif.'))
                ,Field('last_check'         ,'date'                   ,label = T('Last Check'))
                ,Field('note'               ,'text'                   ,label = T('note'))
                ,format='%(gene)s %(id_hg19)s'
               )


#db.VARIANT.gene.requires=IS_IN_SET(set_of_values(db.VARIANT.gene),zero=None,error_message=T('mandatory'))
db.VARIANT.gene.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.VARIANT.id_hg19.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.VARIANT.id_hg38.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

db.VARIANT.classif.requires=IS_EMPTY_OR(IS_IN_SET([('C1' ,T('C1'))
                                                  ,('C2' ,T('C2'))
                                                  ,('C3' ,T('C3'))
                                                  ,('C4' ,T('C4'))
                                                  ,('C5' ,T('C5'))
                                                  ]))
db.VARIANT.classif.represent = lambda value, row: representlabel(db.VARIANT.classif,value)

db.VARIANT.last_check.represent = lambda value, row: value.strftime("%d/%m/%Y") if value else ''

db.VARIANT.note.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.VARIANT.note.widget = lambda f,v : SQLFORM.widgets.text.widget(f,v,_rows=2)

def validation_VARIANT(form):
    return True

def find_insert_VARIANT(hg,variant,gene,classif,classif_valid_from):

    classif = classif.strip() or ''

    #if variant[0:3] != "chr": #change for add CNV type variant
    if variant[0].isdigit():   #if variant start with number add "chr"
        variant = "chr" + variant
    elif variant[1]=='|':  #if variant start with '<char>|', the second position is pipe, add "chr"
        variant = "chr" + variant

    row = None
    if hg=='hg19':
        row = db(db.VARIANT.id_hg19 == variant).select().first()
    if hg=='hg38':
        row = db(db.VARIANT.id_hg38 == variant).select().first()

    variant_id = None
    if row:
        variant_id = row['id']
        id_hg19 = row['id_hg19']
        id_hg38 = row['id_hg38']
        update_VARIANT(variant_id,id_hg19,id_hg38,gene,classif,classif_valid_from)
    else:
        if hg=='hg19':
            variant_id = db.VARIANT.insert(id_hg19=variant, gene=gene, classif=classif)
        if hg=='hg38':
            variant_id = db.VARIANT.insert(id_hg38=variant, gene=gene, classif=classif)
        db.commit()
        if classif !='':
            update_VARIANT_ATTRIBUTE_classif(variant_id,classif,classif_valid_from)

    return variant_id

def update_VARIANT(variant_id,id_hg19,id_hg38,gene,classif,classif_valid_from):
    classif = classif.strip() or ''
    row = db(db.VARIANT.id == variant_id).select().first()
    if row:
        row.id_hg19 = id_hg19
        row.id_hg38 = id_hg38
        if gene != '':
            row.gene = gene
        row.update_record()
        db.commit()
        if classif !='':
            update_VARIANT_ATTRIBUTE_classif(variant_id,classif,classif_valid_from)
            update_VARIANT_classif(variant_id) #update classif from current attribute of DEFAULT_CLASSIF


def update_VARIANT_classif(variant_id):
    row = db((db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id == variant_id) 
           & (db.VARIANT_ATTRIBUTE_CURRENT.attribute_name == DEFAULT_CLASSIF)).select().first()
    classif = ''
    if row:
        classif = row.attribute_value

    row = db(db.VARIANT.id == variant_id).select().first()
    if row:
        if row.classif != classif or row.classif == None:
            row.classif = classif
            row.update_record()
            db.commit()
            return True #update

    return False

def variant_id_hg19(id_hg19):
    row = db(db.VARIANT.id_hg19 == id_hg19).select().first()
    if row:
        return row.id
    else:
        return 0

def variant_default_classif_id(variant_id):
    row = db((db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id == variant_id) &\
             (db.VARIANT_ATTRIBUTE_CURRENT.attribute_name==DEFAULT_CLASSIF)).select().first()
    if row:
        return row.id
    else:
        return 0

db.define_table('VARIANT_ATTRIBUTE'
                ,Field('VARIANT_id'        ,'reference VARIANT'      ,label = T('Variant'))
                ,Field('attribute_name'    ,'string' ,length = 250   ,label = T('Attribute'))
                ,Field('attribute_value'   ,'string' ,length = 500   ,label = T('Value'))
                ,Field('valid_from'        ,'date'                   ,label = T('Valid from'))
                ,format='%(attribute_name)s : %(attribute_value)s  at %(valid_from)'
               )

db.VARIANT_ATTRIBUTE.VARIANT_id.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.VARIANT_ATTRIBUTE.VARIANT_id.widget = SQLFORM.widgets.autocomplete(request, db.VARIANT.id_hg19, id_field=db.VARIANT.id, at_beginning=False, limitby=(0, 10))


db.VARIANT_ATTRIBUTE.attribute_name.requires=IS_IN_SET(set_of_values(db.VARIANT_ATTRIBUTE.attribute_name),zero=None,error_message=T('mandatory'))
db.VARIANT_ATTRIBUTE.attribute_name.represent=lambda value, row: '' if value is None else value
db.VARIANT_ATTRIBUTE.attribute_value.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.VARIANT_ATTRIBUTE.attribute_value.widget = lambda f,v : SQLFORM.widgets.text.widget(f,v,_rows=4,_title=v)
db.VARIANT_ATTRIBUTE.attribute_value.represent=lambda value, row: '' if value is None else value

db.VARIANT_ATTRIBUTE.valid_from.requires = IS_DATE()
db.VARIANT_ATTRIBUTE.valid_from.represent = lambda value, row: value.strftime("%d/%m/%Y") if value else ''

def validation_VARIANT_ATTRIBUTE(form):
#FEXME : valutare se inserire il default "data del giorno" al momento dell'insert e toglierlo dalla validazione
    if (form.vars.valid_from==''):
        form.vars.valid_from=request.now
    if (form.vars.attribute_name==DEFAULT_CLASSIF):
        form.vars.attribute_value = form.vars.attribute_value.upper()
        if (form.vars.attribute_value not in ('C1','C2','C3','C4','C5','')):
            form.errors.attribute_value=T('Empty or C1,C2,C3,C4,C5')

    return True

def variant_has_attribute(variant_id):
    numrecord = db(db.VARIANT_ATTRIBUTE.VARIANT_id == variant_id).count() or 0
    if (numrecord > 0):
        return True
    else:
        return False

def variant_id_of_attribute(variant_attribute_id):
        variant_attribute = db(db.VARIANT_ATTRIBUTE.id==variant_attribute_id).select().first()
        if variant_attribute:
            return variant_attribute.VARIANT_id
        else:
            return None

def num_variant_attribute(variant_id,attribute_name):
    nrecord = db((db.VARIANT_ATTRIBUTE.attribute_name == attribute_name) & (db.VARIANT_ATTRIBUTE.VARIANT_id == variant_id)).count() or 0
    return nrecord

def num_attributes_of_variant(variant_id):
    numrecord = db(db.VARIANT_ATTRIBUTE.VARIANT_id == variant_id).count() or 0
    return numrecord

def ClinVar(variant_id):
    url = ''
    attribute= ''
    for a in CLINVAR_HGVS:
        row = db((db.VARIANT_ATTRIBUTE_CURRENT.attribute_name == a) & (db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id == variant_id)).select().first() or None
        if row:
            hgvs = row.attribute_value
            attribute = a+"\n"+hgvs

            if ";" in hgvs:
                lista = hgvs.split(';') #trasformo in lista
                hgvs = lista[0]

            url = CLINVAR_URL + '?term='
            gene = db(db.VARIANT.id==variant_id).select().first()['gene'] or None
            if gene:
                url = url + gene + '%5Bgene%5D+' #[gene]+'
            url += hgvs
            break
    return dict(url=url,attribute=attribute)

def ClinVar_attribute(attribute_name, attribute_id):
    url = ''
    if attribute_name in CLINVAR_HGVS:
        row = db(db.VARIANT_ATTRIBUTE.id==attribute_id).select().first() or None
        if row:
            hgvs = row.attribute_value
            if ";" in hgvs:
                lista = hgvs.split(';') #trasformo in lista
                hgvs = lista[0]

            url = CLINVAR_URL + '?term='
            gene = db(db.VARIANT.id==row.VARIANT_id).select().first()['gene'] or None
            if gene:
                url = url + gene + '%5Bgene%5D+' #[gene]+'
            url += hgvs
    return url

def insert_VARIANT_ATTRIBUTE(variant_id, attribute,valid_from, accept_empty_value=False):
    if not valid_from or valid_from == None:
        valid_from = datetime.datetime.now()
    for (k,v) in attribute.items():
        if v.strip() != '' or accept_empty_value: # inserisco solo se valore è qualcosa di significativo o se accept_empty_value)
            # ci sono casi in cui, anche all'interno dello stesso file annotation, è presente più volte lo stesso valore per lo stesso attributo
            # in tal modo , a parità di valore e validità, non ricarico lo stesso dato.
            row_same = db((db.VARIANT_ATTRIBUTE.VARIANT_id == variant_id)&(db.VARIANT_ATTRIBUTE.attribute_name == k)
                          &
                          (db.VARIANT_ATTRIBUTE.valid_from == valid_from)
                          &
                          (db.VARIANT_ATTRIBUTE.attribute_value[:500] == v[:500])
                         ).select().first()
            if row_same:
                continue

            row_prec= db(
                (db.VARIANT_ATTRIBUTE.VARIANT_id == variant_id)&(db.VARIANT_ATTRIBUTE.attribute_name == k)&(db.VARIANT_ATTRIBUTE.valid_from<=valid_from)).select(db.VARIANT_ATTRIBUTE.ALL,orderby=~db.VARIANT_ATTRIBUTE.valid_from).first()

            row_succ = db((db.VARIANT_ATTRIBUTE.VARIANT_id == variant_id)&(db.VARIANT_ATTRIBUTE.attribute_name == k)&(db.VARIANT_ATTRIBUTE.valid_from>valid_from)).select(db.VARIANT_ATTRIBUTE.ALL, orderby=db.VARIANT_ATTRIBUTE.valid_from).first()

            if row_prec and row_prec.attribute_value[:500] == v[:500]:
                continue

            if row_prec and row_prec.attribute_value[:500] != v[:500] and row_prec.valid_from==valid_from:
                #aggiorno valore
                row_prec.attribute_value = v
                row_prec.update_record()
                db.commit()
                continue

            if row_succ and row_succ.attribute_value[:500] == v[:500]:
                #aggiorno data -> retrodato validlita
                row_succ.valid_from = valid_from
                row_succ.update_record()
                db.commit()
                continue

            #inserisco
            i = db.VARIANT_ATTRIBUTE.insert(VARIANT_id = variant_id
                                           ,attribute_name = k
                                           ,attribute_value = v
                                           ,valid_from = valid_from)
            db.commit()



def update_VARIANT_ATTRIBUTE_classif(variant_id,classif, classif_valid_from=None,accept_empty_value=False):
    attribute = dict()
    attribute[DEFAULT_CLASSIF]=classif or ''
    insert_VARIANT_ATTRIBUTE(variant_id, attribute,classif_valid_from, accept_empty_value)

def delete_false_VARIANT_ATTRIBUTE():
     for row in db(db.VARIANT_ATTRIBUTE.attribute_value.contains("|")).select():
        if row.attribute_value.replace("|","").strip()=="":
            row.delete_record()
            db.commit()

## view of only value valid (valid_from max)
"""
db.define_table('VARIANT_ATTRIBUTE_VALID'
                ,Field('VARIANT_id'        ,'reference VARIANT'      ,label = T('Variant'))
                ,Field('attribute_name'    ,'string' ,length = 250   ,label = T('Attribute'))
                ,Field('attribute_value'   ,'string' ,length = 500   ,label = T('Value'))
                ,Field('valid_from'        ,'date'                   ,label = T('Valid from'))
                ,format='%(attribute_name)s : %(attribute_value)s  at %(valid_from)'
                ,migrate=False
               )
db.VARIANT_ATTRIBUTE_VALID.VARIANT_id.requires  = db.VARIANT_ATTRIBUTE.VARIANT_id.requires
db.VARIANT_ATTRIBUTE_VALID.VARIANT_id.widget = db.VARIANT_ATTRIBUTE.VARIANT_id.widget

db.VARIANT_ATTRIBUTE_VALID.attribute_name.requires=db.VARIANT_ATTRIBUTE.attribute_name.requires
db.VARIANT_ATTRIBUTE_VALID.attribute_name.represent=db.VARIANT_ATTRIBUTE.attribute_name.represent
db.VARIANT_ATTRIBUTE_VALID.attribute_value.widget = db.VARIANT_ATTRIBUTE.attribute_value.widget
db.VARIANT_ATTRIBUTE_VALID.attribute_value.represent = db.VARIANT_ATTRIBUTE.attribute_value.represent

db.VARIANT_ATTRIBUTE_VALID.valid_from.represent = db.VARIANT_ATTRIBUTE.valid_from.represent



"""
## view of last value of attribute (valid_from max)

db.define_table('VARIANT_ATTRIBUTE_CURRENT'
                ,Field('VARIANT_id'        ,'reference VARIANT'      ,label = T('Variant'))
                ,Field('attribute_name'    ,'string' ,length = 250   ,label = T('Attribute'))
                ,Field('attribute_value'   ,'string' ,length = 500   ,label = T('Value'))
                ,Field('valid_from'        ,'date'                   ,label = T('Valid from'))
                ,format='%(attribute_name)s : %(attribute_value)s  at %(valid_from)'
                ,migrate=False
               )
db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id.requires  = db.VARIANT_ATTRIBUTE.VARIANT_id.requires
db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id.widget = db.VARIANT_ATTRIBUTE.VARIANT_id.widget

db.VARIANT_ATTRIBUTE_CURRENT.attribute_name.requires=db.VARIANT_ATTRIBUTE.attribute_name.requires
db.VARIANT_ATTRIBUTE_CURRENT.attribute_name.represent=db.VARIANT_ATTRIBUTE.attribute_name.represent
db.VARIANT_ATTRIBUTE_CURRENT.attribute_value.widget = db.VARIANT_ATTRIBUTE.attribute_value.widget
db.VARIANT_ATTRIBUTE_CURRENT.attribute_value.represent = db.VARIANT_ATTRIBUTE.attribute_value.represent

db.VARIANT_ATTRIBUTE_CURRENT.valid_from.represent = db.VARIANT_ATTRIBUTE.valid_from.represent


db.define_table('VARIANT_ATTRIBUTE_PREV'
                ,Field('VARIANT_ATTRIBUTE_id'        ,'integer' ,length = 11   ,label = T('Attribute'))
                ,Field('VARIANT_ATTRIBUTE_id_prev'   ,'integer' ,length = 11   ,label = T('Attribute Prev'))
                ,Field('attribute_value_prev'         ,'string' ,length = 500   ,label = T('Value Prev'))
                ,migrate=False
               )
db.VARIANT_ATTRIBUTE_PREV.attribute_value_prev.represent=lambda value, row: '' if value is None else value

db.define_table('VARIANT_ATTRIBUTE_COUNT'
                ,Field('VARIANT_id'                  ,'integer' ,length = 11   ,label = T('Variant'))
                ,Field('attribute_name'              ,'string' ,length = 250   ,label = T('Attribute'))
                ,Field('count'                       ,'integer' ,length = 11   ,label = T('Count'))
                ,migrate=False
               )

###################
##   ANNOTATION  ##
###################

db.define_table('ANNOTATION_TYPE'
               ,Field('name_type'           ,'string'      ,length = 50  ,label = T('Type name'))
               ,Field('char_sep'            ,'string'      ,length = 2   ,label = T('Sep'))
               ,Field('sample'            ,'string'      ,length = 50 ,label = T('Sample')
                     ,comment = T('Specify the columns, delimited by "" and separated by |, to identify the sample: "X"|"Y"'))
               ,Field('variant_hg19'        ,'string'      ,length = 50  ,label = T('Variant hg19')
                     ,comment = T('Specify the columns, delimited by "" and separated by |, to identify the variant: "X"|"Y"'))
               ,Field('variant_hg38'        ,'string'      ,length = 50  ,label = T('Variant hg38')
                     ,comment = T('Specify the columns, delimited by "" and separated by |, to identify the variant: "X"|"Y"'))
               ,Field('gene'                ,'string'      ,length = 10  ,label = T('Gene')
                      ,comment = T('Specify the columns, delimited by "" and separated by |, to identify the gene: "X"|"Y"'))
               ,Field('classif'             ,'string'      ,length = 50 ,label = T('Classif')
                  ,comment = T('Specify the columns, delimited by "" and separated by |, to identify the classification:  "X"|"Y"'))
               ,Field('classif_eval'       ,'text'                      ,label = T('Eval Classif')
                  ,comment = T('evaluation classif. Es: classif[0][0:2] if classif[0][0:2] in ["C1","C2",C3","C4",C5"] else ""'))
               ,Field('classif_valid_from' ,'string'      ,length = 100 ,label = T('Classif valid from')
                  ,comment = T('Specify "column":"format date" - Es: "Date val":"%d/%m/%Y" - "%d/%m/%Y" for 01/01/2021 , "%d/%m/%y" for 01/01/21'))
               ,Field('row_filter'          ,'list:string'      ,length = 150 ,label = T('Row filter')
                     ,comment = T('Specify the conditions for importing the rows. Empty = all'))
               ,Field('break_condition'     ,'list:string'  ,length = 500 ,label = T('Break condition')
                     ,comment = T('Break conditions: the subsiquent rows will be ignored. Es: row[0]=="xxx"'))
               ,Field('variant_attribute'  ,'list:string'  ,length = 500  ,label = T('Variant Attribute')
                     ,comment = T('Specify "X":"L", where X is column to import (delimited by ""), L is the label (delimited by ""); use | to concatenate more columns ("X"|"Y":"L")'))
               ,format='%(name_type)s'
               )

db.ANNOTATION_TYPE.name_type.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.ANNOTATION_TYPE.char_sep.requires=IS_IN_SET([('\t' ,T('tab'))
                                                ,(' ' ,T('space'))
                                                ,('|' ,T('|'))
                                                ,(',' ,T(','))
                                                ,(';' ,T(';'))
                                                ,(':' ,T(':'))
                                               ], error_message = 'mandatory')
db.ANNOTATION_TYPE.char_sep.default = '\t'
db.ANNOTATION_TYPE.char_sep.widget=lambda f,v : SQLFORM.widgets.radio.widget(f,v,style='table', cols=6, _width='100%')
db.ANNOTATION_TYPE.char_sep.represent = lambda value, row: representlabel(db.ANNOTATION_TYPE.char_sep,value)
db.ANNOTATION_TYPE.variant_hg19.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.variant_hg38.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.gene.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.classif.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.classif_eval.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.classif_eval.widget = lambda f,v : SQLFORM.widgets.text.widget(f,v,_rows=2)
db.ANNOTATION_TYPE.classif_valid_from.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.sample.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.row_filter.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.break_condition.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.ANNOTATION_TYPE.variant_attribute.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

def validation_ANNOTATION_TYPE(form):
    if not (request.vars['variant_hg19']) and not (request.vars['variant_hg38']) :
        form.errors.variant_hg19 = T('variant mandatory')
        form.errors.variant_hg38 = T('variant mandatory')
        return False
    return True

def copy_ANNOTATION_TYPE(annotation_type_id_from):
    annotation_type_from = db.ANNOTATION_TYPE(db.ANNOTATION_TYPE.id==annotation_type_id_from) 
    i = 0
    if annotation_type_from:
        i = db.ANNOTATION_TYPE.insert(name_type = "--copy from " + annotation_type_from.name_type + " --"
                                     ,variant_hg19 = annotation_type_from.variant_hg19
                                     ,variant_hg38 = annotation_type_from.variant_hg38
                                     ,gene = annotation_type_from.gene
                                     ,classif = annotation_type_from.classif
                                     ,classif_eval = annotation_type_from.classif_eval
                                     ,row_filter = annotation_type_from.row_filter 
                                     ,break_condition =annotation_type_from.break_condition
                                     ,variant_attribute = annotation_type_from.variant_attribute)
        db.commit()
    return i

db.define_table('ANNOTATION_FILE'
                ,Field('file_upload'         ,'upload',  uploadseparate=True ,autodelete=True 
                                                                              ,label = T('Text file') )
                ,Field('filename_upload'     ,'string'      ,length = 200     ,label = T('File name'))
                ,Field('date_upload'         ,'datetime'                      ,label = T('Upload date') )
                ,Field('fl_elaborated'       ,'string'      ,length = 1       ,label = T('Processed?') 
                        ,comment = T('N=not Processed/to Reprocess X=in Processing Y=Processed'))
                ,Field('date_valid_from'     ,'date'                          ,label = T('Valid from date') 
                      ,comment = T('use to set the ''valid from'' date'))
                ,Field('ANNOTATION_TYPE_id'  ,'reference ANNOTATION_TYPE'     ,label = T('Text file type'))
                ,format='%(filename_upload)s'
               )

db.ANNOTATION_FILE.file_upload.requires = IS_UPLOAD_FILENAME( error_message='mandatory')#, extension='^(vcf)$')
#db.ANNOTATION_FILE.file_upload.represent = lambda value,row: A(row.filename_upload or T('annotation file'), _href=URL('download', args=value))
db.ANNOTATION_FILE.file_upload.represent = lambda value,row: A(T('Text file'), _href=URL('download', args=value))

db.ANNOTATION_FILE.date_upload.requires = IS_EMPTY_OR(IS_DATETIME())
db.ANNOTATION_FILE.date_upload.represent = lambda value, row: value.strftime("%d/%m/%Y %H:%M") if value else ''
db.ANNOTATION_FILE.date_valid_from.requires = IS_EMPTY_OR(IS_DATE())
db.ANNOTATION_FILE.date_valid_from.represent = lambda value, row: value.strftime("%d/%m/%Y") if value else ''

db.ANNOTATION_FILE.fl_elaborated.default = 'N'
db.ANNOTATION_FILE.fl_elaborated.requires=IS_IN_SET([('N', T("not Processed")),('X',T("in Processing")),('Y',T("Processed"))])

db.ANNOTATION_FILE.fl_elaborated.widget=lambda f,v : SQLFORM.widgets.radio.widget(f,v,style='table', cols=3, _width='100%')
db.ANNOTATION_FILE.fl_elaborated.represent = lambda value, row: representlabel(db.ANNOTATION_FILE.fl_elaborated,value)

db.ANNOTATION_FILE.ANNOTATION_TYPE_id.requires=IS_EMPTY_OR(IS_IN_DB(db, 'ANNOTATION_TYPE.id', '%(name_type)s'))


def validation_ANNOTATION_FILE(form):
    return True

def ondelete_ANNOTATION_FILE(table, record_id):
    record = table(record_id)
    if ANNOTATION_FILE_is_used(record.id):
        response.flash = T('The Text file cannot be deleted: there is sample(s) linked to it')
        raise HTTP(403)

def ANNOTATION_FILE_is_used(TEXT_FILE_id):
    for row in db(db.SAMPLE.id>0).select():
        if row.TEXT_FILE_ids!= None:
            if TEXT_FILE_id in row.TEXT_FILE_ids:
                return True
    return False

def validation_ANNOTATION_FILE_import(form):
    if request.vars['file_upload'] =='':
        form.errors.file_upload = T('mandatory')
        return False
    return True
    


def insert_ANNOTATION_FILE(file_upload,filename_upload):
    i = db.ANNOTATION_FILE.insert(file_upload = file_upload
                                 ,filename_upload = filename_upload
                                 ,date_upload = datetime.datetime.now()
                                 ,fl_elaborated = 'N')
    db.commit()
    return i



###########
##  VCF  ##
###########

db.define_table('PANEL'
               ,Field('name_panel'  ,'string'      ,length = 50   ,label = T('Name of panel'))
               ,Field('gene'        ,'string'      ,length = 500  ,label = T('gene'))
               ,format='%(name_panel)s'
               )

db.PANEL.name_panel.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.PANEL.gene.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
#db.PANEL.gene.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.PANEL.gene.widget = lambda f,v : SQLFORM.widgets.text.widget(f,v,_rows=4)

def validation_PANEL(form):
    return True

def PANEL_is_used(PANEL_id):
    row = db(db.VCF_FILE.PANEL_id == PANEL_id).select().first()
    if row:
        return True
    else:
        return False
    

db.define_table('VIRTUAL_PANEL'
               ,Field('name_virtual_panel'  ,'string'      ,length = 50  ,label = T('Name of virtual panel'))
               ,Field('gene'                ,'string'      ,length = 500 ,label = T('gene'))
               ,format='%(name_virtual_panel)s'
               )

db.VIRTUAL_PANEL.name_virtual_panel.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.VIRTUAL_PANEL.gene.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.VIRTUAL_PANEL.gene.widget = lambda f,v : SQLFORM.widgets.text.widget(f,v,_rows=4)

def validation_VIRTUAL_PANEL(form):
    return True

def VIRTUAL_PANEL_is_used(VIRTUAL_PANEL_id):
    row = db(db.VCF_FILE.VIRTUAL_PANEL_id == VIRTUAL_PANEL_id).select().first()
    if row:
        return True
    else:
        return False


db.define_table('VCF_TYPE'
               ,Field('name_type'           ,'string'      ,length = 50  ,label = T('Name of Type VCF'))
               ,Field('variant'             ,'string'      ,length = 50  ,label = T('Variant')
                     ,comment = T('Specify the columns, delimited by "" and separated by |, to identyfy the variant: "X"|"Y"'))
               ,Field('row_filter'          ,'list:string'      ,length = 150 ,label = T('Row filter')
                     ,comment = T('Specify the conditions for importing the rows. Empty = all'))
               ,Field('sample_attribute'   ,'list:string' ,length = 50  ,label = T('Sample Attribute')
                     ,comment = T('Specify X:L, where X is column to import, L is the label; use | to concatenate more columns (X|Y:L)'))
               ,Field('variant_attribute'  ,'list:string' ,length = 250  ,label = T('Variant Attribute')
                     ,comment = T('Specify X:L, where X is column to import, L is the label; use | to concatenate more columns (X|Y:L)'))
               ,format='%(name_type)s'
               )

db.VCF_TYPE.name_type.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.VCF_TYPE.variant.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.VCF_TYPE.row_filter.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.VCF_TYPE.sample_attribute.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.VCF_TYPE.variant_attribute.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

def validation_VCF_TYPE(form):
    return True

def copy_VCF_TYPE(vcf_type_id_from):
    vcf_type_from = db.VCF_TYPE(db.VCF_TYPE.id==vcf_type_id_from) 
    i = 0
    if vcf_type_from:
        i = db.VCF_TYPE.insert(name_type = "--copy from " + vcf_type_from.name_type + " --"
                              ,variant = vcf_type_from.variant
                              ,row_filter = vcf_type_from.row_filter
                              ,sample_attribute = vcf_type_from.sample_attribute
                              ,variant_attribute = vcf_type_from.variant_attribute)
        db.commit()
    return i

db.define_table('VCF_FILE'
                ,Field('file_upload'         ,'upload',  uploadseparate=True ,autodelete=True 
                                                                              ,label = T('VCF file') )
                ,Field('filename_upload'     ,'string'      ,length = 200     ,label = T('VCF name'))
                ,Field('date_upload'         ,'datetime'                      ,label = T('date upload') )
                ,Field('fl_elaborated'       ,'string'      ,length = 1       ,label = T('Processed?')
                      ,comment = T('N=not Processed/to Reprocess X=in Processing Y=Processed'))
                ,Field('VCF_TYPE_id'         ,'reference VCF_TYPE'            ,label = T('VCF type'))
                ,Field('PANEL_id'            ,'reference PANEL'               ,label = T('VCF analysis panel'))
                ,Field('VIRTUAL_PANEL_id'    ,'reference VIRTUAL_PANEL'       ,label = T('Virtual panel for filtering') )
                ,Field('date_vcf'            ,'date'                          ,label = T('date VCF') )
                ,Field('hg'                  ,'string'      ,length = 10      ,label = T('hg'))
                ,Field('samples'             ,'list:string' ,length = 10      ,label = T('sample(s)'))
                ,format='%(filename_upload)s'
               )

db.VCF_FILE.file_upload.requires = IS_UPLOAD_FILENAME( error_message='mandatory')#, extension='^(vcf)$')
db.VCF_FILE.file_upload.represent = lambda value,row: A(row.filename_upload or T('vcf file'), _href=URL('download', args=value))
db.VCF_FILE.file_upload.represent = lambda value,row: A(T('VCF file'), _href=URL('download', args=value))

"""
db.VCF_FILE.vcf.represent = lambda value,row: A(T('vcf file'), _title=row.vcf_filename , _href=URL('vcf','vcf_download', args=row.id))
db.VCF_FILE.vcf.requires = lambda id, row: read_VCF_FILE_vcf(id)

db.VCF_FILE.vcf_filename.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
"""

db.VCF_FILE.filename_upload.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

db.VCF_FILE.date_upload.requires = IS_EMPTY_OR(IS_DATETIME())
db.VCF_FILE.date_upload.represent = lambda value, row: value.strftime("%d/%m/%Y %H:%M") if value else ''
db.VCF_FILE.date_vcf.requires = IS_EMPTY_OR(IS_DATE())
db.VCF_FILE.date_vcf.represent = lambda value, row: value.strftime("%d/%m/%Y") if value else ''

db.VCF_FILE.hg.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.VCF_FILE.samples.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

db.VCF_FILE.fl_elaborated.default = 'N'
db.VCF_FILE.fl_elaborated.requires=IS_IN_SET([('N', T("not Processed")),('X',T("in Processing")),('Y',T("Processed"))])


db.VCF_FILE.fl_elaborated.widget=lambda f,v : SQLFORM.widgets.radio.widget(f,v,style='table', cols=3, _width='100%')
db.VCF_FILE.fl_elaborated.represent = lambda value, row: representlabel(db.VCF_FILE.fl_elaborated,value)

db.VCF_FILE.VCF_TYPE_id.requires=IS_EMPTY_OR(IS_IN_DB(db, 'VCF_TYPE.id', '%(name_type)s'),null='')

db.VCF_FILE.VCF_TYPE_id.represent=lambda value, row: '' if value is None else db.VCF_TYPE._format % value

db.VCF_FILE.PANEL_id.requires=IS_EMPTY_OR(IS_IN_DB(db, 'PANEL.id', '%(name_panel)s'),null='')
db.VCF_FILE.PANEL_id.represent=lambda value, row: '' if value is None else db.PANEL._format % value

db.VCF_FILE.VIRTUAL_PANEL_id.requires=IS_EMPTY_OR(IS_IN_DB(db, 'VIRTUAL_PANEL.id', '%(name_virtual_panel)s'),null='')
db.VCF_FILE.VIRTUAL_PANEL_id.represent=lambda value, row: '' if value is None else db.VIRTUAL_PANEL._format % value


def validation_VCF_FILE(form):
    #form.errors= True  #this prevents the submission from completing
    return True

def ondelete_VCF_FILE(table, record_id):
    record = table(record_id)
    if VCF_FILE_is_used(record.id):
        response.flash = T('The VCF file cannot be deleted: there is sample(s) linked to it')
        raise HTTP(403)

def VCF_FILE_is_used(VCF_FILE_id):
    for row in db(db.SAMPLE.id>0).select():
        if row.VCF_FILE_ids!= None:
            if VCF_FILE_id in row.VCF_FILE_ids:
                return True
    return False

def validation_VCF_FILE_import(form):
    if request.vars['file_upload'] =='':
        form.errors.file_upload = T('mandatory')
        return False
    return True

def read_VCF_FILE_vcf(id):
    row = db(db.VCF_FILE.id == id).select().first()
    if row:
        (filename, stream) = db.VCF_FILE.vcf.retrieve(row.vcf)
        return stream

def insert_VCF_FILE(f):
    filename = f.filename

    file_upload = db.VCF_FILE.file_upload.store(f,filename)

    i = db.VCF_FILE.insert(file_upload = file_upload
                          ,filename_upload = filename
                          ,date_upload = datetime.datetime.now()
                          ,fl_elaborated = 'N'
                         )
    db.commit()

    return i


def update_data_in_VCF_FILE(vcf_file_id,date_vcf,hg,samples):

    row = db(db.VCF_FILE.id == vcf_file_id).select().first()
    if row:
        row.date_vcf = date_vcf
        row.hg = hg
        row.samples = samples
        row.update_record()
        db.commit()
        return row.id
    else:
        return False

############
## SAMPLE ##
############

db.define_table('TISSUE_TYPE'
               ,Field('tissue_type'  ,'string'      ,length = 50  ,label = T('Tissue type'))
               ,format='%(tissue_type)s'
               )

db.TISSUE_TYPE.tissue_type.requires = IS_NOT_EMPTY(error_message=T('mandatory'))

def validation_TISSUE_TYPE(form):
    return True


db.define_table('SAMPLE'
                ,Field('sample'              ,'string'      ,length = 50      ,label = T('Sample'))
                ,Field('date_sample'         ,'date'                          ,label = T('Date') )
                ,Field('fl_sample_type'      ,'string'      ,length = 1       ,label = T('Sample type') )
                ,Field('TISSUE_TYPE_id'      ,'reference TISSUE_TYPE'         ,label = T('Tissue type') )
                ,Field('fl_sex'              ,'string'      ,length = 1       ,label = T('Sex') )
                ,Field('VCF_FILE_ids'        ,'list:integer',length = 11      ,label = T('VCF files'))
                ,Field('TEXT_FILE_ids'       ,'list:integer',length = 11      ,label = T('Text files'))
                ,format='%(sample)s'
               )


db.SAMPLE.sample.requires = IS_NOT_EMPTY(error_message=T('mandatory'))

db.SAMPLE.date_sample.requires = IS_EMPTY_OR(IS_DATE())
db.SAMPLE.date_sample.represent = lambda value, row: value.strftime("%d/%m/%Y") if value else ''

db.SAMPLE.fl_sample_type.requires=IS_EMPTY_OR(IS_IN_SET([('G',T('Germinal'))
                                                        ,('S',T('Somatic')) 
                                                        ]),null='')


db.SAMPLE.fl_sample_type.widget=lambda f,v : SQLFORM.widgets.options.widget(f,v)
#SQLFORM.widgets.radio.widget(f,v,style='table', cols=2, _width='100%')
db.SAMPLE.fl_sample_type.represent = lambda value, row: representlabel(db.SAMPLE.fl_sample_type,value)

db.SAMPLE.TISSUE_TYPE_id.requires=IS_EMPTY_OR(IS_IN_DB(db, 'TISSUE_TYPE.id', '%(tissue_type)s'),null='')
db.SAMPLE.TISSUE_TYPE_id.represent=lambda value, row: '' if value is None else db.TISSUE_TYPE._format % value

db.SAMPLE.fl_sex.requires=IS_EMPTY_OR(IS_IN_SET([('M',T('Male')),('F',T('Female')) ]),null='')
db.SAMPLE.fl_sex.widget=lambda f,v : SQLFORM.widgets.options.widget(f,v)
#SQLFORM.widgets.radio.widget(f,v,style='table', cols=2, _width='100%')
db.SAMPLE.fl_sex.represent = lambda value, row: representlabel(db.SAMPLE.fl_sex,value)

db.SAMPLE.VCF_FILE_ids.requires=IS_EMPTY_OR(IS_IN_DB(db, 'VCF_FILE.id', '%(filename_upload)s', multiple=True),null='')
db.SAMPLE.VCF_FILE_ids.represent = lambda value,row: SAMPLE_files_list('VCF',value)

db.SAMPLE.TEXT_FILE_ids.requires=IS_EMPTY_OR(IS_IN_DB(db, 'ANNOTATION_FILE.id', '%(filename_upload)s', multiple=True),null='')
db.SAMPLE.TEXT_FILE_ids.represent = lambda value,row: SAMPLE_files_list('TEXT',value)


def SAMPLE_files_list(type,value):
    if value == None or value == '':
        return ''

    rows = None
    if type == 'VCF' :
        rows= db(db.VCF_FILE.id.belongs(value)).select()
    elif type == 'TEXT':
        rows = db(db.ANNOTATION_FILE.id.belongs(value)).select()
    if rows == None:
        return ''
    lista = ''
    for row in rows:
        if lista <> '':
            lista = lista + "\n "
        lista = lista + row.filename_upload

    return lista


def validation_SAMPLE(form):
    return True

def insert_SAMPLE(sample,date_sample, type_file = 'VCF', file_id = None):
#type_id = VCF or TEXT or None if not file_id
    if type_file != 'VCF':
        type_file = 'TEXT'
    if file_id == None:
        type_file = None

# hp:sample name is unic and is possibile to update from more different vcf or text files
#9/10/2019 con Sara si decide che lo stesso sample può essere presente in più vcf_file perchè elaborato in più volte

    sample_id = None
    row = db(db.SAMPLE.sample == sample).select().first()
    if row:
        sample_id = row['id']
        if type_file == 'VCF':
            if file_id not in row.VCF_FILE_ids:
                row.VCF_FILE_ids.append(file_id)
                row.update_record()
                db.commit()
        elif type_file == 'TEXT':
            if file_id not in row.TEXT_FILE_ids:
                row.TEXT_FILE_ids.append(file_id)
                row.update_record()
                db.commit()
        #endif update file_id
    else: #insert sample
        if type_file == 'VCF':
            sample_id = db.SAMPLE.insert(sample=sample
                                        ,date_sample=date_sample
                                        ,VCF_FILE_ids=[file_id]
                                        )
        elif type_file == 'TEXT':
            sample_id = db.SAMPLE.insert(sample=sample
                                        ,date_sample=date_sample
                                        ,TEXT_FILE_ids=[file_id]
                                        )
        else:
            sample_id = db.SAMPLE.insert(sample=sample
                                        ,date_sample=date_sample
                                        )
        db.commit()

    return sample_id

def update_SAMPLE(sample_id,vcf_file_id,fl_sample_type,tissue_type_id,fl_sex,date_sample):
    # si assume che il nome del sample sia unico, pertanto ogni altro dato può essere aggiornato se sample già esiste
    #tolto opzione di aggiornaemnto sample da ricarica vcf : prima si cancella il sample e poi si ricarica
    sample_id = None
    row = db(db.SAMPLE.id == sample_id).select().first()
    if row:
        sample_id = row['id']
        #se è già presente, significa che lo si sta ricaricando, quindi aggiorno il riferimento a vcf e altri dati
        row.sample = sample

        vcf_file_ids = row.VCF_FILE_ids
        if vcf_file_id not in vcf_file_ids:
            vcf_file_ids.append(vcf_file_id)
        row.VCF_FILE_ids = vcf_file_ids

        row.fl_sample_type = fl_sample_type
        row.TISSUE_TYPE_id = tissue_type_id
        row.fl_sex = fl_sex
        row.date_sample = date_sample
        row.update_record()
        db.commit()
    else:
        return False

    return sample_id


####################
## SAMPLE VARIANT ##
####################

db.define_table('SAMPLE_VARIANT'
                ,Field('SAMPLE_id'         ,'reference SAMPLE'      ,label = T('Sample'))
                ,Field('VARIANT_id'        ,'reference VARIANT'     ,label = T('Variant'))
                ,Field('AF'                ,'string'  ,length = 20  ,label = T('AF'))
                ,Field('GT'                ,'string'  ,length = 20  ,label = T('GT'))
                #,format = lambda r: '{} {}'.format(db(db.SAMPLE.id==r.SAMPLE_id).select().first()['sample'] or '' 
                #                                 , db(db.VARIANT.id==r.VARIANT_id).select().first()['id_hg19'] or '')
                )


#db.SAMPLE_VARIANT.VARIANT_id.represent = lambda value,row: db(db.VARIANT.id==value).select().first()['id_hg19'] or ''

#db.SAMPLE_VARIANT.SAMPLE_id.requires=IS_EMPTY_OR(IS_IN_DB(db, 'SAMPLE.id', '%(sample)s'), null='')
#db.SAMPLE_VARIANT.VARIANT_id.requires=IS_EMPTY_OR(IS_IN_DB(db, 'VARIANT.id', '%(id_hg19)s'), null='')

#per velocizzare altrimenti troppo lento
db.SAMPLE_VARIANT.SAMPLE_id.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.SAMPLE_VARIANT.VARIANT_id.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.SAMPLE_VARIANT.SAMPLE_id.widget = SQLFORM.widgets.autocomplete(request, db.SAMPLE.sample, id_field=db.SAMPLE.id, at_beginning=False, limitby=(0, 10))
db.SAMPLE_VARIANT.VARIANT_id.widget = SQLFORM.widgets.autocomplete(request, db.VARIANT.id_hg19, id_field=db.VARIANT.id, at_beginning=False, limitby=(0, 10))


db.SAMPLE_VARIANT.AF.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
db.SAMPLE_VARIANT.GT.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')


def validation_SAMPLE_VARIANT(form):
    return True


def insert_SAMPLE_VARIANT(sample_id,variant_id):
    if sample_id == None or variant_id == None:
        return None
    sample_variant_id = None
    row = db((db.SAMPLE_VARIANT.SAMPLE_id == sample_id) & (db.SAMPLE_VARIANT.VARIANT_id == variant_id) ).select().first()
    if row:
        sample_variant_id = row['id']
    else:
        sample_variant_id = db.SAMPLE_VARIANT.insert(SAMPLE_id=sample_id, VARIANT_id=variant_id)
        db.commit()

    return sample_variant_id


def update_SAMPLE_VARIANT(sample_variant_id,af,gt):
    row = db(db.SAMPLE_VARIANT.id == sample_variant_id).select().first()
    if row:
        sample_variant_id = row['id']
        #se è già presente, significa che lo si sta ricaricando, quindi aggiorno il valore di af
        row.AF = af
        row.GT = gt
        row.update_record()
        db.commit()
    else:
        sample_variant_id  = None

    return sample_variant_id

def sample_id_of(sample_variant_id):
    sample_variant = db(db.SAMPLE_VARIANT.id==sample_variant_id).select().first()
    if sample_variant:
        return sample_variant.SAMPLE_id
    else:
        return None

def variant_id_of(sample_variant_id):
    sample_variant = db(db.SAMPLE_VARIANT.id==sample_variant_id).select().first()
    if sample_variant:
        return sample_variant.VARIANT_id
    else:
        return None

def num_samples_of_variant(variant_id):
    numrecord = db(db.SAMPLE_VARIANT.VARIANT_id == variant_id).count() or 0
    return numrecord

def num_variants_of_sample(sample_id):
    numrecord = db(db.SAMPLE_VARIANT.SAMPLE_id == sample_id).count() or 0
    return numrecord

db.define_table('SAMPLE_VARIANT_ATTRIBUTE'
                ,Field('SAMPLE_VARIANT_id' ,'reference SAMPLE_VARIANT'  ,label = T('Sample & Variant'))
                ,Field('attribute_name'    ,'string' ,length = 250      ,label = T('Attribute'))
                ,Field('attribute_value'   ,'string' ,length = 250      ,label = T('Value'))
                ,format='%(attribute_name)s : %(attribute_value)s'
               )

#per velocizzare altrimenti troppo lento
#db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.requires  = IS_NOT_EMPTY()
#db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.widget = SQLFORM.widgets.autocomplete(request, db.SAMPLE_VARIANT.id , id_field=db.SAMPLE_VARIANT.id, at_beginning=False ,limitby=(0, 10))

db.SAMPLE_VARIANT_ATTRIBUTE.attribute_name.requires = IS_NOT_EMPTY(error_message=T('mandatory'))
db.SAMPLE_VARIANT_ATTRIBUTE.attribute_value.requires = IS_NOT_EMPTY(error_message=T('mandatory'))

def validation_SAMPLE_VARIANT_ATTRIBUTE(form):
    return True

def insert_SAMPLE_VARIANT_ATTRIBUTE(sample_variant_id,attributi):
    for (k,v) in attributi.items():
        row = db((db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id == sample_variant_id)
                &(db.SAMPLE_VARIANT_ATTRIBUTE.attribute_name == k)).select().first()
        if (row) and (row.attribute_value == v):
            i = row.id
            row.attribute_value = v
            row.update_record()
            db.commit()
        else:
            i = db.SAMPLE_VARIANT_ATTRIBUTE.insert(SAMPLE_VARIANT_id = sample_variant_id
                                                   ,attribute_name = k
                                                   ,attribute_value = v)
            db.commit()

#####################
## SEARCH CRITERIA ##
#####################

def search_widget(field, value, tables_search, **kwargs):
    #table on compose search
    prefix = field.name

    if not isinstance(tables_search,list):
        tables_search = [tables_search]
    tables =[]
    for f in tables_search:
        tables.append(db[f])
    #tables = [db[table_search]]

    for t in tables:
        db[t].id.readable = False 
        for f in db[t].fields():
            if db[t][f].type.startswith('reference'):
                db[t][f].readable = False 
            if db[t][f].type.startswith('date'):
                db[t][f].readable = False 
    sfields = reduce(lambda a, b: a + b,
                             [[f for f in t if f.readable] for t in tables])

    #prefix = formname == 'web2py_grid' and 'w2p' or 'w2p_%s' % formname
    search_menu = SQLFORM.search_menu(sfields, prefix=prefix)
    spanel_id = '%s_query_fields' % prefix
    sfields_id = '%s_query_panel' % prefix
    skeywords_id = '%s_keywords' % prefix
    form = CAT(DIV(
                    SQLFORM.widgets.text.widget(
                                                field
                                               ,value
                                               ,_name=prefix
                                               ,_id=skeywords_id
                                               ,_class = 'text form-control'
                                               ,_onfocus="jQuery('div[id$=_query_panel]').slideUp(0.1); jQuery('#%s').change(); jQuery('#%s').slideDown();" % (spanel_id, sfields_id)
                                               ,**kwargs)
                    #,INPUT(_type='button'
                    #       ,_value=T('Clear')
                    #       ,_class="button btn btn-default btn-secondary btn-sm"
                    #       ,_onclick="jQuery('#%s').val('');" % skeywords_id
                    #      )
                    #,_class = 'form_group row'
                    #_class='web2py_grid'
                    )
               ,DIV(search_menu,_class='web2py_console')
               )
    return form


db.define_table('SEARCH_CRITERIA'
                ,Field('search_name'        ,'string'  ,length = 50  ,label = T('search name'))
                ,Field('variant'            ,'text'                  ,label = T('variant''s condition'))
                ,Field('attribute'          ,'text'                  ,label = T('attribute''s condition'))
                ,Field('attribute_prev'     ,'text'                  ,label = T('previous attribute''s condition'))
                ,format='%(search_name)s'
               )

db.SEARCH_CRITERIA.variant.widget=lambda f,v : search_widget(f,v,['VARIANT'],_rows=4)
db.SEARCH_CRITERIA.variant.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

db.SEARCH_CRITERIA.attribute.widget=lambda f,v : search_widget(f,v,'VARIANT_ATTRIBUTE',_rows=8)
db.SEARCH_CRITERIA.attribute.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

db.SEARCH_CRITERIA.attribute_prev.widget=lambda f,v : search_widget(f,v,'VARIANT_ATTRIBUTE',_rows=8)
db.SEARCH_CRITERIA.attribute_prev.requires = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

def validation_SEARCH_CRITERIA(form):
    return True

def copy_SEARCH_CRITERIA(search_criteria_id_from):
    search_criteria_from = db.SEARCH_CRITERIA(db.SEARCH_CRITERIA.id==search_criteria_id_from) 
    i = 0
    if search_criteria_from:
        i = db.SEARCH_CRITERIA.insert(search_name = "--copy from " + search_criteria_from.search_name + " --"
                                     ,variant = search_criteria_from.variant
                                     ,attribute = search_criteria_from.attribute
                                     ,attribute_prev = search_criteria_from.attribute_prev
                                     )
        db.commit()
    return i
