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


#########################
####   TISSUE TYPE   ####
#########################

@auth.requires_permission('manage', 'SAMPLE')
def tissue_type_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Tissue Type for sample')
    form_head=head_title(response.title,form_head_indietro)

    db.TISSUE_TYPE.id.readable=False
    db.TISSUE_TYPE.id.writeable=False

    query= (db.TISSUE_TYPE)


    default_sort_order=[db.TISSUE_TYPE.tissue_type]

    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        #,links = links
                        #,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=True
                        ,deletable=True
                        ,editable=True
                        ,details=False
                        #,sorter_icons=(XML('&#x2191;'), XML('&#x2193;'))
                        ,showbuttontext=False
                        ,maxtextlength=50
                        #,maxtextlengths=maxtextlengths
                        ,paginate=DEFAULT_PAGINATE #10
                        ,csv = True
                        ,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_TISSUE_TYPE
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati
    return response.render(default_view, dict(form_head=form_head,form=form))



####################
####   SAMPLE   ####
####################
@auth.requires_permission('view', 'SAMPLE')
def list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Samples')
    form_head=head_title(response.title,form_head_indietro)

    VCF_FILE_id = (request.vars['VCF_FILE_id']) if (request.vars['VCF_FILE_id']) else None
    TEXT_FILE_id = (request.vars['TEXT_FILE_id']) if (request.vars['TEXT_FILE_id']) else None

    links = [lambda row: A('', _title=T('Detail')
                            ,_class='button btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL('edit',args=[row.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                          )
            ,lambda row: A(str(num_variants_of_sample(row.id))
                                      ,_title=T('Variants')
                                      ,_class='btn btn-success btn-sm'
                                      ,_href=URL('sample_variant','variants_of_sample',args=[row.id])
                                      ,_target='blank'
                                       ) if num_variants_of_sample(row.id)>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                                     else SPAN(str(num_variants_of_sample(row.id)),_class='btn btn-success btn-sm')\
                                       if num_variants_of_sample(row.id)>0 else ''
            ,dict(header='',
                   body=lambda row: A('vcf'
                                      ,_class='btn btn-link btn-sm'
                                      ,_href=URL('vcf','vcf_list',vars=dict(VCF_FILE_ids=row.VCF_FILE_ids))
                                      ,_target='blank'
                                       ) if row.VCF_FILE_ids else ''
                )
             ,dict(header='',
                   body=lambda row: A('text'
                                      ,_class='btn btn-link btn-sm'
                                      ,_href=URL('annotation','annotation_file_list',vars=dict(ANNOTATION_FILE_ids=row.TEXT_FILE_ids))
                                      ,_target='blank'
                                       ) if row.TEXT_FILE_ids else ''
                )
            ]

    #db.SAMPLE.VCF_FILE_ids.readable=False
    #db.SAMPLE.TEXT_FILE_ids.readable=False

    db.SAMPLE.id.readable=False
    db.SAMPLE.id.writeable=False

    query = (db.SAMPLE)
    if VCF_FILE_id!= None:
        query = db(db.SAMPLE.VCF_FILE_ids.contains(VCF_FILE_id))
    if TEXT_FILE_id!= None:
        query = db(db.SAMPLE.TEXT_FILE_ids.contains(TEXT_FILE_id))

    default_sort_order=[~db.SAMPLE.date_sample,db.SAMPLE.sample]



    form= SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=True
                        ,deletable=False 
                        ,editable=False
                        ,details=False
                        ,searchable=True
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #10
                        ,csv = True
                        ,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_SAMPLE
                        ,oncreate=oncreate_SAMPLE
                        ,user_signature=False
                        ,args=request.args[:1]
                       )
    return response.render(default_view, dict(form_head=form_head,form=form))


@auth.requires_permission('manage', 'SAMPLE')
def list_edit():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Samples manage')
    form_head=head_title(response.title,form_head_indietro)

    #prepara i dati per valorizzazione di default
    form_default = list_form_default()


    links = [lambda row: A('', _title=T('Detail')
                            ,_class='button btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL('edit',args=[row.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                          )
            ,dict(header='VCF/Text files', body=lambda row: (SAMPLE_files_list('VCF'
                                                                            ,row.VCF_FILE_ids) 
                                                          + "\n " + 
                                                          SAMPLE_files_list('TEXT',row.TEXT_FILE_ids)).strip()[:40]
                  )
             ]


    db.SAMPLE.fl_sample_type.represent = lambda value,row:  options_widget(db.SAMPLE.fl_sample_type,value, _class="form-control",
                                                                           **{'_name':'fl_sample_type_row_%s' % row.id})
    db.SAMPLE.TISSUE_TYPE_id.represent = lambda value,row:  options_widget(db.SAMPLE.TISSUE_TYPE_id,value, _class="form-control",
                                                                           **{'_name':'TISSUE_TYPE_id_row_%s' % row.id})
    db.SAMPLE.fl_sex.represent = lambda value,row:  options_widget(db.SAMPLE.fl_sex,value, _class="form-control",
                                                                   **{'_name':'fl_sex_row_%s' % row.id})


    db.SAMPLE.VCF_FILE_ids.readable = False
    db.SAMPLE.TEXT_FILE_ids.readable = False

    db.SAMPLE.id.readable=False
    db.SAMPLE.id.writeable=False

    query = (db.SAMPLE)

    default_sort_order=[~db.SAMPLE.date_sample,db.SAMPLE.sample]


    form_list = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,searchable=True
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #10
                        ,csv = False   #non funziona con modifica campi in input
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_SAMPLE
                        ,oncreate=oncreate_SAMPLE
                        ,user_signature=False
                        ,args=request.args[:1]
                        ,selectable= lambda ids : [sample_elabora(ids,request.post_vars)
                                                  ,redirect(URL('list_edit',vars=request._get_vars))
                                                  ]
                        ,selectable_submit_button=T('Submit')
                       )

    #preseneziono tutti gli id della pagina, poi li nascondo per fare in modo che tutti quelli modificati vengano salvati
    #check_record = form_list.elements(_type='checkbox',_name='records') 
    #for ck in check_record:
    #    ck["_checked"] = "True"
    #    ck["_style"] = "display:none"
    #trovato soluzione migliore: si preselezionano quando si fa una modifica 
    
    #form_list.element('.web2py_counter', replace=None) # toglie numero records trovati

    return  dict(form_head=form_head,form_default=form_default,form_list=form_list)


def list_form_default():

    form = SQLFORM.factory(
        Field('fl_sample_type', type = db.SAMPLE.fl_sample_type.type
                                     , label = db.SAMPLE.fl_sample_type.label
                                     , requires = db.SAMPLE.fl_sample_type.requires
                                     , widget = db.SAMPLE.fl_sample_type.widget
             )
       ,Field('TISSUE_TYPE_id', type = db.SAMPLE.TISSUE_TYPE_id.type
                                     , label = db.SAMPLE.TISSUE_TYPE_id.label
                                     , requires = db.SAMPLE.TISSUE_TYPE_id.requires
                                     , widget = db.SAMPLE.TISSUE_TYPE_id.widget
             )
       ,Field('fl_sex', type = db.SAMPLE.fl_sex.type
                             , label = db.SAMPLE.fl_sex.label
                             , requires = db.SAMPLE.fl_sex.requires
                             , widget = db.SAMPLE.fl_sex.widget
             )
#       ,submit_button = T("Submit")
       ,table_name = "default"
        )
#    submit = form.element("input",_type="submit")
#    submit["_type"]="button"
#    submit["_onclick"]="imposta_default()"
    return form


def sample_elabora(ids,post_vars):
    for id in ids:
        row = db(db.SAMPLE.id == id).select().first()
        if not row: return False

        row.fl_sample_type = post_vars['fl_sample_type_row_'+ str(id)]
        row.TISSUE_TYPE_id=post_vars['TISSUE_TYPE_id_row_'+ str(id)]
        row.fl_sex=post_vars['fl_sex_row_'+ str(id)]

        row.update_record()


def oncreate_SAMPLE(form):
    if 'new' in request.args:
        session.flash = T('insert done')
        redirect(URL('edit',args=[form.vars.id],vars=dict(form_head_indietro='list')))
    return True


@auth.requires_permission('view', 'SAMPLE')
def edit():
    sample_id = request.args(0)

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not sample_id:
        return dict(form_head='',form='',btn_variants_of_sample='')

    response.title = T('Edit Sample')
    form_head=head_title(response.title,form_head_indietro)

    record = db.SAMPLE(db.SAMPLE.id==sample_id) or None


    db.SAMPLE.VCF_FILE_ids.writable = False
    db.SAMPLE.VCF_FILE_ids.requires=IS_EMPTY_OR(IS_NOT_EMPTY(), null='') #tolgo controllo esistenza nel db, poichè è in sola lettura
    
    #db.SAMPLE.VCF_FILE_ids.represent = lambda value,row: string_widget(db.SAMPLE.VCF_FILE_ids,SAMPLE_files_list(value).replace("\n","  "), _readonly='readonly')

    #union in one filed both VCF and TEXT files origin
    db.SAMPLE.VCF_FILE_ids.label = T('VCF/Text files')
    db.SAMPLE.VCF_FILE_ids.represent = lambda value,row: text_widget(db.SAMPLE.VCF_FILE_ids,(SAMPLE_files_list('VCF',row.VCF_FILE_ids) + " " + SAMPLE_files_list('TEXT',row.TEXT_FILE_ids)).replace("\n","  ").strip(), _readonly='readonly',_rows = '2')
    db.SAMPLE.TEXT_FILE_ids.readable = False

    def is_readonly(): return ((auth.has_permission('view', 'SAMPLE')) and (not (auth.has_permission('manage', 'SAMPLE'))))
    def is_deletable(): return   (auth.has_permission('delete', 'SAMPLE'))

    form=SQLFORM(db.SAMPLE
                ,record
                ,readonly=is_readonly()
                ,deletable=is_deletable()
                ,showid=False
                )

    if form.process(onvalidation=validation_SAMPLE).accepted:
        if form.deleted:
            session.flash = T('delete done')
            redirect(form_head_indietro)
        else:
            if record:
                response.flash = T('modify done')
            #else:
                # in inserimento di qui non passo mai, perchè questa funzione viene chiamata solo per editing

    btn_variants_of_sample = A(str(num_variants_of_sample(record.id))
                              ,_class='btn btn-default btn-secondary btn-sm'
                              ,_title=T('Variants')
                              ,_href=URL('sample_variant','variants_of_sample',args=[record.id])
                              ,_target='blank'
                              ) if auth.has_permission('view', 'SAMPLE_VARIANT')\
                                else SPAN(str(num_variants_of_sample(record.id)),_class='btn btn-default btn-secondary btn-sm')


    #return response.render(default_view, dict(form_head=form_head,form=form, iframe=iframe_attribute))
    return dict(form_head=form_head,form=form,btn_variants_of_sample=btn_variants_of_sample)
