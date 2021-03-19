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

import os
import csv
import datetime 
import tempfile
import vcf
import zipfile

def delete_false_value():
    delete_false_VARIANT_ATTRIBUTE()
    return response.render(default_view, dict(form_head=FORM(DIV(T("Delete false value attribute in VARIANT_ATTRIBUTE"))),form=""))

def update_TEXT_FILE_ids():
    for row in db(db.SAMPLE.TEXT_FILE_ids==None).select():
        row.TEXT_FILE_ids = []
        row.update_record()
        db.commit()
    return response.render(default_view, dict(form_head=FORM(DIV(T("Update Text file ids in SAMPE"))),form=""))

def update_all_VARIANT_classif():
    for row in db(db.VARIANT.id>0).select():
        update_VARIANT_classif(row.id)
    return response.render(default_view, dict(form_head=FORM(DIV(T("Update all Variants classif"))),form=""))


def is_editable()  : return (auth.has_permission('manage', 'ANNOTATION'))
def is_deletable(): return   (auth.has_permission('delete', 'ANNOTATION'))


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

####################################
####   ANNOTATION export VCF    ####
####################################

@auth.requires_permission('import', 'ANNOTATION')
def export_vcf():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Export VCF for re-annotation')
    form_head=head_title(response.title,form_head_indietro)

    hg = request.vars.hg or 'hg19'
    form = SQLFORM.factory(
                            Field('hg' , type='string'
                                       , length = 1
                                       , label = T('Select hg reference for export')
                                       , requires = IS_IN_SET([('hg19',T('Hg 19')),('hg38',T('Hg 38'))])
                                       , default = hg
                                       , widget=lambda f,v : SQLFORM.widgets.radio.widget(f,v,style='table', cols=2, _width='30%')
                                       , id='hg'
                                 )
                           #,formstyle='bootstrap4_stacked' #'bootstrap4_stacked' #table3cols'#bootstrap3_inline'#'divs'
                           ,submit_button = T("export VCF")
                        )

    if form.accepts(request.vars):
        hg = form.vars.hg
        vcf_variants = []
        vcf_variants = compose_vcf(hg)
        
        #da qui per download su pc
        #se rimangono su fs, per successwiva elaborazione automatica, ricordarsi di 
        #gestire os.unlink(vcf_variant.name) #delete vcf_variant temporary file
        #
        #import zipfile
        # create zip of vcf_variant file
        if vcf_variants:
            zip_vcf_variants = tempfile.NamedTemporaryFile(prefix = "ALLVariant_"
                                                          ,suffix='.zip', delete=False) 
            with zipfile.ZipFile(zip_vcf_variants, 'w') as zipMe:
                for vcf_variant in vcf_variants:
                    file_name = os.path.basename(vcf_variant.name).split("|")
                    arcname = file_name[0]+".vcf"
                    zipMe.write(vcf_variant.name, arcname, compress_type=zipfile.ZIP_DEFLATED)
                    os.unlink(vcf_variant.name) #delete vcf_variant temporary file

            fh = open(zip_vcf_variants.name, 'rb')
            os.unlink(zip_vcf_variants.name) # delete zip_vcf_variants temporary file
            file_header = "attachment; filename=ALLVariant_" + datetime.datetime.now().strftime("%Y%m%d%H%M") + ".zip"
            response.headers['ContentType'] = "application/octet-stream"
            response.headers['Content-Disposition'] = file_header
            return response.stream(fh) #download zip_vcf_variants

    return response.render(default_view, dict(form_head=form_head,form=form))
    #return dict(form_head=form_head, form=form)

def compose_vcf(hg):
    vcf_variants=[]
    if hg == 'hg19':
        rows = db(db.VARIANT.id>0).select(db.VARIANT.id_hg19.with_alias('id_hg'))
    elif hg == 'hg38':
        rows = db(db.VARIANT.id>0).select(db.VARIANT.id_hg38.with_alias('id_hg'))
    else:
        return vcf_variants
    
    template = os.path.join(request.folder,VCF_VARIANT_TEMPLATE)
    vcf_template = vcf.Reader(filename=template)
    
    data_format = vcf_template.metadata['fileDate']
    vcf_template.metadata['fileDate'] = datetime.datetime.now().strftime(data_format)
    data_format = vcf_template.metadata['fileUTCtime'][0]
    vcf_template.metadata['fileUTCtime'][0] = datetime.datetime.utcnow().strftime(data_format)
    
    vcf_variant = tempfile.NamedTemporaryFile(prefix = "ALLVariant_1|"
                                             ,suffix='.vcf', delete=False) 
    vcf_variants.append (vcf_variant)
    vcf_writer = vcf.Writer(vcf_variant, vcf_template)
    record=None
    for r in vcf_template:
        record=r

    vcf_variant_max_rows = VCF_REANNOTATION_MAX_ROW
    r_count = 0
    for r in rows:
        if r.id_hg == "" or r.id_hg == None:
            continue
        r_count= r_count+1
        if vcf_variant_max_rows != 0:
            if r_count % vcf_variant_max_rows == 0: # create new vcf file every vcf_variant_max_rows rows to permit to be managed form the subsequent elaboration 
                vcf_writer.close()
                vcf_variant.close()
                n = (r_count // vcf_variant_max_rows ) +1  #// no decimal
                vcf_variant = tempfile.NamedTemporaryFile(prefix = "ALLVariant_" + str(n) + "|"
                                                         ,suffix='.vcf', delete=False)
                vcf_variants.append (vcf_variant)
                vcf_writer = vcf.Writer(vcf_variant, vcf_template)
            #endif
        #endif
        #for record in vcf_template:
        #"CHROM"|"POS"|"REF"|"ALT"
        id_hg = r.id_hg.split("|")
        if len(id_hg)== 4:
            record.CHROM = id_hg[0]
            record.POS = id_hg[1]
            record.REF = id_hg[2]
            record.ALT[0] = id_hg[3]
            vcf_writer.write_record(record)
            vcf_writer.flush()
        #endif
    ##end for record
    #end for r
    vcf_writer.close()
    vcf_variant.close()

    return vcf_variants

###############################
####   ANNOTATION import   ####
###############################

@auth.requires_permission('import', 'ANNOTATION')
def import_file():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    if form_head_indietro == None:
        form_head_indietro = URL('annotation','list_edit')

    response.title = T('Import Text files')
    form_head=head_title(response.title,form_head_indietro)

    uploadfolder = os.path.join(request.folder,'uploads')

    form = FORM(DIV( LABEL(T('Text Files'), _class='form-control-label col-sm-3')
                    ,DIV(INPUT(_name='file_upload', _type='file'
                               , _multiple=True #, _accept=".txt,.csv,.tsv"
                              ,_class='upload input-file')
                        ,SPAN(T('select Text files to upload'),_class='help-block')
                        ,_class='col-sm-9')
                   ,_class='form-group row'
                   )
               ,DIV(INPUT(_type='submit',_value=T('Import'),_class='btn btn-primary')
                        ,_class='col-sm-9 offset-sm-3'
                    )
               )

    if form.accepts(request.vars, onvalidation=validation_ANNOTATION_FILE_import):
        files = request.vars['file_upload'] 
        if files != '':
            if not isinstance(files, list): #convert files to a list if they are not one already.
                files = [files]
            for f in files:
                file_upload = db.ANNOTATION_FILE.file_upload.store(f,f.filename)
                risp=insert_ANNOTATION_FILE(file_upload,f.filename)
            redirect(form_head_indietro)

    return response.render(default_view, dict(form_head=form_head,form=form))
    #return dict(form_head=form_head, form=form)

@auth.requires_permission('manage', 'ANNOTATION')
def list_edit():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Processes Text files')
    form_head=head_title(response.title,form_head_indietro)

    #prepara i dati per valorizzazione di default
    form_default = import_form_default()

    fields = [db.ANNOTATION_FILE.filename_upload
             ,db.ANNOTATION_FILE.date_upload
             ,db.ANNOTATION_FILE.file_upload
             ,db.ANNOTATION_FILE.date_valid_from
             ,db.ANNOTATION_FILE.ANNOTATION_TYPE_id
             ]

    db.ANNOTATION_FILE.ANNOTATION_TYPE_id.represent = lambda value,row:options_widget(db.ANNOTATION_FILE.ANNOTATION_TYPE_id
                                                                                       ,value, _class="form-control row"
                                                                                       ,**{'_name':'ANNOTATION_TYPE_id_row_%s' % row.id})

    db.ANNOTATION_FILE.date_valid_from.requires = IS_EMPTY_OR(IS_DATE(format='%d/%m/%Y'))
    db.ANNOTATION_FILE.date_valid_from.represent = lambda value,row:  date_widget(db.ANNOTATION_FILE.date_valid_from
                                                                                  ,value, _class="date form-control row",
                                                                               **{'_name':'date_valid_from_row_%s' % row.id})

    db.ANNOTATION_FILE.filename_upload.label = ' '
    db.ANNOTATION_FILE.filename_upload.represent = lambda value, row: A('-> ', _href=URL('annotation','annotation_file_list'
                                                                                         ,vars=dict(ANNOTATIO_FILE_id=row.id))
                                                                        , _target = 'blank')

    db.ANNOTATION_FILE.date_upload.represent = lambda value, row: value.strftime("%d/%m/%Y %H:%M") if value else ''
    
    db.ANNOTATION_FILE.file_upload.label = T('Text file')
    db.ANNOTATION_FILE.file_upload.represent = lambda value,row: A(('.. ' if len(row.filename_upload) > 50 else '') + row.filename_upload[-50:-4]  or T('file')
                                                            , _title=row.filename_upload , _href=URL('download', args=value))


    query= (db.ANNOTATION_FILE.fl_elaborated == 'N')

    default_sort_order=[~db.ANNOTATION_FILE.date_upload, db.ANNOTATION_FILE.filename_upload]


    form_list = SQLFORM.grid(query=query
                        ,fields=fields
                        #,headers=headers
                        #,links = links
                        #,links_in_grid = True
                        ,orderby=default_sort_order
                        ,searchable=True
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        #,sorter_icons=(XML('&#x2191;'), XML('&#x2193;'))
                        ,showbuttontext=False
                        ,maxtextlength=50
                        #,maxtextlengths=maxtextlengths
                        ,paginate=DEFAULT_PAGINATE #25
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,user_signature=False
                        ,selectable= lambda ids : [list_edit_elab(ids,request.post_vars)
                                                  ,redirect(URL('annotation','list_edit',vars=request._get_vars))
                                                  ]
                        ,selectable_submit_button=T('Submit')
                       )

    heading = form_list.elements('th') #cerco l'intestazione della tabella
    if heading:
        heading[0].append(INPUT(_type='checkbox'
        ,_name = 'records_select'
        ,_onclick="jQuery('input[name=records]').each(function(){jQuery(this).prop('checked',!jQuery(this).prop('checked'));});"
                               )
                         )
    #form.elements(_type='checkbox',_name='records',replace=None)  #remove selectable's checkboxes
    #form_list.element('.web2py_counter', replace=None) # toglie numero records trovati


    #return response.render(default_view, dict(form_head=form_head,form=form_list))
    return  dict(form_head=form_head,form_default=form_default,form_list=form_list)


def import_form_default():

    form = SQLFORM.factory(
        Field('date_valid_from' , type = db.ANNOTATION_FILE.date_valid_from.type
                                     , label = db.ANNOTATION_FILE.date_valid_from.label
                                     , requires = db.ANNOTATION_FILE.date_valid_from.requires
                                     , widget = db.ANNOTATION_FILE.date_valid_from.widget
             ),
        Field('ANNOTATION_TYPE_id' , type = db.ANNOTATION_FILE.ANNOTATION_TYPE_id.type
                                     , label = db.ANNOTATION_FILE.ANNOTATION_TYPE_id.label
                                     , requires = db.ANNOTATION_FILE.ANNOTATION_TYPE_id.requires
                                     , widget = db.ANNOTATION_FILE.ANNOTATION_TYPE_id.widget
             )

       ,table_name = "default"
        )

    return form

def list_edit_elab(ids,post_vars):
    # salvo i valori impostati 
    for id in ids:
        row = db(db.ANNOTATION_FILE.id == id).select().first()
        if not row: continue
        if row.fl_elaborated!= 'N': continue # nel frammepo qualcuno lo ha elaborato (Y) o lo sta elaborando (X)

        row.ANNOTATION_TYPE_id = post_vars['ANNOTATION_TYPE_id_row_'+ str(id)]
        v = post_vars['date_valid_from_row_'+ str(id)]
        try:
            datetime.datetime.strptime(v, '%d/%m/%Y')
        except ValueError:
            v = ''
        if (v == ''):
            row.date_valid_from = ''
        else:
            row.date_valid_from = datetime.datetime.strptime(v, '%d/%m/%Y').strftime("%Y-%m-%d")
 
        row.update_record()
        db.commit()

    # rileggo gli id e faccio il parse
    for id in ids:
        risp = annotation_file_elab(id)
        if not risp: #risp = true tutto ok, altrimenti mi fermo
            return False

    return True


def annotation_file_elab(id):
    row = db(db.ANNOTATION_FILE.id == id).select().first()
    if not row: 
        session.flash = T('Text file is not exist') 
        return False
    if row.fl_elaborated!= 'N': 
        session.flash = T('Text file is not in the "not processed" state') 
        return False
    if (not row.ANNOTATION_TYPE_id) or (row.ANNOTATION_TYPE_id == 0):
        session.flash = T('Text type not set for ') + '\n' + row.filename_upload
        return False
    if (not row.date_valid_from) or (row.date_valid_from == ''):
        session.flash = T('Date valid from not set for ') + '\n' + row.filename_upload
        return False

    row.fl_elaborated = 'X' #in processing

    row.update_record()
    db.commit()

    esito_parse = annotation_parse(id)
    if esito_parse == 1:
        db(db.ANNOTATION_FILE.id == id).update(fl_elaborated='Y')
        db.commit()
        return True
    elif esito_parse == -1: #errore in eval classif
        return False
    else:
        session.flash = T('Error during elaboration of file ') + '\n' + row.filename_upload + '\n\n Error:\n' + esito_parse
        return False

    return True


def annotation_parse(id):

    annotation_file = db(db.ANNOTATION_FILE.id == id).select().first()
    if not annotation_file: return 0

    date_valid_from_annotation = annotation_file.date_valid_from

    #acquisizione parametri ANNOTATION_TYPE
    annotation_type_id = annotation_file.ANNOTATION_TYPE_id
    annotation_type = db(db.ANNOTATION_TYPE.id == annotation_type_id).select().first()
    if not annotation_type: return 0

    char_sep = str(annotation_type.char_sep)
    if char_sep == None:
        char_sep = "\t"

    component_sample = string_to_list(annotation_type.sample)
    component_variant_hg19 = string_to_list(annotation_type.variant_hg19)
    component_variant_hg38 = string_to_list(annotation_type.variant_hg38)
    component_gene = string_to_list(annotation_type.gene)
    component_classif = string_to_list(annotation_type.classif)
    classif_eval = annotation_type.classif_eval
    if classif_eval == None:
        classif_eval = ''
    component_classif_valid_from = list_to_dict(annotation_type.classif_valid_from)

    row_filter = annotation_type.row_filter
    if row_filter == None:
        row_filter = ''
    break_condition = annotation_type.break_condition
    if break_condition == None:
        break_condition = ''
    component_attribute = list_to_dict(annotation_type.variant_attribute)
    component_single_attribute = list()
    for c in component_attribute.keys():
        if "|" in c:
            list_c = string_to_list(c)
            component_single_attribute.extend(list_c)
        else:
            component_single_attribute.append(c)

    sample_prec = ''
    try:
    #if 1==1:

        (filename,fullfilename) = db.ANNOTATION_FILE.file_upload.retrieve(annotation_file.file_upload,nameonly=True)
        # con nameonly=true riporta come secondo parametro il nome completo del file con percors
        file_reader = csv.reader(open(fullfilename, 'r'), delimiter=char_sep)

        colonna = dict()
        #numero della colonna in cui trovo l'elemento della variante, gene, classif o parametro
        intestazione = next(file_reader)
        if not isinstance(intestazione,list):
            intestazione = [intestazione]

        for i in intestazione:
            I = i.upper()
            if not I in colonna.keys(): #if more colums with the same name, set the first.
                if I in (x.upper() for x in component_variant_hg19):
                    colonna[I] = intestazione.index(i)
                if I in (x.upper() for x in component_variant_hg38):
                    colonna[I] = intestazione.index(i)
                if I in (x.upper() for x in component_sample):
                    colonna[I] = intestazione.index(i)
                if I in (x.upper() for x in component_gene):
                    colonna[I] = intestazione.index(i)
                if I in (x.upper() for x in component_classif):
                    colonna[I] = intestazione.index(i)
                if I in (x.upper() for x in component_classif_valid_from):
                    colonna[I] = intestazione.index(i)
                if I in (x.upper() for x in component_single_attribute):
                    colonna[I] = intestazione.index(i)

        # in colonna ho le posizioni di tutti i campi che mi interessano


        for row in file_reader:
            if not row:
                continue

            #controllo condizione di break
            record_ok = True
            if break_condition:
                for c in break_condition:
                    try :
                        c_eval = eval(c)
                    except Exception, e:
                        continue # condizione di break non valutabile, continuo
                    else:
                        if c_eval: #condizione di break verificata
                            record_ok = False
                            break #uscita dalle condizioni

            if not record_ok :
                break # esco da lettura file_reader

            # controllo se la riga è da considerare -> row_filer true
            record_ok = True
            for f in row_filter:
                try :
                    f_eval = eval(f)
                except Exception, e:
                    record_ok = False # condizione di riga ok non valutabile, allora record non ok
                    break
                else:
                    if not f_eval:
                        record_ok = False
                        break

            if not record_ok :
                continue

            sample = ''
            for c in component_sample:
                C = c.upper()
                if row[colonna[C]]!="":
                    sample = sample + row[colonna[C]] + "|"
            sample = sample[:-1]
            sample = sample.strip()

            variant_hg19 = ''
            for c in component_variant_hg19:
                C = c.upper()
                if row[colonna[C]]!="":
                    variant_hg19 = variant_hg19 + row[colonna[C]] + "|"
            variant_hg19 = variant_hg19[:-1]
            variant_hg19 = variant_hg19.strip()

            variant_hg38 = ''
            for c in component_variant_hg38:
                C = c.upper()
                if row[colonna[C]]!="":
                    variant_hg38 = variant_hg38 + row[colonna[C]] + "|"
            variant_hg38 = variant_hg38[:-1]
            variant_hg38 = variant_hg38.strip()

            gene = ''
            for c in component_gene:
                C = c.upper()
                if row[colonna[C]]!="":
                    gene = gene + row[colonna[C]] + "|"
            gene = gene[:-1]
            gene = gene.strip()

            classif = ''
            for c in component_classif:
                C = c.upper()
                #if row[colonna[c]]!="": nel caslo della classe, se ha più componenti li prendo anche nulli, per poter fare l'evaluate dopo
                classif = classif + row[colonna[C]] + "|"
            classif = classif[:-1]

            #eval classif per gestione logiche semplici ( classif[0:1] )
            #o complesse come "classif[0][0:1] if classif[0][1:1]=='1' else 'C'+classif[1][0:0]
            if classif_eval.strip()!="":
                #trasformo classif in lista
                string = classif
                if '|' in string:
                    classif = string.split('|') #trasformo in lista
                else:
                    classif = string
                if not isinstance(classif,list):
                    classif = [classif]
                try :
                    classif = eval(classif_eval)
                except Exception, e:
                    session.flash = T('Error for eval classif in ') + '\n' + annotation.filename_upload  + '\n' + 'classif eval = ' + classif_eval
                    return -1

            classif = classif.strip()

            classif_valid_from = None
            if classif != '':
                valid_from = ''
                classif_valid_from_format=''
                for c in component_classif_valid_from.keys():
                    classif_valid_from_format = component_classif_valid_from[c]
                    C = c.upper()
                    valid_from = valid_from + row[colonna[C]] + "|"
                valid_from = valid_from[:-1].strip()

                if valid_from== '':
                    valid_from = date_valid_from_annotation
                try:
                    classif_valid_from = datetime.datetime.strptime(valid_from, classif_valid_from_format)
                except Exception, e:
                    classif_valid_from = datetime.datetime.now()

            #fine classif

            attribute = dict()
            for c in component_attribute.keys():
                lab = component_attribute[c]
                # if "|" in c: # se sono campi concatenati, devo prendere i singoli valori e concatenarli con |
                list_c = string_to_list(c)
                v = ''
                if len(list_c) > 1:
                    for d in list_c:
                        D = d.upper()
                        if colonna[D]:
                            if row[colonna[D]]=="":
                                v = v + " |"
                            else:
                                v = v + row[colonna[D]] + "|"
                    v = v[:-1]
                    p = v.replace("|","")
                    if p.strip() == "" :
                        v = ""
                elif len(list_c) == 1:
                    D = list_c[0].upper()
                    if colonna[D]:
                        v = row[colonna[D]]
                        p = v.replace("|","")
                        if p.strip() == "" :
                            v = ""

                attribute[lab] = v
            #fine attribute

            #ho tutto, posso insierire/aggiornare i dati
            variant_id=0
            if variant_hg19 !="":
                variant_id = find_insert_VARIANT('hg19',variant_hg19,gene,classif,classif_valid_from)
                if variant_id > 0 and variant_hg38 !="": #se ho anche hg38, aggiorno variante
                    update_VARIANT(variant_id,variant_hg19,variant_hg38,gene,classif,classif_valid_from)
            elif variant_hg38 !="":
                variant_id = find_insert_VARIANT('hg38',variant_hg38,gene,classif,classif_valid_from)
            if variant_id > 0:
                insert_VARIANT_ATTRIBUTE(variant_id, attribute,date_valid_from_annotation)

            if sample!=None and sample != '':
                if sample != sample_prec:
                    sample_id = insert_SAMPLE(sample,date_valid_from_annotation, 'TEXT', annotation_file.id)
                    sample_prec = sample
                if variant_id > 0:
                    sample_variant_id = insert_SAMPLE_VARIANT(sample_id,variant_id)

        #fine lettura file_reader

    except Exception , e:
        return e.message
    else:
        return 1



#############################
####   ANNOTATION file   ####
#############################

@auth.requires_permission('manage', 'ANNOTATION')
def annotation_elab():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    id = request.args(0)
    if id:
        r = annotation_file_elab(id)
        if r:
            session.flash = T('Text file processed') 
    redirect(form_head_indietro)

@auth.requires_permission('view', 'ANNOTATION')
def annotation_file_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    response.title = T('Text files')
    form_head=head_title(response.title,form_head_indietro)

    ANNOTATION_FILE_id = (request.vars['ANNOTATION_FILE_id']) if (request.vars['ANNOTATION_FILE_id']) else None
    ANNOTATION_FILE_ids = (request.vars['ANNOTATION_FILE_ids']) if (request.vars['ANNOTATION_FILE_ids']) else None

    links = [dict(header=''
                 ,body=lambda row: A('', _title=T('Sample')
                                    #,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_class='btn btn-secondary btn-sm icon flask icon-flask glyphicon glyphicon-flask'
                                    ,_href=URL("sample","list", vars=dict(TEXT_FILE_id=row.id))
                                    ,_target="blank") 
                  )
            ,dict(header='',
                   body=lambda row: A('', _title=T('Processes')
                            ,_class='btn btn-secondary btn-sm icon cogs icon-cogs glyphicon glyphicon-cog'
                            ,_href=URL('annotation_elab',args=[row.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                     ) if is_editable() else ''
                  )
            ]


    if ANNOTATION_FILE_id:
        query = db(db.ANNOTATION_FILE.id == ANNOTATION_FILE_id)
    elif ANNOTATION_FILE_ids:
        ANNOTATION_FILE_ids = [ANNOTATION_FILE_ids]
        query = db(db.ANNOTATION_FILE.id.belongs(ANNOTATION_FILE_ids))
    else:
        query= (db.ANNOTATION_FILE)

    default_sort_order=[~db.ANNOTATION_FILE.date_upload,db.ANNOTATION_FILE.filename_upload ]


    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable=is_deletable()
                        ,editable=is_editable()
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #25
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_ANNOTATION_FILE
                        ,ondelete= ondelete_ANNOTATION_FILE
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati
    return response.render(default_view, dict(form_head=form_head,form=form))



#############################
####   ANNOTATION type   ####
#############################

@auth.requires_permission('view', 'ANNOTATION')
def annotation_type_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    response.title = T('Text file types')
    form_head=head_title(response.title,form_head_indietro)

    def is_create()      :return (auth.has_permission('manage', 'ANNOTATION'))
    
    links = [(lambda row: A('', _title=T('Duplicate')
                            ,_class='btn btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                            ,_href=URL('annotation_type_copy',args=[row.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           ) if is_create() else '')
            ]

    db.ANNOTATION_TYPE.id.readable=False
    db.ANNOTATION_TYPE.id.writeable=False

    query= (db.ANNOTATION_TYPE)
    default_sort_order=[db.ANNOTATION_TYPE.name_type]


    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        #,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=is_create()
                        ,deletable=is_deletable()
                        ,editable=is_editable()
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #8
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_ANNOTATION_TYPE
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati
    return response.render(default_view, dict(form_head=form_head,form=form))

@auth.requires_permission('view', 'ANNOTATION')
def annotation_type_copy():
    annotation_type_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    if not annotation_type_id:
        session.flash = T('error occured during call "Duplicate Text file type')
        redirect(form_head_indietro)

    copy_ANNOTATION_TYPE(annotation_type_id)
    redirect(form_head_indietro)
    return
