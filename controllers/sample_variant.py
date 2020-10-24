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

def is_manage()     :return (auth.has_permission('manage', 'SAMPLE_VARIANT'))

@auth.requires_permission('view', 'SAMPLE_VARIANT')
def list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Samples and variants')
    form_head=head_title(response.title,form_head_indietro)

    links = [(lambda row: A('Sample',_title=T('Edit Sample')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("sample","edit" ,args=[sample_id_of(row[field_id])])
                                    ,_target="blank"
                                    ,_name='btn_sample_edit') if auth.has_permission('view', 'SAMPLE') else ''
             )
            ,dict(header=''
                 ,body=lambda row: A('Variant', _title=T('Edit Variant')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","edit" ,args=[variant_id_of(row[field_id])])
                                    ,_target="blank"
                                    ,_name='btn_variant_edit') if auth.has_permission('view', 'VARIANT') else ''
             )
            ]

    
    for field in db.SAMPLE:
        field.readable = False
    for field in db.VARIANT:
        field.readable = False
    for field in db.SAMPLE_VARIANT:
        field.readable = False

    fields = [db.SAMPLE.sample
             ,db.SAMPLE.date_sample
             ,db.SAMPLE.fl_sample_type
             ,db.SAMPLE.fl_sex
             ,db.VARIANT.gene
             ,db.VARIANT.id_hg19
             ,db.VARIANT.note
             ,db.VARIANT.last_check
             ,db.VARIANT.classif
             ,db.SAMPLE_VARIANT.AF
             ,db.SAMPLE_VARIANT.GT
             ]

    for field in fields:
        field.readable = True

    #db.SAMPLE_VARIANT.SAMPLE_id.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
    #db.SAMPLE_VARIANT.VARIANT_id.requires  = IS_EMPTY_OR(IS_NOT_EMPTY(), null='')


    query = ((db.SAMPLE_VARIANT.SAMPLE_id == db.SAMPLE.id) & (db.VARIANT.id == db.SAMPLE_VARIANT.VARIANT_id))

    field_id = db.SAMPLE_VARIANT.id

    default_sort_order=[~db.SAMPLE.date_sample, db.SAMPLE.sample, db.VARIANT.gene, db.VARIANT.id_hg19]


    form = SQLFORM.grid(query=query
                       ,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,field_id = field_id
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=70
                        ,paginate=DEFAULT_PAGINATE #10
                        ,csv = True
                        ,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,user_signature=False
                        ,args=request.args[:1]
                       )


    return response.render(default_view, dict(form_head=form_head,form=form))

@auth.requires_permission('view', 'SAMPLE_VARIANT')
def variants_of_sample():
    sample_id = request.args(0) or None

    if sample_id == None:
        return response.render(default_subview, dict(form_head='',form=''))

    sample = db(db.SAMPLE.id==sample_id).select().first()
    if not sample:
        return response.render(default_subview, dict(form_head='',form=''))

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Variants of sample: ') + sample.sample

    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('', _title=T('Edit')
                                    ,_class='button btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                                    ,_href=URL('edit', args=[row.SAMPLE_VARIANT.id]
                                               ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                      ) if is_manage() else ''
            ,dict(header='',
                  body=lambda row: A(' ' , _title=T('Classif History')
                                    ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                                    ,_href=URL("variant","attribute_history"
                                              ,args=[variant_default_classif_id(variant_id_of(row.SAMPLE_VARIANT.id))]
                                              ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                     ) if num_variant_attribute(variant_id_of(row.SAMPLE_VARIANT.id),DEFAULT_CLASSIF) > 1 else ""
                  )
            ,dict(header=' ',
                  body=(lambda row: A('Variant', _title=T('Edit Variant')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","edit" ,args=[variant_id_of(row.SAMPLE_VARIANT.id)])
                                    ,_target='blank'
                                     ) if auth.has_permission('view', 'VARIANT') else ''
                        )
                   )
            ]


    for field in db.SAMPLE_VARIANT:
        field.readable = False
    for field in db.SAMPLE:
        field.readable = False
    for field in db.VARIANT:
        field.readable = False


    fields= (db.VARIANT.gene
            ,db.VARIANT.id_hg19
            ,db.VARIANT.classif
            ,db.SAMPLE_VARIANT.AF
            ,db.SAMPLE_VARIANT.GT
            )

    for field in fields:
        field.readable = True
    db.SAMPLE_VARIANT.SAMPLE_id.default = sample_id

    #per velocizzare l'output altrimenti troppo lento
    db.SAMPLE_VARIANT.SAMPLE_id.requires=IS_EMPTY_OR(IS_NOT_EMPTY(), null='')
    db.SAMPLE_VARIANT.VARIANT_id.requires=IS_EMPTY_OR(IS_NOT_EMPTY(), null='')

    query = ((db.SAMPLE_VARIANT.SAMPLE_id == sample_id) & (db.VARIANT.id == db.SAMPLE_VARIANT.VARIANT_id))

    field_id = db.SAMPLE_VARIANT.id

    default_sort_order=[db.VARIANT.id_hg19]


    form = SQLFORM.grid(query=query
                        ,fields=fields
                        ,field_id = field_id
                        #,headers=headers
                        ,links = links
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,searchable=True
                        ,paginate=DEFAULT_PAGINATE #20
                        ,exportclasses=default_exportclasses
                        ,csv = True
                        ,buttons_placement = 'left'
                        ,onvalidation=validation_SAMPLE_VARIANT
                        ,user_signature=False
                        ,formstyle="bootstrap4_inline"
                 #table3cols,table2cols,divs,ul,bootstrap,bootstrap3_stacked,bootstrap3_inline,bootstrap4_stacked,bootstrap4_inline,inline
                        ,args=request.args[:1]
                       )

    # Add new variant for sample
    add_record = A(' ' , _title=T('Add Variant')
                       ,_class='button btn btn-default btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                       ,_href=URL('insert',vars=dict(sample_id=sample_id
                                                    ,form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                       ,_name='btn_variant_of_sample_Add'
                       ,_id ='btn_variant_of_sample_Add'
                  )

    form[0].insert(-2,add_record) if is_manage() else ''


    if db(query).count() == 0:
        form.element('.web2py_table', replace=None)  # Delete "no records found" text


    form.element('.web2py_counter', replace=None) # toglie numero records trovati

    #paginazione = form.element('.web2py_paginator')
    #form.element('.web2py_paginator', _style="visibility: hidden")
    #addRecordPaginazione = TABLE(TR(TD(add_record, _width='3%'),TD(paginazione,_width='97%')))
    #form[0].insert(-1,addRecordPaginazione)

    return response.render(default_subview, dict(form_head=form_head,form=form))


@auth.requires_permission('view', 'SAMPLE_VARIANT')
def samples_of_variant():
    variant_id = request.args(0) or None

    if variant_id == None:
        return response.render(default_view, dict(form_head='',form=''))

    variant = db(db.VARIANT.id==variant_id).select().first()
    if not variant:
        return response.render(default_view, dict(form_head='',form=''))

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    response.title = T('Variants of sample: ') + variant.id_hg19

    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('', _title=T('Edit')
                            ,_class='button btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL('edit', args=[row.SAMPLE_VARIANT.id]
                                       ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                            ,_name='btn_sample_variant_edit') if is_manage() else ''
            ,dict(header=' ',
                   body=(lambda row: A('Sample', _title=T('Edit Sample')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("sample","edit" ,args=[sample_id_of(row.SAMPLE_VARIANT.id)])
                                    ,_target='blank'
                                    ,_name='btn_sample_edit') if auth.has_permission('view', 'SAMPLE') else ''
                        )
                  )
            ]

    for field in db.SAMPLE_VARIANT:
        field.readable = False
    for field in db.SAMPLE:
        field.readable = False
    for field in db.VARIANT:
        field.readable = False


    fields= (db.SAMPLE.sample
            ,db.SAMPLE.date_sample
            ,db.SAMPLE.fl_sample_type
            ,db.SAMPLE.TISSUE_TYPE_id
            ,db.SAMPLE.fl_sex
            ,db.SAMPLE_VARIANT.AF
            ,db.SAMPLE_VARIANT.GT
            )

    for field in fields:
        field.readable = True


    db.SAMPLE_VARIANT.VARIANT_id.default = variant_id

    #per velocizzare l'output altrimenti troppo lento
    db.SAMPLE_VARIANT.SAMPLE_id.requires=IS_NOT_EMPTY()
    db.SAMPLE_VARIANT.VARIANT_id.requires=IS_NOT_EMPTY()

    query = ((db.SAMPLE_VARIANT.VARIANT_id == variant_id) & (db.SAMPLE.id == db.SAMPLE_VARIANT.SAMPLE_id))

    default_sort_order=[~db.SAMPLE.date_sample,db.SAMPLE.sample]

    field_id = db.SAMPLE_VARIANT.id


    form = SQLFORM.grid(query=query
                        ,fields=fields
                        ,field_id = field_id
                        #,headers=headers
                        ,links = links
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,searchable=True
                        ,paginate=DEFAULT_PAGINATE #20
                        ,exportclasses=default_exportclasses
                        ,csv = True
                        ,buttons_placement = 'left'
                        ,onvalidation=validation_SAMPLE_VARIANT
                        ,user_signature=False
                        ,formstyle="bootstrap4_inline"
                 #table3cols,table2cols,divs,ul,bootstrap,bootstrap3_stacked,bootstrap3_inline,bootstrap4_stacked,bootstrap4_inline,inline
                        ,args=request.args[:1]
                       )

     # Add new sample for variant
    add_record = A(' ' , _title=T('Add Sample')
                       ,_class='button btn btn-default btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                       ,_href=URL('insert',vars=dict(variant_id=variant_id
                                                    ,form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                       ,_name='btn_sample_of_variant_Add'
                       ,_id ='btn_sample_of_variant_Add'
                  )

    form[0].insert(-2,add_record) if is_manage() else ''

    if db(query).count() == 0:
        form.element('.web2py_table', replace=None)  # Delete "no records found" text


    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    return response.render(default_view, dict(form_head=form_head,form=form))


@auth.requires_permission('manage', 'SAMPLE_VARIANT')
def edit():
    sample_variant_id = request.args(0) or None
    if not sample_variant_id:
        return response.render(default_subview, dict(form_head='',form=''))

    record = db.SAMPLE_VARIANT(db.SAMPLE_VARIANT.id==sample_variant_id)
    if not record:
        return response.render(default_subview, dict(form_head='',form=''))


    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Edit Variant - Sample')
    form_head=head_title(response.title,form_head_indietro)


    db.SAMPLE_VARIANT.id.writable = False
    db.SAMPLE_VARIANT.id.readable = False

    db.SAMPLE_VARIANT.SAMPLE_id.readable = True
    db.SAMPLE_VARIANT.SAMPLE_id.writable = False
    db.SAMPLE_VARIANT.SAMPLE_id.requires=IS_EMPTY_OR(IS_NOT_EMPTY(),null='')
    #db.SAMPLE_VARIANT.SAMPLE_id.widget = SQLFORM.widgets.autocomplete(request, db.SAMPLE.sample, id_field=db.SAMPLE.id,limitby=(1))
    db.SAMPLE_VARIANT.SAMPLE_id.represent = lambda value,row: string_widget(db.SAMPLE_VARIANT.SAMPLE_id,(db.SAMPLE._format % value) or '', _readonly='readonly')

    db.SAMPLE_VARIANT.VARIANT_id.readable = True
    db.SAMPLE_VARIANT.VARIANT_id.writable = False
    db.SAMPLE_VARIANT.VARIANT_id.requires=IS_EMPTY_OR(IS_NOT_EMPTY(),null='')
    #db.SAMPLE_VARIANT.VARIANT_id.widget = SQLFORM.widgets.autocomplete(request, db.VARIANT.id_hg19, id_field=db.VARIANT.id,limitby=(1))
    db.SAMPLE_VARIANT.VARIANT_id.represent = lambda value,row: string_widget(db.SAMPLE_VARIANT.VARIANT_id,(db.VARIANT._format % value) or '', _readonly='readonly')


    form=SQLFORM(db.SAMPLE_VARIANT
                ,record
                ,readonly=False
                ,deletable=True
                ,formstyle="bootstrap4_inline"
                 #table3cols,table2cols,divs,ul,bootstrap,bootstrap3_stacked,bootstrap3_inline,bootstrap4_stacked,bootstrap4_inline,inline
                ,args=request.args[:1]
                )

    if form.process(onvalidation=validation_SAMPLE_VARIANT).accepted:
        if form.deleted:
            session.flash = T('delete done')
            redirect(form_head_indietro)
        else:
            if record:
                response.flash = T('modify done')
                redirect(URL(args=request.args, vars=request.get_vars, host=True)) #reload this page

    """ tolgo visualizzazione attributi del sample_variant
    iframe_attribute = IFRAME(T('Attribute')
                              ,_title=T('Attribute')
                              ,_src=URL('sample_variant','attribute_list',args=[record.id])
                              ,_style="padding-left:0px; height:100%; width:100%"
                              ,_frameborder='0',_scrolling='yes'
                              ,_onload='resize_iframe(this)'
                              ,_id='iframe_sample_variant_attribute'
                           ) if record else ''
    """
    iframe_attribute =''

    return dict(form=form, iframe_attribute=iframe_attribute,form_head=form_head)


@auth.requires_permission('manage', 'SAMPLE_VARIANT')
def insert():
    sample_id = (request.vars['sample_id']) if (request.vars['sample_id']) else None
    variant_id = (request.vars['variant_id']) if (request.vars['variant_id']) else None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    if not sample_id and not variant_id:
        redirect(form_head_indietro)

    response.title = T('Insert Variant - Sample')
    if sample_id:
        sample = db(db.SAMPLE.id==sample_id).select().first()
        if not sample:
            redirect(form_head_indietro)
        response.title = T('Insert Variant of Sample:'+ sample.sample)
    if variant_id:
        variant = db(db.VARIANT.id==variant_id).select().first()
        if not variant:
            redirect(form_head_indietro)
        response.title = T('Insert Sample of Variant:'+ variant.id_hg19)

    form_head=head_title(response.title,form_head_indietro)

    if sample_id:
        db.SAMPLE_VARIANT.SAMPLE_id.default = sample_id
        db.SAMPLE_VARIANT.SAMPLE_id.readable = False
    else:
        db.SAMPLE_VARIANT.SAMPLE_id.readable = True
        db.SAMPLE_VARIANT.SAMPLE_id.writable = True
        db.SAMPLE_VARIANT.SAMPLE_id.requires=IS_IN_DB(db, 'SAMPLE.id', '%(sample)s')
        db.SAMPLE_VARIANT.SAMPLE_id.widget = SQLFORM.widgets.autocomplete(request, db.SAMPLE.sample, id_field=db.SAMPLE.id
                                                                        , at_beginning=False, limitby=(0, 10))

    if variant_id :
        db.SAMPLE_VARIANT.VARIANT_id.default = variant_id
        db.SAMPLE_VARIANT.VARIANT_id.readable = False
    else:
        db.SAMPLE_VARIANT.VARIANT_id.readable = True
        db.SAMPLE_VARIANT.VARIANT_id.writable = True
        db.SAMPLE_VARIANT.VARIANT_id.requires=IS_IN_DB(db, 'VARIANT.id', '%(id_hg19)s')
        db.SAMPLE_VARIANT.VARIANT_id.widget = SQLFORM.widgets.autocomplete(request, db.VARIANT.id_hg19, id_field=db.VARIANT.id
                                                                               , at_beginning=False, limitby=(0, 10))


    form=SQLFORM(db.SAMPLE_VARIANT
                ,None
                ,readonly=False
                ,deletable=False
                ,formstyle="bootstrap4_inline"
                 #table3cols,table2cols,divs,ul,bootstrap,bootstrap3_stacked,bootstrap3_inline,bootstrap4_stacked,bootstrap4_inline,inline
                ,args=request.args[:1]
                )


    if form.process(onvalidation=validation_SAMPLE_VARIANT).accepted:
        session.flash = T('insert done')
        redirect(URL('edit',args=[form.vars.id],vars=dict(form_head_indietro=form_head_indietro)))

    return response.render("sample_variant/edit.html", dict(form=form, iframe_attribute='',form_head=form_head))


#####################################
####   SAMPLE VARIANT ATTRIBUTE  ####
#####################################
""" disattivato

@auth.requires_permission('view', 'SAMPLE_VARIANT')
def attribute_list():
    sample_variant_id = request.args(0) or None

    form_head = ''

    if sample_variant_id == None:
        return response.render(default_subview, dict(form_head='',form=''))
    else:
        form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else ''
        sample_variant = db(db.SAMPLE_VARIANT.id==sample_variant_id).select().first()
        if sample_variant:
            sample = db(db.SAMPLE.id==sample_variant.SAMPLE_id).select().first()
            variant = db(db.VARIANT.id==sample_variant.VARIANT_id).select().first()
            response.title = T('Attribute of : ')+ sample.sample + ' ' + variant.id_hg19
            if not form_head_indietro :
                form_head=head_title(response.title)
            elif form_head_indietro == "list":
                form_head_indietro2 = (request.vars['form_head_indietro2']) if (request.vars['form_head_indietro2']) else ''
                form_head=head_title(response.title,URL('sample_variant',form_head_indietro,args=sample_variant.SAMPLE_id, vars=dict(form_head_indietro=form_head_indietro2)))
            else:
                form_head=head_title(response.title,URL('sample_variant',form_head_indietro, vars=dict(form_head_indietro=form_head_indietro2)))


    db.SAMPLE_VARIANT_ATTRIBUTE.id.writable = False
    db.SAMPLE_VARIANT_ATTRIBUTE.id.readable = False

    db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.default = sample_variant_id
    db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.writable = False
    db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.readable = False

    query=(db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id == sample_variant_id)

    fields= (db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id
            ,db.SAMPLE_VARIANT_ATTRIBUTE.attribute_name
            ,db.SAMPLE_VARIANT_ATTRIBUTE.attribute_value
            )
    links = [(lambda row: A('', _title=T('Detail')
                            ,_class='button btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL("sample_variant","attribute_edit",args=[row.id])
                            ,_name='btn_sample_variant_attribute_Edit') if is_manage() else '')
            ]

    default_sort_order=[db.SAMPLE_VARIANT_ATTRIBUTE.attribute_name]

    form = SQLFORM.grid(query=query
                        ,fields=fields
                        #,headers=headers
                        ,links = links
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable=is_manage()
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,searchable=False
                        ,paginate=DEFAULT_PAGINATE #9
                        ,csv = False
                        ,buttons_placement = 'left'
                        ,onvalidation=validation_SAMPLE_VARIANT_ATTRIBUTE
                        ,user_signature=False
                        #,formstyle="bootstrap4_inline"
                 #table3cols,table2cols,divs,ul,bootstrap,bootstrap3_stacked,bootstrap3_inline,bootstrap4_stacked,bootstrap4_inline,inline
                        ,args=request.args[:1]
                       )

    if db(query).count() == 0:
        form.element('.web2py_table', replace=None)  # Delete "no records found" text


    # Add new record con form personalizzata
    add_record = A(' ' , _title=T('Add Attribute')
                       ,_class='button btn btn-default btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                       ,_href=URL("sample_variant","attribute_insert",args=[sample_variant_id])
                       ,_name='btn_sample_variant_attribute_Add'
                       ,_id ='btn_sample_variant_attribute_Add'
                  )

    form[0].insert(-1,add_record) if is_manage() else ''

    form.element('.web2py_counter', replace=None) # toglie numero records trovati

    #paginazione = form.element('.web2py_paginator')
    #form.element('.web2py_paginator', _style="visibility: hidden")
    #addRecordPaginazione = TABLE(TR(TD(add_record, _width='3%'),TD(paginazione,_width='97%')))
    #form[0].insert(-1,addRecordPaginazione)

    return response.render(default_subview, dict(form_head=form_head,form=form))


def attribute_form(record,sample_variant_id):

    form_head = FORM(DIV(A(' ' , _title=T('Back')
                               ,_class='button btn btn-default btn-secondary btn-sm icon arrowleft icon-arrowleft glyphicon glyphicon-arrow-left'
                               ,_href=URL('sample_variant','attribute_list',args=[sample_variant_id])
                          )
                        ))

    db.SAMPLE_VARIANT_ATTRIBUTE.id.writable = False
    db.SAMPLE_VARIANT_ATTRIBUTE.id.readable = False

    db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.default = sample_variant_id
    db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.writable = False
    db.SAMPLE_VARIANT_ATTRIBUTE.SAMPLE_VARIANT_id.readable = False

    form=SQLFORM(db.SAMPLE_VARIANT_ATTRIBUTE
                ,record
                ,readonly=False
                ,deletable=False #si può cancellare solo dalla lista
                ,formstyle="bootstrap4_inline"
                 #table3cols,table2cols,divs,ul,bootstrap,bootstrap3_stacked,bootstrap3_inline,bootstrap4_stacked,bootstrap4_inline,inline
                ,args=request.args[:1]
                ,formname = "sample_variant_attribute_form"
                )

    #form.custom.widget['HP_id'][0].add_class('form-control')

    if form.process(onvalidation=validation_SAMPLE_VARIANT_ATTRIBUTE).accepted:
        if form.deleted:
            session.flash = T('delete done')
            redirect(URL('sample_variant','attribute_list',args=[sample_variant_id] , vars=dict(form_head_indietro='list')))
        else:
            if record:
                response.flash = T('modify done')
                redirect(URL('sample_variant','attribute_list',args=[sample_variant_id] , vars=dict(form_head_indietro='list')))
            else: # sono in inserimento
                redirect(URL('sample_variant','attribute_list',args=[sample_variant_id] , vars=dict(form_head_indietro='list')))

    return dict(form_head=form_head,form=form)

@auth.requires_permission('manage', 'SAMPLE_VARIANT')
def attribute_edit():
    sample_variant_attribute_id = request.args(0) or None
    if sample_variant_attribute_id=='None':
        return response.render(default_subview, dict(form_head='',form=''))

    record = db.SAMPLE_VARIANT_ATTRIBUTE(db.SAMPLE_VARIANT_ATTRIBUTE.id==sample_variant_attribute_id) or None

    dict_forms = attribute_form(record,record.SAMPLE_VARIANT_id)

    return response.render(default_subview, dict_forms)


@auth.requires_permission('manage', 'SAMPLE_VARIANT')
def attribute_insert():
    sample_variant_attribute_id = request.args(0) or None
    record = None

    if sample_variant_attribute_id is None:
        dict_forms = dict(form_head='',form='')
    else:
        dict_forms = attribute_form(record,sample_variant_attribute_id)

    return response.render(default_subview, dict_forms)

"""
