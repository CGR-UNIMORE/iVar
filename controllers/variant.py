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

##################
####   LIST   ####
##################

@auth.requires_permission('view', 'VARIANT')
def list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Variants')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('', _title=T('Edit')
                             ,_class='btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                             ,_href=URL("variant","edit",args=[row.id]
                                        ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           )
            ,lambda row: A(str(num_samples_of_variant(row.id))
                                     ,_title = T('Samples')
                                     ,_class='btn btn-success btn-sm'
                                     ,_href=URL('sample_variant','samples_of_variant',args=[row.id])
                                     ,_target='blank'
                                     ) if num_samples_of_variant(row.id)>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                                     else SPAN(str(num_samples_of_variant(row.id)),_class='btn btn-success btn-sm')\
                                       if num_samples_of_variant(row.id)>0 else ''
            ,dict(header='',
                  body=lambda row: A(' ' , _title=T('Classif History')
                                    ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                                    ,_href=URL("variant","attribute_history",args=[variant_default_classif_id(row.id)]
                                              ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                     ) if num_variant_attribute(row.id,DEFAULT_CLASSIF) > 1 else ''
                  )
            ,dict(header='',
                  body=lambda row: A('',_title="#Attr." + str(num_attributes_of_variant(row.id))
                                     ,_class='btn btn-success btn-sm icon list icon-list glyphicon glyphicon-th-list'
                                     ,_href=URL('variant','attribute_list',args=[row.id]
                                                ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                     ) if num_attributes_of_variant(row.id)>0 else ''
                   )
            ,dict(header='',
                  body=lambda row: A('ClinVar',_title=ClinVar(row.id)['attribute']
                             ,_class='btn btn-default btn-secondary btn-sm'
                             ,_href=ClinVar(row.id)['url']
                             ,_target='blank'
                           ) if ClinVar(row.id)['url']!='' else ''
                 )
            ]


    for field in db.VARIANT:
        field.readable = False

    fields= (db.VARIANT.gene
            ,db.VARIANT.id_hg19
            ,db.VARIANT.id_hg38
            ,db.VARIANT.last_check
            ,db.VARIANT.classif
            )

    for field in fields:
        field.readable = True

    #too slow db.VARIANT.gene.requires=IS_IN_SET(set_of_values(db.VARIANT.gene),zero=None,error_message=T('mandatory'))

    query= (db.VARIANT)
    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19, db.VARIANT.id_hg38]


    form = SQLFORM.grid(query=query
                        ,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=auth.has_permission('manage', 'VARIANT')
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #10
                        ,csv = True
                        ,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_VARIANT
                        ,oncreate=oncreate_VARIANT
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati
    return response.render(default_view, dict(form_head=form_head,form=form))



def oncreate_VARIANT(form):
    if 'new' in request.args:
        session.flash = T('insert done') 
        redirect(URL('edit',args=[form.vars.id],vars=dict(form_head_indietro='list')))
    return True


@auth.requires_permission('view', 'VARIANT')
def edit():
    variant_id = request.args(0) or None

    response.title = T('Edit Variant')

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    form_head=head_title(response.title,form_head_indietro)

    if not variant_id:
        return dict(form_head='',form='',iframe_attribute='',btn_samples_of_variant='')

    record = db.VARIANT(db.VARIANT.id==variant_id) or None

    #hg non modificabili se già valorizzati

    if record.id_hg19 in (None, ''):
        record.id_hg19 = ""
        db.VARIANT.id_hg19.writable  = True
    else:
        db.VARIANT.id_hg19.writable  = False
        db.VARIANT.id_hg19.represent = lambda value,row: string_widget(db.VARIANT.id_hg19,value, _readonly='readonly')

    if record.id_hg38 in (None, ''):
        record.id_hg38 =""
        db.VARIANT.id_hg38.writable  = True
    else:
        db.VARIANT.id_hg38.writable  = False
        db.VARIANT.id_hg38.represent = lambda value,row: string_widget(db.VARIANT.id_hg38,value, _readonly='readonly')


    def is_readonly(): return ((auth.has_permission('view', 'VARIANT')) and (not (auth.has_permission('manage', 'VARIANT'))))
    def is_deletable(): return   (auth.has_permission('delete', 'VARIANT'))

    form=SQLFORM(db.VARIANT
                ,record
                ,readonly=is_readonly()
                ,deletable=is_deletable()
                ,showid=False
                )

    if form.process(onvalidation=validation_VARIANT).accepted:
        if form.deleted:
            session.flash = T('Variant deleted')
            redirect(form_head_indietro)
        else:
            if record:
                update_VARIANT_ATTRIBUTE_classif(record.id,form.vars.classif, None, True)
                session.flash = T('Variant modified')
                redirect(URL(args=request.args, vars=request.get_vars, host=True))
                #redirect(URL('variant','edit',args=[record.id], vars=dict(form_head_indietro=form_head_indietro)))
            #else:
                # in inserimento di qui non passo mai, perchè questa funzione viene chiamata in editing

    btn_samples_of_variant = A(str(num_samples_of_variant(record.id)),_title=T('Samples')
                                ,_class='btn btn-default btn-secondary btn-sm'
                                ,_href=URL('sample_variant','samples_of_variant',args=[record.id])
                                ,_target='blank'
                               ) if record and auth.has_permission('view', 'SAMPLE_VARIANT')\
                               else SPAN(str(num_samples_of_variant(record.id))
                                         ,_class='btn btn-default btn-secondary btn-sm') if record else ''

    btn_clinvar = A('ClinVar',_title=ClinVar(record.id)['attribute']
                    ,_class='btn btn-default btn-secondary btn-sm' 
                    ,_href=ClinVar(record.id)['url']
                    ,_target='blank'
                    ) if record else ''

    iframe_attribute = IFRAME(T('Attributes')
                                ,_title=T('Attributes')
                                ,_src=URL('variant','attribute_list',args=[record.id])
                                ,_style="padding-left:0px; height:100%; width:100%"
                                ,_frameborder='0',_scrolling='yes'
                                ,_onload='resize_iframe(this)'
                                ,_id='iframe_variant_attribute'
                               ) if record else ''

    #return response.render(default_view, dict(form_head=form_head,form=form))
    return dict(form_head=form_head,form=form,iframe_attribute=iframe_attribute
                ,btn_samples_of_variant=btn_samples_of_variant,btn_clinvar=btn_clinvar)


###############################
####   VARIANT ATTRIBUTE   ####
###############################

@auth.requires_permission('view', 'VARIANT')
def attribute_list():
    variant_id = request.args(0) or None
    if variant_id == None:
        return response.render(default_subview, dict(form_head='',form=''))

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not form_head_indietro:
        form_head = ''
    else:
        variant = db(db.VARIANT.id==variant_id).select().first()
        response.title = T('Attributes of Variant: ')+ variant.id_hg19 + ' ' + variant.id_hg38
        form_head=head_title(response.title,form_head_indietro)


    def is_manage()     :return (auth.has_permission('manage', 'VARIANT'))

    links = [lambda row: A('', _title=T('Detail')
                            ,_class='button btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL("variant","attribute_edit",args=[row.id]
                                       ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                            ) if is_manage() else ''
            ,lambda row: A(' ' , _title=T('History values')
                    ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                    ,_href=URL("variant","attribute_history",args=[row.id]
                              ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           ##,vars=dict(variant_id=variant_id,form_head_indietro='attribute_list',id_indietro=variant_id))
              ) if num_variant_attribute(variant_id_of_attribute(row.id),row.attribute_name) > 1 else ''
            ]


    for field in db.VARIANT_ATTRIBUTE_CURRENT:
        field.readable = False

    db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id.default = variant_id
    db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id.writable = False

    fields= (db.VARIANT_ATTRIBUTE_CURRENT.attribute_name
            ,db.VARIANT_ATTRIBUTE_CURRENT.valid_from
            ,db.VARIANT_ATTRIBUTE_CURRENT.attribute_value
            )

    for field in fields:
        field.readable = True


    query=(db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id == variant_id)

    default_sort_order=[db.VARIANT_ATTRIBUTE_CURRENT.attribute_name, ~db.VARIANT_ATTRIBUTE_CURRENT.valid_from]


    form = SQLFORM.grid(query=query
                        ,fields=fields
                        #,headers=headers
                        ,links = links
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=500
                        ,searchable=False
                        ,paginate=DEFAULT_PAGINATE #50
                        ,csv = True
                        ,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,onvalidation=validation_VARIANT_ATTRIBUTE
                        ,user_signature=False
                        #,formstyle="bootstrap3_stacked"#"bootstrap3_stacked","bootstrap2", "table3cols", "table2cols" 
                        ,args=request.args[:1]
                       )

    if db(query).count() == 0:
        form.element('.web2py_table', replace=None)  # Delete "no records found" text


    # Add new record con form personalizzata
    add_record = A(' ' ,_title=T('Add attribute')
                       ,_class='button btn btn-default btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                       ,_href=URL("variant","attribute_insert",args=[variant_id]
                                 ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                  )

    form[0].insert(-1,add_record) if is_manage() else ''

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    return response.render(default_subview, dict(form_head=form_head,form=form))


def attribute_form(record,variant_id,form_head_indietro=None):

    if form_head_indietro:
        form_head = FORM(DIV(A(' ' , _title=T('back') 
                                   , _class='button btn btn-default btn-secondary btn-sm icon arrowleft icon-arrowleft glyphicon glyphicon-arrow-left'
                                   , _href=form_head_indietro
                              )))
    else:
        response.title = T('Attribute')
        form_head=head_title(response.title)

    db.VARIANT_ATTRIBUTE.id.writable = False
    db.VARIANT_ATTRIBUTE.id.readable = False

    db.VARIANT_ATTRIBUTE.VARIANT_id.default = variant_id
    db.VARIANT_ATTRIBUTE.VARIANT_id.writable = False
    db.VARIANT_ATTRIBUTE.VARIANT_id.readable = False

    form=SQLFORM(db.VARIANT_ATTRIBUTE
                ,record
                ,readonly=False
                ,deletable=True
                ,formstyle="bootstrap4_stacked"#"bootstrap3_inline","bootstrap2", "table3cols", "table2cols"  bootstrap3_stacked
                ,args=request.args[:1]
                )

    if form.process(onvalidation=validation_VARIANT_ATTRIBUTE).accepted:
        session.flash=''
        if form.deleted:
            session.flash = T('Attribute deleted')
        else:
            if record:
                session.flash = T('Attribute modified')
            else: 
                session.flash = T('Attribute inserted')
        if update_VARIANT_classif(variant_id):
            session.flash = T('Classif modified: reload to view the classif of this variant')
            #redirect(URL(form_head_indietro)) ##'variant','attribute_list',args=[variant_id]))

        redirect(form_head_indietro)
        #URL('attribute_list',args=[variant_id],vars=dict(form_head_indietro=form_head_indietro)))

    return dict(form_head=form_head,form=form)


@auth.requires_permission('manage', 'VARIANT')
def attribute_edit():
    variant_attribute_id = request.args(0) or None
    if not variant_attribute_id:
        return response.render(default_subview, dict(form_head='',form=''))

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    record = db.VARIANT_ATTRIBUTE(db.VARIANT_ATTRIBUTE.id==variant_attribute_id) or None

    dict_forms = attribute_form(record,record.VARIANT_id,form_head_indietro)

    # History View con form personalizzata
    history = A(' ' , _title=T('History values')
                    ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                    ,_href=URL("variant","attribute_history",args=[record.id]
                               ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
               )

    if num_variant_attribute(record.VARIANT_id,record.attribute_name) > 1:
        dict_forms['form'][0].insert(-2,history)  

    if not form_head_indietro:
        return response.render(default_view, dict_forms)
    else:
        return response.render(default_subview, dict_forms)

@auth.requires_permission('manage', 'VARIANT')
def attribute_insert():
    variant_id = request.args(0) or None
    record = None

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    if not variant_id:
        dict_forms = dict(form_head='',form='')
    else:
        dict_forms = attribute_form(record,variant_id,form_head_indietro)

    return response.render(default_subview, dict_forms)


@auth.requires_permission('view', 'VARIANT')
def attribute_history():
    record_id = request.args(0) or None
    if record_id is None:
        redirect(URL('iVar'))

    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    variant_id = (request.vars['variant_id']) if (request.vars['variant_id']) else None
    attribute_name = (request.vars['attribute_name']) if (request.vars['attribute_name']) else None

    if not variant_id and not attribute_name:
        variant_attribute = db(db.VARIANT_ATTRIBUTE.id==record_id).select().first()
        if variant_attribute is None:
            redirect(form_head_indietro)
        attribute_name = variant_attribute.attribute_name
        variant_id = variant_attribute.VARIANT_id


    variant = db(db.VARIANT.id==variant_id).select().first()
    response.title = T('Variant''s history:')
    if variant.id_hg19:
        response.title = response.title +' '+ variant.id_hg19 
    if variant.id_hg38:
        response.title = response.title +' '+ variant.id_hg38
    if attribute_name:
        response.title = response.title +' - '+T('Attribute')+': '+ attribute_name

    form_head=head_title(response.title,form_head_indietro)

    def is_manage()     :return (auth.has_permission('manage', 'VARIANT'))

    links = [(lambda row: A('', _title=T('Detail')
                            ,_class='button btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL("variant","attribute_edit",args=[row.id]
                                       ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           ) if is_manage() else '')
             ]

    for field in db.VARIANT_ATTRIBUTE:
        field.readable = False

    fields= (db.VARIANT_ATTRIBUTE.valid_from
            ,db.VARIANT_ATTRIBUTE.attribute_value
            )

    for field in fields:
        field.readable = True

    db.VARIANT_ATTRIBUTE.VARIANT_id.default = variant_id
    db.VARIANT_ATTRIBUTE.attribute_name.default = attribute_name

    query=(db.VARIANT_ATTRIBUTE.attribute_name == attribute_name) & (db.VARIANT_ATTRIBUTE.VARIANT_id == variant_id)

    field_id = db.VARIANT_ATTRIBUTE.id

    default_sort_order=[~db.VARIANT_ATTRIBUTE.valid_from]

    form = SQLFORM.grid(query=query
                        ,fields=fields
                        #,headers=headers
                        ,links = links
                        ,orderby=default_sort_order
                        ,field_id = field_id
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=500
                        ,searchable=False
                        ,paginate=DEFAULT_PAGINATE #10
                        ,csv = True
                        ,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,onvalidation=validation_VARIANT_ATTRIBUTE
                        ,user_signature=False
                        ,formstyle="bootstrap4_stacked"#"bootstrap3_stacked","bootstrap2", "table3cols", "table2cols" 
                        ,args=request.args[:1] or None
                       )

    if db(query).count() == 0:
        form.element('.web2py_table', replace=None)  # Delete "no records found" text

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    return response.render(default_subview, dict(form_head=form_head,form=form))



@auth.requires_permission('delete', 'VARIANT')
def delete_attribute():

    response.title = T('Delete Variants attribute')
    form_head=head_title(response.title)

    def variant_id_attribute(attribute_id):
        row = db(db.VARIANT_ATTRIBUTE.id == attribute_id).select().first() or None
        if row:
            return row.VARIANT_id
        else:
            return None

    links = [dict(header=''
                 ,body=lambda row: A('Variant', _title=T('Variant')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","edit" ,args=[variant_id_attribute(row.id)]
                                               ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                    ,_target="blank") 
                  )
            ]

    db.VARIANT_ATTRIBUTE.id.writable = False
    db.VARIANT_ATTRIBUTE.id.readable = False
    db.VARIANT_ATTRIBUTE.VARIANT_id.writable = False
    db.VARIANT_ATTRIBUTE.VARIANT_id.readable = False

    query= (db.VARIANT_ATTRIBUTE)

    default_sort_order=[db.VARIANT_ATTRIBUTE.attribute_name, ~db.VARIANT_ATTRIBUTE.valid_from]


    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid = True
                        ,orderby=default_sort_order
                        ,searchable=True
                        ,create=False
                        ,deletable=False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=110
                        ,paginate=(DEFAULT_PAGINATE*50) #500
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,user_signature=False
                        ,selectable= lambda ids : [sql_delete_attribute(ids)
                                                  ,redirect(URL('variant','delete_attribute',vars=request._get_vars))
                                                  ]
                        ,selectable_submit_button=T('Delete')
                       )

    heading = form.elements('th') #cerco l'intestazione della tabella
    if heading:
        heading[0].append(INPUT(_type='checkbox'
        ,_name = 'records_select'
        ,_onclick="jQuery('input[name=records]').each(function(){jQuery(this).prop('checked',!jQuery(this).prop('checked'));});"
                               )
                         )

    return response.render(default_view, dict(form_head=form_head,form=form))

def sql_delete_attribute(ids): 
    for row in db(db.VARIANT_ATTRIBUTE.id.belongs(ids)).select():
        row.delete_record()
        db.commit()
    session.flash = T('Attributes deleted')
