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

@auth.requires_permission('view', 'VARIANT')
def special_attribute():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Variants and special attributes')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('Variant', _title=T('Edit Variant')
                            ,_class='btn btn-default btn-secondary btn-link btn-sm'
                            ,_href=URL("variant","edit",args=[row[field_id]]
                                       ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           )
             ,lambda row: A(str(num_samples_of_variant(row[field_id]))
                            ,_title=T('Samples')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','samples_of_variant',args=[row[field_id]])
                            ,_target='blank'
                           ) if num_samples_of_variant(row[field_id])>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                                         else SPAN(str(num_samples_of_variant(row[field_id])),_class='btn btn-success btn-sm')\
                                         if num_samples_of_variant(row[field_id])>0 else ''
             ,dict(header='',
                  body=lambda row: A(' ' , _title=T('Classif History')
                                    ,_class='btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                                    ,_href=URL('variant','attribute_history',args=[0]
                                               ,vars=dict(variant_id=row[field_id]
                                                        ,attribute_name = row.VARIANT_ATTRIBUTE.attribute_name))
                                    ,_target='blank'
                                     ) if num_variant_attribute(row[field_id],row.VARIANT_ATTRIBUTE.attribute_name) > 1 else ""
                  )
           ,dict(header='',
                  body=lambda row: A('Attribute', _title=T('Edit Attribute')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","attribute_edit",args=[row.VARIANT_ATTRIBUTE.id])
                                    ,_target='blank'
                                    ) if row.VARIANT_ATTRIBUTE.id else ""
                   )
           ,dict(header='',
                  body=lambda row: A('ClinVar', _title=T('Link to ClinVar')
                                     ,_class='btn btn-default btn-secondary btn-sm' 
                                     ,_href=ClinVar_attribute(row.VARIANT_ATTRIBUTE.attribute_name, row.VARIANT_ATTRIBUTE.id)
                                     ,_target='blank'
                                    ) if ClinVar_attribute(row.VARIANT_ATTRIBUTE.attribute_name, row.VARIANT_ATTRIBUTE.id)!='' else ''
                 )
             ]


    for field in db.VARIANT:
        field.readable = False
    for field in db.VARIANT_ATTRIBUTE:
        field.readable = False

    fields = [db.VARIANT.gene
             ,db.VARIANT.id_hg19
             ,db.VARIANT.classif
             ,db.VARIANT_ATTRIBUTE.attribute_name
             ,db.VARIANT_ATTRIBUTE.valid_from
             ,db.VARIANT_ATTRIBUTE.attribute_value
             ,db.VARIANT_ATTRIBUTE.id
             ]

    for field in fields:
        field.readable = True

    db.VARIANT_ATTRIBUTE.id.readable = False

    db.VARIANT_ATTRIBUTE.attribute_name.requires=IS_IN_SET(SPECIAL_ATTRIBUTES)

    #query =(db.VARIANT)
    #left = db.VARIANT_ATTRIBUTE.on((db.VARIANT_ATTRIBUTE.VARIANT_id == db.VARIANT.id)\
    #                             & (db.VARIANT_ATTRIBUTE.attribute_name.belongs(SPECIAL_ATTRIBUTES)))
    query = ((db.VARIANT.id== db.VARIANT_ATTRIBUTE.VARIANT_id) & (db.VARIANT_ATTRIBUTE.attribute_name.belongs(SPECIAL_ATTRIBUTES)))
    left=None
    field_id = db.VARIANT.id

    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19
                       #,db.VARIANT_ATTRIBUTE.attribute_name,db.VARIANT_ATTRIBUTE.valid_from 
                       ]

    form = SQLFORM.grid(query=query
                       ,fields=fields
                       #,headers=headers
                        ,left = left
                        ,links = links
                        ,links_in_grid = True
                        ,field_id = field_id
                        ,orderby=default_sort_order
                        ,create=False
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
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    form.element('.web2py_counter', replace=None) # toglie numero records trovati
    return response.render(default_view, dict(form_head=form_head,form=form))

@auth.requires_permission('view', 'VARIANT')
def attribute_current():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Variants and current attribute')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('Variant', _title=T('Edit Variant')
                              ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                              ,_href=URL("variant","edit",args=[row[field_id]])
                              ,_target="blank"
                          )
            ,lambda row: A(str(num_samples_of_variant(row[field_id]))
                            ,_title=T('Samples')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','samples_of_variant',args=[row[field_id]])
                            ,_target='blank'
                           ) if num_samples_of_variant(row[field_id])>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                             else SPAN(str(num_samples_of_variant(row[field_id])),_class='btn btn-success btn-sm')\
                               if num_samples_of_variant(row[field_id])>0 else ''
            ,dict(header='',
                  body=lambda row: A(' ' , _title=T('History')
                                    ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                                    ,_href=URL('variant','attribute_history',args=[0]
                                               ,vars=dict(variant_id=row[field_id]
                                                        ,attribute_name = row.VARIANT_ATTRIBUTE_CURRENT.attribute_name))
                                    ,_target='blank'
                                     ) if num_variant_attribute(row[field_id],row.VARIANT_ATTRIBUTE_CURRENT.attribute_name) > 1 else ""
                  )
            ,dict(header='',
                  body=lambda row: A('Attribute', _title=T('Edit Attribute')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","attribute_edit",args=[row.VARIANT_ATTRIBUTE_CURRENT.id])
                                    ,_target='blank'
                                    ) if row.VARIANT_ATTRIBUTE_CURRENT.id else ""
                   )
            ]

    for field in db.VARIANT:
        field.readable = False
    for field in db.VARIANT_ATTRIBUTE_CURRENT:
        field.readable = False

    fields = [db.VARIANT.gene
             ,db.VARIANT.id_hg19
             ,db.VARIANT.note
             ,db.VARIANT.last_check
             ,db.VARIANT.classif
             ,db.VARIANT_ATTRIBUTE_CURRENT.attribute_name
             ,db.VARIANT_ATTRIBUTE_CURRENT.attribute_value
             ,db.VARIANT_ATTRIBUTE_CURRENT.valid_from
             ,db.VARIANT_ATTRIBUTE_CURRENT.id
             ]

    for field in fields:
        field.readable = True
    db.VARIANT_ATTRIBUTE_CURRENT.id.readable= False

    query= (db.VARIANT.id>0)
    left = db.VARIANT_ATTRIBUTE_CURRENT.on(db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id == db.VARIANT.id)

    field_id = db.VARIANT.id

    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19]#, db.VARIANT_ATTRIBUTE_CURRENT.attribute_name]

    form = SQLFORM.grid(query=query
                       ,fields=fields
                        #,headers=headers
                        ,left = left
                        ,links = links
                        ,links_in_grid = True
                        ,field_id = field_id
                        ,orderby=default_sort_order
                        ,create=False
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
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    return response.render(default_view, dict(form_head=form_head,form=form))

@auth.requires_permission('view', 'VARIANT')
def attribute():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Variants and  all attribute')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('Variant', _title=T('Edit Variant')
                              ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                              ,_href=URL("variant","edit",args=[row[field_id]])
                              ,_target="blank"
                          )
            ,lambda row: A(str(num_samples_of_variant(row[field_id]))
                            ,_title=T('Samples')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','samples_of_variant',args=[row[field_id]])
                            ,_target='blank'
                           ) if num_samples_of_variant(row[field_id])>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                             else SPAN(str(num_samples_of_variant(row[field_id])),_class='btn btn-success btn-sm')\
                               if num_samples_of_variant(row[field_id])>0 else ''
            ,dict(header='',
                  body=lambda row: A(' ' , _title=T('History')
                                    ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                                    ,_href=URL('variant','attribute_history',args=[0]
                                               ,vars=dict(variant_id=row[field_id]
                                                        ,attribute_name = row.VARIANT_ATTRIBUTE.attribute_name))
                                    ,_target='blank'
                                     ) if num_variant_attribute(row[field_id],row.VARIANT_ATTRIBUTE.attribute_name) > 1 else ""
                  )
            ,dict(header='',
                  body=lambda row: A('Attribute', _title=T('Edit Attribute')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","attribute_edit",args=[row.VARIANT_ATTRIBUTE.id])
                                    ,_target='blank'
                                    ) if row.VARIANT_ATTRIBUTE.id else ""
                   )
            ]

    for field in db.VARIANT:
        field.readable = False
    for field in db.VARIANT_ATTRIBUTE:
        field.readable = False

    fields = [db.VARIANT.gene
             ,db.VARIANT.id_hg19
             ,db.VARIANT.note
             ,db.VARIANT.last_check
             ,db.VARIANT.classif
             ,db.VARIANT_ATTRIBUTE.attribute_name
             ,db.VARIANT_ATTRIBUTE.attribute_value
             ,db.VARIANT_ATTRIBUTE.valid_from
             ,db.VARIANT_ATTRIBUTE.id
             ]

    for field in fields:
        field.readable = True
    db.VARIANT_ATTRIBUTE.id.readable= False

    query= (db.VARIANT.id>0)
    left = db.VARIANT_ATTRIBUTE.on(db.VARIANT_ATTRIBUTE.VARIANT_id == db.VARIANT.id)

    field_id = db.VARIANT.id

    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19, db.VARIANT_ATTRIBUTE.attribute_name, ~db.VARIANT_ATTRIBUTE.valid_from]


    form = SQLFORM.grid(query=query
                       ,fields=fields
                        #,headers=headers
                        ,left = left
                        ,links = links
                        ,links_in_grid = True
                        ,field_id = field_id
                        ,orderby=default_sort_order
                        ,create=False
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
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    return response.render(default_view, dict(form_head=form_head,form=form))

def List_samples_of_variant(variant_id):
    s =[]
    rows = db((db.SAMPLE_VARIANT.SAMPLE_id == db.SAMPLE.id) & (db.SAMPLE_VARIANT.VARIANT_id==variant_id)).select(db.SAMPLE.sample)
    for row in rows:
        s.append(row.sample)
    return '|'.join(s)

@auth.requires_permission('view', 'VARIANT')
def samples_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    response.title = T('Variants with samples list')
    form_head=head_title(response.title,form_head_indietro)

    links = [lambda row: A('Variant', _title=T('Edit Variant')
                            ,_class='btn btn-default btn-secondary btn-link btn-sm'
                            ,_href=URL("variant","edit",args=[row[field_id]]
                                       ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           )
            ,lambda row: A(' ' , _title=T('Classif History')
                               ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                               ,_href=URL("variant","attribute_history",args=[variant_default_classif_id(row.id)]
                                          ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           ) if num_variant_attribute(row.id,DEFAULT_CLASSIF) > 1 else ''
             ,dict(header='',
                  body=lambda row: A(str(num_samples_of_variant(row[field_id]))
                                    ,_title=T('Samples')
                                    ,_class='btn btn-success btn-sm'
                                    ,_href=URL('sample_variant','samples_of_variant',args=[row[field_id]])
                                    ,_target='blank'
                                   ) if num_samples_of_variant(row[field_id])>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                                         else SPAN(str(num_samples_of_variant(row[field_id])),_class='btn btn-success btn-sm')\
                                         if num_samples_of_variant(row[field_id])>0 else ''
                  )

             ]


    for field in db.VARIANT:
        field.readable = False


    fields = [db.VARIANT.gene
             ,db.VARIANT.id_hg19
             ,db.VARIANT.classif
             ,db.VARIANT.id
             ]

    for field in fields:
        field.readable = True

    db.VARIANT.id.represent  = lambda value,row: List_samples_of_variant(value)
    db.VARIANT.id.label= T('Samples list')

    query =(db.VARIANT)
    field_id = db.VARIANT.id

    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19 ]


    form = SQLFORM.grid(query=query
                       ,fields=fields
                       #,headers=headers
                       #,left = left
                        ,links = links
                        ,links_in_grid = True
                       #,field_id = field_id
                        ,orderby=default_sort_order
                        ,create=False
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
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati
    return response.render(default_view, dict(form_head=form_head,form=form))
