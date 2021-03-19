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
import datetime
import vcf


# prova qualcosa come
def index(): 
    #db.SAMPLE.drop()
    #db.SAMPLE_VARIANT.drop()
    #db.SAMPLE_ATTRIBUTE.drop()
    #db.VCF_FILE.drop()
    
    return dict(message="hello from vcf.py")

def is_editable()  : return (auth.has_permission('manage', 'VCF'))
def is_create()   : return (auth.has_permission('manage', 'VCF'))
def is_readonly(): return ((auth.has_permission('view', 'VCF')) and (not (auth.has_permission('manage', 'VCF'))))
def is_deletable(): return (auth.has_permission('delete', 'VCF'))
    
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@cache.action()
def vcf_download():
    id = request.args(0)
    row = db(db.VCF_FILE.id == id).select().first()
    if row:
        (filename, stream) = db.VCF_FILE.vcf.retrieve(row.vcf)

        fh = open(stream.name, 'rb')
        stream.close()

        file_header = "attachment; filename=" + filename
        response.headers['ContentType'] = "application/octet-stream"
        response.headers['Content-Disposition'] = file_header

        return response.stream(fh)
    else:
        return None



########################
####   VCF import   ####
########################

@auth.requires_permission('import', 'VCF')
def import_file():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Import VCF')
    form_head=head_title(response.title,form_head_indietro)


    uploadfolder = os.path.join(request.folder,'uploads')

    form = FORM(DIV( LABEL(T('Files VCF'), _class='form-control-label col-sm-3')
                    ,DIV(INPUT(_name='file_upload', _type='file'
                               , _multiple=True #, _accept=".vcf,.VCF,.step2"
                              ,_class='upload input-file')
                        ,SPAN(T('select VCF files to upload'),_class='help-block')
                        ,_class='col-sm-9')
                   ,_class='form-group row'
                   )
               ,DIV(INPUT(_type='submit',_value=T('Import'),_class="btn btn-primary")
                    ,_class="col-sm-9 offset-sm-3"
                    )
               )

    if form.accepts(request.vars, onvalidation=validation_VCF_FILE_import):
        files = request.vars['file_upload'] 
        if files != '':
            if not isinstance(files, list): #convert files to a list if they are not one already.
                files = [files]
            for f in files:
                risp=insert_VCF_FILE(f)

            redirect(URL('vcf','list_edit'))

    return response.render(default_view, dict(form_head=form_head,form=form))


@auth.requires_permission('manage', 'VCF')
def list_edit():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Processes VCF')
    form_head=head_title(response.title,form_head_indietro)


    #prepara i dati per valorizzazione di default
    form_default = import_form_default()

    fields = [db.VCF_FILE.filename_upload
             ,db.VCF_FILE.date_upload
             ,db.VCF_FILE.file_upload
             ,db.VCF_FILE.VCF_TYPE_id
             ,db.VCF_FILE.PANEL_id
             ,db.VCF_FILE.VIRTUAL_PANEL_id
             ]
        
    db.VCF_FILE.VCF_TYPE_id.represent = lambda value,row:  options_widget(db.VCF_FILE.VCF_TYPE_id,value, _class="form-control",
                                                                               **{'_name':'VCF_TYPE_id_row_%s' % row.id})
    db.VCF_FILE.PANEL_id.represent = lambda value,row:  options_widget(db.VCF_FILE.PANEL_id,value, _class="form-control",
                                                                       **{'_name':'PANEL_id_row_%s' % row.id , '_cols':'2'})
    db.VCF_FILE.VIRTUAL_PANEL_id.represent = lambda value,row:  options_widget(db.VCF_FILE.VIRTUAL_PANEL_id,value, _class="form-control",
                                                                               **{'_name':'VIRTUAL_PANEL_id_row_%s' % row.id})

    db.VCF_FILE.filename_upload.label = ' '
    db.VCF_FILE.filename_upload.represent = lambda value, row: A('-> '
                                                                 , _href=URL('vcf_list'
                                                      ,vars=dict(VCF_FILE_id=row.id
                                                                ,form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                                                 , _target = 'blank')
 
    db.VCF_FILE.file_upload.label = T('VCF file')
    db.VCF_FILE.file_upload.represent = lambda value,row: A(('.. ' if len(row.filename_upload) > 50 else '') + row.filename_upload[-50:-4]  or T('file')
                                                            , _title=row.filename_upload , _href=URL('download', args=value))


    db.VCF_FILE.date_upload.represent = lambda value, row: value.strftime("%d/%m/%Y") if value else ''


    query= (db.VCF_FILE.fl_elaborated == 'N')

    default_sort_order=[~db.VCF_FILE.date_upload, db.VCF_FILE.filename_upload]


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
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #25
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,user_signature=False
                        ,selectable= lambda ids : [vcf_elabora(ids,request.post_vars)
                                                  ,redirect(URL('list_edit',vars=request._get_vars))
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

    return  dict(form_head=form_head,form_default=form_default,form_list=form_list)


def import_form_default():

    form = SQLFORM.factory(
        Field('VCF_TYPE_id' , type = db.VCF_FILE.VCF_TYPE_id.type
                                     , label = db.VCF_FILE.VCF_TYPE_id.label
                                     , requires = db.VCF_FILE.VCF_TYPE_id.requires
                                     , widget = db.VCF_FILE.VCF_TYPE_id.widget
             )
       ,Field('PANEL_id', type = db.VCF_FILE.PANEL_id.type
                               , label = db.VCF_FILE.PANEL_id.label
                               , requires = db.VCF_FILE.PANEL_id.requires
                               , widget = db.VCF_FILE.PANEL_id.widget
             )
       ,Field('VIRTUAL_PANEL_id', type = db.VCF_FILE.VIRTUAL_PANEL_id.type
                                       , label = db.VCF_FILE.VIRTUAL_PANEL_id.label
                                       , requires = db.VCF_FILE.VIRTUAL_PANEL_id.requires
                                       , widget = db.VCF_FILE.VIRTUAL_PANEL_id.widget
             )

#       ,submit_button = T("Submit")
       ,table_name = "default"
        )
#    submit = form.element("input",_type="submit")
#    submit["_type"]="button"
#    submit["_onclick"]="imposta_default()"
    return form

def vcf_elabora(ids,post_vars):
    # salvo i valori impostati 
    for id in ids:
        row = db(db.VCF_FILE.id == id).select().first()
        if not row: continue

        row.VCF_TYPE_id = post_vars['VCF_TYPE_id_row_'+ str(id)]
        row.PANEL_id=post_vars['PANEL_id_row_'+ str(id)]
        row.VIRTUAL_PANEL_id=post_vars['VIRTUAL_PANEL_id_row_'+ str(id)]

        row.update_record()
        db.commit()

    # rileggo gli id e faccio il parse
    for id in ids:
        risp = vcf_file_elab(id)
        if not risp: #risp = true tutto ok, altrimenti mi fermo
            return False

    return True
    """
        row = db(db.VCF_FILE.id == id).select().first()
        if not row: continue
        if (not row.VCF_TYPE_id) or (row.VCF_TYPE_id == 0):
            session.flash = T('VCF type doesn''t set for ') + '\n' + row.filename_upload
            return False

        if (not row.PANEL_id) or (row.PANEL_id == 0):
            session.flash = T('Panel doesn''t set for ') + '\n' + row.filename_upload
            return False

        row.fl_elaborated = 'X' #in elbaorazione
        row.update_record()
        db.commit()

        esito_parse = vcf_parse(id)
        if esito_parse == 1:
            db(db.VCF_FILE.id == id).update(fl_elaborated='Y')
            db.commit()
        elif esito_parse == -1:
            db(db.VCF_FILE.id == id).select().first()
            return False
        elif esito_parse == 0:
            db(db.VCF_FILE.id == id).select().first()
            session.flash = T('Error occured during parse of') + '\n' + row.filename_upload
            return False

    return True
    """

def vcf_file_elab(id):
    row = db(db.VCF_FILE.id == id).select().first()
    if not row:
        session.flash = T('VCF file is not exist') 
        return False
    if row.fl_elaborated!= 'N': 
        session.flash = T('The VCF file is not in the "not processed" state') 
        return False

    if (not row.VCF_TYPE_id) or (row.VCF_TYPE_id == 0):
        session.flash = T('VCF type doesn''t set for ') + '\n' + row.filename_upload
        return False

    if (not row.PANEL_id) or (row.PANEL_id == 0):
        session.flash = T('Panel doesn''t set for ') + '\n' + row.filename_upload
        return False

    row.fl_elaborated = 'X' #in elbaorazione
    row.update_record()
    db.commit()

    esito_parse = vcf_parse(id)
    if esito_parse == 1:
        db(db.VCF_FILE.id == id).update(fl_elaborated='Y')
        db.commit()
        return True
    elif esito_parse == -1: #errore in eval classif
        return False
    else:
        session.flash = T('Error during elaboration of file ') + '\n' + row.filename_upload + '\n\n Error:\n' + esito_parse
        return False

    return True

def vcf_parse(id):

    
    """
    #!/usr/bin/env python
import vcf

vcf_reader = vcf.VCFReader(open('prova1.vcf', 'rb'))
print vcf_reader.samples

for record in vcf_reader:
   print "CHROM: "
   print record.CHROM
   print "POS: "
   print record.POS
   print "ID: "
   print record.ID
   print "REF: "
   print record.REF
   print "ALT: "
   print record.ALT
   print "QUAL: "
   print record.QUAL
   print "FILTER: "
   print record.FILTER
   print "INFO: "
   print record.INFO
   print "FORMAT: "
   print record.FORMAT
   print "samples: "
   print record.samples

   #af = record.INFO['AF'][0]
   #print af
   for s in record.samples:
   	print s
	print s.sample

	print s.data
	print s.data.GT

    command = "af > 0.5"
    if eval(command): ...
    x=10
    command = "x+1"
    eval(command)

    """

    vcf_file = db(db.VCF_FILE.id == id).select().first()
    if not vcf_file: return 0

    #acquisizione parametri VCF_TYPE
    vcf_type_id = vcf_file.VCF_TYPE_id
    vcf_type = db(db.VCF_TYPE.id == vcf_type_id).select().first()
    if not vcf_type: return 0
    
    component_variant = string_to_list(vcf_type.variant)
    row_filter = vcf_type.row_filter
    sample_attribute = vcf_type.sample_attribute
    variant_attribute = vcf_type.variant_attribute

    #acquisizione geni pannello virtuale
    geni_ammessi=[]
    virtual_panel_id = vcf_file.VIRTUAL_PANEL_id
    if virtual_panel_id:
        virtual_panel = db(db.VIRTUAL_PANEL.id == virtual_panel_id).select().first()
        if virtual_panel:
            geni_ammessi = virtual_panel.gene.split(",")  #trasformo in lista

    #inizio parse vcf
    try:
        (filename,fullfilename) = db.VCF_FILE.file_upload.retrieve(vcf_file.file_upload,nameonly=True)
        # con nameonly=true riporta come secondo parametro il nome completo del file con percorso
        stream = open(fullfilename, 'rb')
        vcf_reader = vcf.VCFReader(stream)

        try:
            date_str = vcf_reader.metadata['fileDate']
            try:
                date_vcf = datetime.datetime.strptime(date_str, '%a %b %d  %H:%M:%S %Y')
            except Exception, e:
                try:
                    date_vcf = datetime.datetime.strptime(date_str, '%Y%m%d')
                except Exception, e:
                    date_vcf = datetime.datetime.now()
        except Exception, e:
            date_vcf = datetime.datetime.now()

        samples = vcf_reader.samples
        reference = vcf_reader.metadata['reference']
        hg = '-'
        if 'hg19' in reference:
            hg = 'hg19'
        if 'hg38' in reference:
            hg = 'hg38'

        update_data_in_VCF_FILE(id,date_vcf,hg,samples)

        contigs = vcf_reader.contigs
        #assembly = assembly['assembly']

        #ottimizzazione per non riaccedere sempre alla tabella SAMPLE in caso di unico sample
        sample_prec = ''

        for record in vcf_reader:
            #controllo se gene è in pannello virtale (se gene è nel vcf file e è stato impostato pannello virtuale)
            try:
                sgvep = record.INFO['SGVEP']
                if not isinstance(sgvep,list):
                    sgvep = [sgvep]

                gene = sgvep[0].split("|")[0]

            except Exception, e:
                gene = ''
            else:
                if geni_ammessi:
                    if len(gene)>0:
                        if gene not in geni_ammessi:
                            continue # prosegue alla riga successiva

            #estraggo variant
            variant = ''
            for c in component_variant:
                #esempio:
                #ref_string = '|'.join(map(str,record.REF))
                #alt_string = '|'.join(map(str,record.ALT))
                #variant =  '{}|{}|{}|{}'.format(record.CHROM, record.POS,ref_string,alt_string)  #sostituire con variante
                d = 'record.'+ c
                if eval(d):
                    e = eval(d)
                    if not isinstance(e,list):
                        e = [e]
                    if not isinstance(e[0],str):
                        f = map(str,e)
                    else:
                        f = e
                    g = '|'.join(f)
                    if variant == '':
                        variant = '{}'.format(g)
                    else:
                        variant = variant + '|{}'.format(g)
            #fine for c


            # dopo, solo se supera le regole di filtro row
            # variant_id = find_insert_VARIANT(hg,variant,gene,"")

            variant_id = 0
            for s in record.samples:# s.samlpe e s.data (FORMAT data)

                record_ok = True
                for f in row_filter:
                    f = f.replace("FORMAT", "s.data")
                    c = c.replace("INFO", "record.INFO")
                    if not eval(f):
                        record_ok = False
                if not record_ok :
                    continue

                if variant_id == 0:
                    #estraggo eventuali attributi indicati in VCF_TYPE per la variante
                    gene = ''
                    attribute = dict()
                    for a in variant_attribute:

                        at = a.split(":")
                        # prendo l'ultimo : come separatore della label .. in caso prima ci siano dei ":" nelle formule.
                        #c = at[0] #campo
                        #l = at[1] #label
                        c = ':'.join(at[:-1]) #campo
                        l = at[-1] #label
                        c = c.replace("FORMAT", "s.data")
                        c = c.replace("INFO", "record.INFO")

                        try:
                            c_val = eval(c)
                        except Exception, e:
                            c_val = ''

                        if not c_val=='': 
                            if not isinstance(c_val,list):
                                c_val = [c_val]
                            if not isinstance(c_val[0],str):
                                c_val = map(str,c_val)

                            v_at = '|'.join(c_val)
                            if l.upper() == 'GENE' :
                                gene = v_at
                            else:
                                attribute[l] = v_at

                    #registro la variante
                    variant_id = find_insert_VARIANT(hg,variant,gene,"",None)
                    #registro eventuali altri attributi oltre al gene
                    if attribute:
                        insert_VARIANT_ATTRIBUTE(variant_id, attribute,date_vcf)
                # fine variant

                sample = str(s.sample)
                if sample != sample_prec:
                    sample_id = insert_SAMPLE(sample, date_vcf, 'VCF', vcf_file.id)
                    sample_prec = sample

                """ 9/10/2019 con Sara. Più VCF file possono aggiornare lo stesso Sample: 
                questo caso non si verifica più

                if sample_id == -1 :
                    session.flash = T('Error occured during elaboration of') + '\n' + vcf_file.filename_upload +  '\n' + 'sample ' + sample + ' ' + T('already imported!')
                    stream.close #chiudo file stream aperto
                    return -1
                """
                sample_variant_id = insert_SAMPLE_VARIANT(sample_id,variant_id)

                if sample_variant_id:
                    #estraggo eventuali attributi indicati in VCF_TYPE per il sample
                    af = ''
                    gt = ''
                    attribute = dict()

                    for a in sample_attribute:

                        at = a.split(":")
                        c = at[0] #campo
                        l = at[1] #label
                        c = c.replace("FORMAT", "s.data")
                        c = c.replace("INFO", "record.INFO")

                        try:
                            c_val = eval(c)
                        except Exception, e:
                            c_val = ''

                        if not c_val=='': 
                            if not isinstance(c_val,list):
                                c_val = [c_val]
                            if not isinstance(c_val[0],str):
                                c_val = map(str,c_val)

                            v_at = '|'.join(c_val)
                            if l.upper() == 'AF' :
                                af = v_at
                            elif l.upper() == 'GT' :
                                gt = v_at
                            else:
                                attribute[l] = v_at

                    sample_variant_id = update_SAMPLE_VARIANT(sample_variant_id,af,gt)

                    if attribute:
                        insert_SAMPLE_VARIANT_ATTRIBUTE(sample_variant_id, attribute)
                #end if sample_variant_id

    except Exception, e:
        stream.close #chiudo file stream aperto
        return e.message
    else:
        stream.close #chiudo file stream aperto
        return 1


######################
####   VCF file   ####
######################
@auth.requires_permission('manage', 'VCF')
def vcf_elab():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    id = request.args(0)
    if id:
        r = vcf_file_elab(id)
        if r:
            session.flash = T('VCF file processed') 
    redirect(form_head_indietro)


@auth.requires_permission('view', 'VCF')
def vcf_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('VCF files')
    form_head=head_title(response.title,form_head_indietro)

    VCF_FILE_id = (request.vars['VCF_FILE_id']) if (request.vars['VCF_FILE_id']) else None
    VCF_FILE_ids= (request.vars['VCF_FILE_ids']) if (request.vars['VCF_FILE_ids']) else None

    links = [dict(header=''
             ,body=lambda row: A('', _title=T('Sample')
                                #,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                ,_class='btn btn-secondary btn-sm icon flask icon-flask glyphicon glyphicon-flask'
                                ,_href=URL("sample","list", vars=dict(VCF_FILE_id=row.id))
                                ,_target="blank") 
              )
             ,dict(header='',
               body=lambda row: A('', _title=T('Processes')
                        ,_class='btn btn-secondary btn-sm icon cogs icon-cogs glyphicon glyphicon-cog'
                        ,_href=URL("vcf","vcf_elab",args=[row.id]
                                   ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                 ) if is_editable() else ''
              )
             ]

    db.VCF_TYPE.id.readable=False
    db.VCF_TYPE.id.writeable=False

    fields = [db.VCF_FILE.file_upload
             ,db.VCF_FILE.filename_upload
             ,db.VCF_FILE.date_upload
             ,db.VCF_FILE.fl_elaborated
             ,db.VCF_FILE.VCF_TYPE_id
             ,db.VCF_FILE.PANEL_id
             ,db.VCF_FILE.VIRTUAL_PANEL_id
             ,db.VCF_FILE.date_vcf
             ,db.VCF_FILE.hg
             ,db.VCF_FILE.samples
             ]

    if VCF_FILE_id:
        query = db(db.VCF_FILE.id == VCF_FILE_id)
    elif VCF_FILE_ids:
        VCF_FILE_ids = [VCF_FILE_ids]
        query= (db.VCF_FILE.id.belongs(VCF_FILE_ids))
    else:
        query= (db.VCF_FILE)

    default_sort_order=[~db.VCF_FILE.date_upload,db.VCF_FILE.filename_upload]



    form = SQLFORM.grid(query=query
                        ,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=is_create()
                        ,deletable=is_deletable()
                        ,editable=is_editable()
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #20
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_VCF_FILE
                        ,ondelete= ondelete_VCF_FILE
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    return response.render(default_view, dict(form_head=form_head,form=form))


###########################
####   VCF file type   ####
###########################

@auth.requires_permission('view', 'VCF')
def vcf_type_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('VCF types')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('', _title=T('Duplicate')
                            ,_class='btn btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                            ,_href=URL('vcf_type_copy',args=[row.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                            ) if is_create() else ''
            ]

    db.VCF_TYPE.id.readable=False
    db.VCF_TYPE.id.writeable=False

    query= (db.VCF_TYPE)

    default_sort_order=[db.VCF_TYPE.name_type]



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
                        ,onvalidation=validation_VCF_TYPE
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    return response.render(default_view, dict(form_head=form_head,form=form))


@auth.requires_permission('view', 'VCF')
def vcf_type_copy():
    vcf_type_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not vcf_type_id:
        session.flash = T('error occured during call "Duplicate vcf type"')
        redirect(form_head_indietro)

    copy_VCF_TYPE(vcf_type_id)
    redirect(form_head_indietro)
    return


###################
####   PANEL   ####
###################

@auth.requires_permission('view', 'VCF')
def panel_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('VCF analysis panel')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('', _title=T('Edit')
                            ,_class='btn btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL('panel_edit',args=[row.id]
                                       ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           ) if is_editable() else ''
            ]


    db.PANEL.id.readable=False
    db.PANEL.id.writeable=False

    query= (db.PANEL)

    default_sort_order=[db.PANEL.name_panel]



    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        #,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=is_create()
                        ,deletable=is_deletable()
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=110
                        ,paginate=DEFAULT_PAGINATE #12
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_PANEL
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    return response.render(default_view, dict(form_head=form_head,form=form))

@auth.requires_permission('view', 'VCF')
def panel_edit():
    panel_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not panel_id:
        redirect(form_head_indietro)

    record = db.PANEL(db.PANEL.id==panel_id) or None


    response.title = T('Edit Panel')
    form_head=head_title(response.title,form_head_indietro)


    def is_readonly(): return ((auth.has_permission('view', 'VCF')) and (not (auth.has_permission('manage', 'VCF'))))

    if PANEL_is_used(record.id):
        db.PANEL.gene.writable  = False
        db.PANEL.gene.represent = lambda value,row: text_widget(db.PANEL.gene,value, _rows=4, _readonly='readonly')
    else:
        db.PANEL.gene.writable  = True


    form=SQLFORM(db.PANEL
                ,record
                ,readonly=is_readonly()
                ,deletable=False
                ,showid=False
                )

    if form.process(onvalidation=validation_PANEL).accepted:
        if form.deleted:
            session.flash = T('delete done')
            redirect(form_head_indietro)
        else:
            if record:
                response.flash = T('modify done')
            #else:
                # in inserimento di qui non passo mai, perchè questa funzione viene chiamata in editing
    return response.render(default_view, dict(form_head=form_head,form=form))


###########################
####   VIRTUAL PANEL   ####
###########################

@auth.requires_permission('view', 'VCF')
def virtual_panel_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    response.title = T('Virtual panel for VCF filtering')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('', _title=T('Edit')
                            ,_class='btn btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL('virtual_panel_edit',args=[row.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           ) if is_editable() else ''
            ]

    db.VIRTUAL_PANEL.id.readable=False
    db.VIRTUAL_PANEL.id.writeable=False

    query= (db.VIRTUAL_PANEL)

    default_sort_order=[db.VIRTUAL_PANEL.name_virtual_panel]


    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=is_create()
                        ,deletable=is_deletable()
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=110
                        ,paginate=DEFAULT_PAGINATE #12
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_VIRTUAL_PANEL
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    return response.render(default_view, dict(form_head=form_head,form=form))


@auth.requires_permission('view', 'VCF')
def virtual_panel_edit():
    virtual_panel_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not virtual_panel_id:
        redirect(form_head_indietro)

    response.title = T('Edit Virtual Panel')

    form_head=head_title(response.title,form_head_indietro)


    def is_readonly(): return ((auth.has_permission('view', 'VCF')) and (not (auth.has_permission('manage', 'VCF'))))

    if VIRTUAL_PANEL_is_used(record.id):
        db.VIRTUAL_PANEL.gene.writable  = False
        db.VIRTUAL_PANEL.gene.represent = lambda value,row: text_widget(db.VIRTUAL_PANEL.gene,value, _rows=4, _readonly='readonly')
    else:
        db.VIRTUAL_PANEL.gene.writable  = True

    record = db.VIRTUAL_PANEL(db.VIRTUAL_PANEL.id==virtual_panel_id) or None

    form=SQLFORM(db.VIRTUAL_PANEL
                ,record
                ,readonly=is_readonly()
                ,deletable=False
                ,showid=False
                )

    if form.process(onvalidation=validation_VIRTUAL_PANEL).accepted:
        if form.deleted:
            session.flash = T('delete done')
            redirect(form_head_indietro)
        else:
            if record:
                response.flash = T('modify done')
            #else:
                # in inserimento di qui non passo mai, perchè questa funzione viene chiamata in editing
    return response.render(default_view, dict(form_head=form_head,form=form))
