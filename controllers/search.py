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

##############################
####   VSEARCH_CRITERIA   ####
##############################

@auth.requires_permission('view', 'VARIANT')
def search_criteria_list():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    response.title = T('Search criteria')
    form_head=head_title(response.title,form_head_indietro)

    def is_create(): return auth.has_permission('manage', 'VARIANT')
    def is_visible(): return auth.has_permission('view', 'VARIANT')

    links = [lambda row:A('', _title=T('Edit')
                            ,_class='btn btn-default btn-secondary btn-sm icon pen icon-pen glyphicon glyphicon-pencil'
                            ,_href=URL('search_criteria_edit',args=[row.id]
                                       ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                      ) if is_visible() else ''
             ,lambda row: A('', _title=T('Duplicate')
                            ,_class='btn btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                            ,_href=URL('search_criteria_copy',args=[row.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                           ) if is_create() else ''
         ]

    db.SEARCH_CRITERIA.id.readable=False
    db.SEARCH_CRITERIA.id.writeable=False

    query= (db.SEARCH_CRITERIA)

    default_sort_order=[db.SEARCH_CRITERIA.search_name]


    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        #,links_in_grid = True
                        ,orderby=default_sort_order
                        ,create=False
                        ,deletable= False
                        ,editable=False
                        ,details=False
                        ,showbuttontext=False
                        ,maxtextlength=50
                        ,paginate=DEFAULT_PAGINATE #8
                        ,csv = False
                        #,exportclasses=default_exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,onvalidation=validation_SEARCH_CRITERIA
                        ,user_signature=False
                        ,args=request.args[:1]
                       )

    #form.element('.web2py_counter', replace=None) # toglie numero records trovati

    add_record = A(' ' , _title=T('Add')
                       ,_class='button btn btn-default btn-secondary btn-sm icon plus icon-plus glyphicon glyphicon-plus'
                       ,_href=URL('search_criteria_insert'
                                 ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                       ,_name='btn_search_criteria_Add'
                       ,_id ='btn_search_criteria_Add'
                  )

    form[0].insert(-2,add_record) if auth.has_permission('manage', 'VARIANT')else ''

    return response.render(default_view, dict(form_head=form_head,form=form))

@auth.requires_permission('manage', 'VARIANT')
def search_criteria_copy():
    search_criteria_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not search_criteria_id:
        session.flash = T('error occured during call "Duplicate search criteria"')
        redirect(form_head_indietro)

    copy_SEARCH_CRITERIA(search_criteria_id)
    redirect(form_head_indietro)
    return

def search_criteria_form(record,form_head_indietro):
    response.title = T('Variant Search criteria')
    form_head=head_title(response.title,form_head_indietro)

    db.SEARCH_CRITERIA.id.writable = False
    db.SEARCH_CRITERIA.id.readable = False


    form=SQLFORM(db.SEARCH_CRITERIA
                ,record
                ,readonly=False
                ,deletable=True
                #,formstyle="bootstrap4_stacked" #"table3cols"#"bootstrap3_inline","bootstrap2", "table3cols", "table2cols"  bootstrap3_stacked
                ,args=request.args[:1]
                )
    #form.custom.widget['HP_id'][0].add_class('form-control')

    if form.process(onvalidation=validation_SEARCH_CRITERIA).accepted:
        if form.deleted:
            session.flash = T('delete done')
        else:
            if record:
                response.flash = T('modify done')
            #else: # sono in inserimento
        redirect(form_head_indietro)

    return dict(form_head=form_head,form=form)

@auth.requires_permission('view', 'VARIANT')
def search_criteria_edit():
    search_criteria_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    
    if not search_criteria_id:
        return response.render(default_view, dict(form_head='',form=''))

    record = db.SEARCH_CRITERIA(db.SEARCH_CRITERIA.id==search_criteria_id) or None

    dict_forms = search_criteria_form(record,form_head_indietro)

    return response.render(default_view, dict_forms)

@auth.requires_permission('manage', 'VARIANT')
def search_criteria_insert():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    dict_forms = search_criteria_form(None,form_head_indietro)

    return response.render(default_view, dict_forms)


######################################
####   VARIANT ATTRIBUTE SEARCH   ####
######################################

@auth.requires_permission('view', 'VARIANT')
def variant_attribute():
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    response.title = T('Variants and attributes search')
    form_head=head_title(response.title,form_head_indietro)

    #campi di ricerca
    search_criteria_id = request.vars.search_criteria_id
    fl_time_criteria = request.vars.fl_time_criteria or None
    date_from = string_to_date(request.vars.date_from, '%d/%m/%Y')
    date_to = string_to_date(request.vars.date_to, '%d/%m/%Y')
    fl_values_criteria = request.vars.fl_values_criteria or None
    fl_type_result = request.vars.fl_type_result or "A"

    form = SQLFORM.factory(
                Field('search_criteria_id' , type='integer'
                                           , label = T('Search criteria')
                                           , default = search_criteria_id
                                           , requires = IS_IN_DB(db, 'SEARCH_CRITERIA.id', '%(search_name)s', error_message=T('mandatory'))
                     )
               ,Field('fl_time_criteria'   , label = T('attribute valid date')
                                           , requires = IS_EMPTY_OR(IS_IN_SET([('C',T('only current value'))
                                                                              ,('V',T('after last check'))
                                                                              ,('P',T('date from/to:'))]
                                                                              ,multiple = True)
                                                                    )
                                           , default = fl_time_criteria
                                           , widget=lambda f,v : SQLFORM.widgets.checkboxes.widget(f,v,style='table', cols=3, _width='115%')
                     )

               ,Field('date_from'          , type='date'
                                           , label = T('from date:')
                                           , default = date_from
                                           , requires = IS_EMPTY_OR(IS_DATE(format='%d/%m/%Y'))
                     )
               ,Field('date_to'            , type='date'
                                           , label = T('to date:')
                                           , default = date_to
                                           , requires = IS_EMPTY_OR(IS_DATE(format='%d/%m/%Y'))
                     )
               ,Field('fl_values_criteria' 
                                           , label = T('Attribute criteria')
                                           , requires = IS_EMPTY_OR(IS_IN_SET([('U',T('only with unique value')) #new
                                                                              ,('H',T('only with historical values'))
                                                                              ],multiple = False,error_message=T('check only one'))
                                                                    )
                                           , default = fl_values_criteria
                                           , widget=lambda f,v : SQLFORM.widgets.checkboxes.widget(f,v,style='table', cols=2, _width='119%')
                     )
               ,Field('fl_type_result'
                                           , label = T('List of results')
                                           , requires = IS_IN_SET([('A',T('Attributes'))
                                                                  ,('P',T('Attributes with previous'))
                                                                  ,('V',T('only Variants'))
                                                                  ,('S',T('Samples of Variants'))
                                                                  ])
                                           , default = fl_type_result
                                           , widget=lambda f,v : SQLFORM.widgets.radio.widget(f,v,style='table', cols=4, _width='114%')
                     )
               #,formstyle='bootstrap4_stacked' #table3cols'#bootstrap3_inline'#'divs'
               ,submit_button = T("Search")
               ,table_name = "search"
            )


#risposta
    iframe_search_results=''
    search_criteria_id = None
    fl_time_criteria = None
    date_from = None
    date_to = None
    fl_values_criteria = None
    if form.process(onvalidation=validation_search_variant_attribute).accepted:
    #if form.process().accepted:
        response.flash = ''
        search_criteria_id = form.vars.search_criteria_id
        fl_time_criteria = form.vars.fl_time_criteria
        date_from = date_to_string(string_to_date(request.vars.date_from, '%d/%m/%Y'),'%Y-%m-%d')
        date_to = date_to_string(string_to_date(request.vars.date_to, '%d/%m/%Y'),'%Y-%m-%d')
        fl_values_criteria = form.vars.fl_values_criteria
        fl_type_result = form.vars.fl_type_result


        url = ""
        if fl_type_result == "A":
            url = 'variant_attribute_list'
        if fl_type_result == "P":
            url = 'variant_attribute_prev_list'
        if fl_type_result == "V":
            url='variant_list'
        if fl_type_result == "C":
            url = 'variant_attribute_current_list'
        if fl_type_result == "S":
            url = 'sample_of_variants_list'

        iframe_search_results = DIV(
                                    DIV(A(T('open in new tab')
                                          ,_title = T('open in new tab')
                                          ,_href=URL(url,args=[search_criteria_id]
                                                                 ,vars=dict(rows_for_page = DEFAULT_PAGINATE*5 #50
                                                                           ,fl_values_criteria = fl_values_criteria
                                                                           ,fl_time_criteria=fl_time_criteria
                                                                           ,date_from=date_from,date_to=date_to))
                                          ,_target = 'blank'
                                          ,_class ="button btn btn-default btn-warning btn-sm"
                                          )
                                        ,_align="right",_style="margin-top:0;margin-bottom:0"
                                       )
                                    ,IFRAME(T('Search\'s result')
                                            ,_title=T('Search\'s result')
                                            ,_src=URL(url
                                                      ,args=[search_criteria_id]
                                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)
                                                                ,fl_values_criteria = fl_values_criteria
                                                                ,fl_time_criteria=fl_time_criteria
                                                                ,date_from=date_from,date_to=date_to
                                                                 ))
                                            ,_style="padding-top:0px;height:100%; width:100%"
                                            ,_frameborder='0',_scrolling='yes'
                                            ,_onload='resize_iframe(this)'
                                            ,_id='iframe_search_result'
                                           )
                                    ,_style="margin-top:0"
                                    )


    elif form.errors:
        response.flash = ''


    return dict(form_head=form_head,form=form,iframe_search_results=iframe_search_results)

def validation_search_variant_attribute(form):
    if request.vars['fl_time_criteria'] == "P" :
        if request.vars['date_from'] != "" and request.vars['date_to'] != "":
            date_from =  string_to_date(request.vars.date_from, '%d/%m/%Y')
            date_to =  string_to_date(request.vars.date_to, '%d/%m/%Y')
            if date_from > date_to:
                form.errors.date_from = T('Date from > date to')

    return True

@auth.requires_permission('view', 'VARIANT')
def variant_list():
    search_criteria_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not search_criteria_id:
        redirect(form_head_indietro)

    fl_values_criteria = (request.vars['fl_values_criteria']) if (request.vars['fl_values_criteria']) else None
    fl_time_criteria = (request.vars['fl_time_criteria']) if (request.vars['fl_time_criteria']) else None
    date_from = (request.vars['date_from']) if (request.vars['date_from']) else None
    date_to = (request.vars['date_to']) if (request.vars['date_to']) else None
    rows_for_page = int((request.vars['rows_for_page'])) if (request.vars['rows_for_page']) else DEFAULT_PAGINATE/2 #5

    links = [lambda row: A('Variant', _title=T('Edit Variant')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","edit" ,args=[row.id])
                                    ,_target="blank"
                          )
             ,lambda row: A(str(num_samples_of_variant(row.id))[0:6]
                            ,_title=T('Samples')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','samples_of_variant',args=[row.id])
                            ,_target='blank'
                            ) if num_samples_of_variant(row.id)>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                             else SPAN(str(num_samples_of_variant(row.id)),_class='btn btn-success btn-sm')\
                               if num_samples_of_variant(row.id)>0 else ''
            ,dict(header='',
                  body=lambda row: A(' ' , _title=T('Classif History')
                                    ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                                    ,_href=URL("variant","attribute_history",args=[variant_default_classif_id(row.id)])
                                    ,_target='blank'
                                    ) if num_variant_attribute(row.id,DEFAULT_CLASSIF) > 1 else ''
                  )

            ]

    for field in db.VARIANT:
        field.readable = False
    db.VARIANT.id.writable = False

    fields= (db.VARIANT.gene
            ,db.VARIANT.id_hg19
            ,db.VARIANT.id_hg38
            ,db.VARIANT.classif
            ,db.VARIANT.last_check
            )

    for field in fields:
        field.readable = True


    d = variant_attribute_query(search_criteria_id,fl_values_criteria,fl_time_criteria, date_from,date_to,"V")
    query = d["query"]
    q = d["q"]

    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19]

    
    #debug
    #form_head = FORM(DIV(q))
    #query = -1
    if query == -1:
        form = FORM(DIV(T('ERROR in Search criteria setting!')
                       ,A(' -> Search Criteria', _href=URL('search_criteria_list'), _target = 'blank')
                       ,BR()
                       ,q))
    elif query:
        form = SQLFORM.grid(query=query
                            ,fields=fields
                            #,headers=headers
                            #,field_id=field_id
                            ,links = links
                            ,links_in_grid = True
                            ,orderby=default_sort_order
                            ,create=False
                            ,deletable=False
                            ,editable=False
                            ,details=False
                            ,showbuttontext=False
                            ,maxtextlength=50
                            ,paginate=rows_for_page
                            ,csv = True
                            ,exportclasses=default_exportclasses
                            ,buttons_placement = 'left'
                            ,links_placement = 'right'
                            ,user_signature=False
                            ,args=request.args[:1]
                           )
    else:
        form = ''

    return response.render(default_subview, dict(form_head='',form=form))
@auth.requires_permission('view', 'VARIANT')
def sample_of_variants_list():
    search_criteria_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not search_criteria_id:
        redirect(form_head_indietro)

    fl_values_criteria = (request.vars['fl_values_criteria']) if (request.vars['fl_values_criteria']) else None
    fl_time_criteria = (request.vars['fl_time_criteria']) if (request.vars['fl_time_criteria']) else None
    date_from = (request.vars['date_from']) if (request.vars['date_from']) else None
    date_to = (request.vars['date_to']) if (request.vars['date_to']) else None
    rows_for_page = int((request.vars['rows_for_page'])) if (request.vars['rows_for_page']) else DEFAULT_PAGINATE/2 #5

    links = [lambda row: A('Sample', _title=T('Edit Sample')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("sample","edit" ,args=[row.id])
                                    ,_target="blank"
                          )
             ,lambda row: A(str(num_variants_of_sample(row.id))[0:6]
                            ,_title=T('Variants')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','variants_of_sample',args=[row.id])
                            ,_target='blank'
                            ) if num_variants_of_sample(row.id)>0 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                             else SPAN(str(num_variants_of_sample(row.id)),_class='btn btn-success btn-sm')\
                               if num_variants_of_sample(row.id)>0 else ''
            ]

    for field in db.SAMPLE:
        field.readable = False
    db.SAMPLE.id.writable = False

    fields= [db.SAMPLE.sample
            ,db.SAMPLE.date_sample
            ,db.SAMPLE.fl_sample_type
            ,db.SAMPLE.TISSUE_TYPE_id
            ,db.SAMPLE.fl_sex
            ]

    for field in fields:
        field.readable = True


    d = variant_attribute_query(search_criteria_id,fl_values_criteria,fl_time_criteria, date_from,date_to,"S")
    query = d["query"]
    q = d["q"]

    default_sort_order=[db.SAMPLE.sample]

    
    #debug
    #form_head = FORM(DIV(q))
    #query = -1
    if query == -1:
        form = FORM(DIV(T('ERROR in Search criteria setting!')
                       ,A(' -> Search Criteria', _href=URL('search_criteria_list'), _target = 'blank')
                       ,BR()
                       ,q))
    elif query:
        form = SQLFORM.grid(query=query
                            ,fields=fields
                            #,headers=headers
                            #,field_id=field_id
                            ,links = links
                            ,links_in_grid = True
                            ,orderby=default_sort_order
                            ,create=False
                            ,deletable=False
                            ,editable=False
                            ,details=False
                            ,showbuttontext=False
                            ,maxtextlength=50
                            ,paginate=rows_for_page
                            ,csv = True
                            ,exportclasses=default_exportclasses
                            ,buttons_placement = 'left'
                            ,links_placement = 'right'
                            ,user_signature=False
                            ,args=request.args[:1]
                           )
    else:
        form = ''

    return response.render(default_subview, dict(form_head='',form=form))

@auth.requires_permission('view', 'VARIANT')
def variant_attribute_list():
    search_criteria_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not search_criteria_id:
        redirect(form_head_indietro)

    fl_values_criteria = (request.vars['fl_values_criteria']) if (request.vars['fl_values_criteria']) else None
    fl_time_criteria = (request.vars['fl_time_criteria']) if (request.vars['fl_time_criteria']) else None
    date_from = (request.vars['date_from']) if (request.vars['date_from']) else None
    date_to = (request.vars['date_to']) if (request.vars['date_to']) else None
    rows_for_page = int((request.vars['rows_for_page'])) if (request.vars['rows_for_page']) else DEFAULT_PAGINATE/2 #4

    links = [lambda row: A('Variant', _title=T('Variant')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","edit" ,args=[row.VARIANT.id]
                                              ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                    ,_target="blank"
                          )
            ,lambda row: A(str(num_samples_of_variant(row.VARIANT.id))[0:6]
                            ,_title=T('Samples')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','samples_of_variant'
                                       ,args=[row.VARIANT.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                            ,_target='blank'
                            ) if num_samples_of_variant(row.VARIANT.id)>0\
                                 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                             else SPAN(str(num_samples_of_variant(row.VARIANT.id))
                                       ,_class='btn btn-success btn-sm')\
                               if num_samples_of_variant(row.VARIANT.id)>0 else ''
            ,lambda row: A(' ' , _title=T('History')
                            ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                            ,_href=URL("variant","attribute_history",args=[row.VARIANT_ATTRIBUTE.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                            ,_target='blank'
                           ) if num_variant_attribute(row.VARIANT.id
                                                     ,row.VARIANT_ATTRIBUTE.attribute_name) > 1 else ""
             ]

    for field in db.VARIANT:
        field.readable = False
    for field in db.VARIANT_ATTRIBUTE:
        field.readable = False

    fields= (db.VARIANT.gene
            ,db.VARIANT.id_hg19
            #,db.VARIANT.id_hg38
            ,db.VARIANT.classif
            ,db.VARIANT.last_check
            ,db.VARIANT.id
            ,db.VARIANT_ATTRIBUTE.valid_from
            ,db.VARIANT_ATTRIBUTE.attribute_name
            ,db.VARIANT_ATTRIBUTE.attribute_value
            )


    for field in fields:
        field.readable = True

    db.VARIANT.id.readable = False
    db.VARIANT_ATTRIBUTE.id.readable = False

    db.VARIANT.id.writable = False
    db.VARIANT_ATTRIBUTE.id.writable = False


    d = variant_attribute_query(search_criteria_id,fl_values_criteria,fl_time_criteria, date_from,date_to,"A")
    query = d["query"]
    q = d["q"]

    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19, db.VARIANT_ATTRIBUTE.attribute_name, db.VARIANT_ATTRIBUTE.valid_from]
    field_id = db.VARIANT_ATTRIBUTE.id

    #debug
    #form_head = FORM(DIV(q))
    #query = -1
    if query == -1:
        form = FORM(DIV(T('ERROR in Search criteria setting!')
                       ,A(' -> Search Criteria', _href=URL('search','search_criteria_list'), _target = 'blank')
                       ,BR()
                       ,q))
    elif query:
        form = SQLFORM.grid(query=query
                            ,fields=fields
                            #,headers=headers
                            ,field_id=field_id
                            ,links = links
                            ,links_in_grid = True
                            ,orderby=default_sort_order
                            ,create=False
                            ,deletable=False
                            ,editable=False
                            ,details=False
                            ,showbuttontext=False
                            ,maxtextlength=50
                            ,paginate=rows_for_page
                            ,csv = True
                            ,exportclasses=default_exportclasses
                            ,buttons_placement = 'left'
                            ,links_placement = 'right'
                            ,user_signature=False
                            ,args=request.args[:1]
                           )
    else:
        form = ''

    return response.render(default_subview, dict(form_head='',form=form))

@auth.requires_permission('view', 'VARIANT')
def variant_attribute_prev_list():
    search_criteria_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None

    if not search_criteria_id:
        redirect(form_head_indietro)

    fl_values_criteria = (request.vars['fl_values_criteria']) if (request.vars['fl_values_criteria']) else None
    fl_time_criteria = (request.vars['fl_time_criteria']) if (request.vars['fl_time_criteria']) else None
    date_from = (request.vars['date_from']) if (request.vars['date_from']) else None
    date_to = (request.vars['date_to']) if (request.vars['date_to']) else None
    rows_for_page = int((request.vars['rows_for_page'])) if (request.vars['rows_for_page']) else DEFAULT_PAGINATE/2 #4

    links = [lambda row: A('Variant', _title=T('Variant')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","edit" ,args=[row.VARIANT.id]
                                              ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                                    ,_target="blank"
                          )
            ,lambda row: A(str(num_samples_of_variant(row.VARIANT.id))[0:6]
                            ,_title=T('Samples')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','samples_of_variant'
                                       ,args=[row.VARIANT.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                            ,_target='blank'
                            ) if num_samples_of_variant(row.VARIANT.id)>0\
                                 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                             else SPAN(str(num_samples_of_variant(row.VARIANT.id))
                                       ,_class='btn btn-success btn-sm')\
                               if num_samples_of_variant(row.VARIANT.id)>0 else ''
            ,lambda row: A(' ' , _title=T('History')
                            ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                            ,_href=URL("variant","attribute_history",args=[row.VARIANT_ATTRIBUTE.id]
                                      ,vars=dict(form_head_indietro=URL(args=request.args, vars=request.get_vars, host=True)))
                            ,_target='blank'
                           ) if num_variant_attribute(row.VARIANT.id
                                                     ,row.VARIANT_ATTRIBUTE.attribute_name) > 1 else ""
             ]

    for field in db.VARIANT:
        field.readable = False
    for field in db.VARIANT_ATTRIBUTE:
        field.readable = False
    for field in db.VARIANT_ATTRIBUTE_PREV:
        field.readable = False

    fields= (db.VARIANT.gene
            ,db.VARIANT.id_hg19
            #,db.VARIANT.id_hg38
            ,db.VARIANT.classif
            #,db.VARIANT.last_check
            ,db.VARIANT.id
            ,db.VARIANT_ATTRIBUTE.valid_from
            ,db.VARIANT_ATTRIBUTE.attribute_name
            ,db.VARIANT_ATTRIBUTE.attribute_value
            ,db.VARIANT_ATTRIBUTE_PREV.attribute_value_prev
            )

    for field in fields:
        field.readable = True

    db.VARIANT.id.readable = False
    db.VARIANT_ATTRIBUTE.id.readable = False

    db.VARIANT.id.writable = False
    db.VARIANT_ATTRIBUTE.id.writable = False


    d = variant_attribute_query(search_criteria_id,fl_values_criteria,fl_time_criteria, date_from,date_to,"P")
    query = d["query"]
    q = d["q"]
    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19, db.VARIANT_ATTRIBUTE.attribute_name, db.VARIANT_ATTRIBUTE.valid_from]
    field_id = db.VARIANT_ATTRIBUTE.id

    #debug
    #form_head = FORM(DIV(q))
    #query = -1
    if query == -1:
        form = FORM(DIV(T('ERROR in Search criteria setting!')
                       ,A(' -> Search Criteria', _href=URL('search','search_criteria_list'), _target = 'blank')
                       ,BR()
                       ,q))
    elif query:
        form = SQLFORM.grid(query=query
                            ,fields=fields
                            #,headers=headers
                            ,field_id=field_id
                            ,links = links
                            ,links_in_grid = True
                            ,orderby=default_sort_order
                            ,create=False
                            ,deletable=False
                            ,editable=False
                            ,details=False
                            ,showbuttontext=False
                            ,maxtextlength=170
                            #,maxtextlengths=maxtextlengths
                            ,paginate=rows_for_page
                            ,csv = True
                            ,exportclasses=default_exportclasses
                            ,buttons_placement = 'left'
                            ,links_placement = 'right'
                            ,user_signature=False
                            ,args=request.args[:1]
                           )
    else:
        form = ''

    return response.render(default_subview, dict(form_head='',form=form))

@auth.requires_permission('view', 'VARIANT')
def variant_attribute_current_list():
    search_criteria_id = request.args(0) or None
    form_head_indietro = (request.vars['form_head_indietro']) if (request.vars['form_head_indietro']) else None
    if not search_criteria_id:
        redirect(form_head_indietro)

    fl_values_criteria = (request.vars['fl_values_criteria']) if (request.vars['fl_values_criteria']) else None
    fl_time_criteria = (request.vars['fl_time_criteria']) if (request.vars['fl_time_criteria']) else None
    date_from = (request.vars['date_from']) if (request.vars['date_from']) else None
    date_to = (request.vars['date_to']) if (request.vars['date_to']) else None
    rows_for_page = int((request.vars['rows_for_page'])) if (request.vars['rows_for_page']) else DEFAULT_PAGINATE/2 #4

    links = [lambda row: A('Variant', _title=T('Variant')
                                    ,_class='button btn btn-default btn-secondary btn-link btn-sm'
                                    ,_href=URL("variant","edit" 
                                               ,args=[variant_id_of_attribute(row.VARIANT_ATTRIBUTE_CURRENT.id)])
                                    ,_target="blank") 

             ,lambda row: A(str(num_samples_of_variant(row.VARIANT.id))[0:6]
                            ,_title=T('Samples')
                            ,_class='btn btn-success btn-sm'
                            ,_href=URL('sample_variant','samples_of_variant'
                                       ,args=[row.VARIANT.id])
                            ,_target='blank'
                           ) if num_samples_of_variant(row.VARIANT.id)>0\
                                 and auth.has_permission('view', 'SAMPLE_VARIANT')\
                             else SPAN(str(num_samples_of_variant(row.VARIANT.id))
                                       ,_class='btn btn-success btn-sm')\
                               if num_samples_of_variant(row.VARIANT.id)>0 else ''
            ,lambda row: A(' ' , _title=T('History')
                            ,_class='button btn btn-default btn-secondary btn-sm icon history icon-history glyphicon glyphicon-time'
                            ,_href=URL("variant","attribute_history",args=[row.VARIANT_ATTRIBUTE_CURRENT.id])
                            ,_target='blank'
                           ) if num_variant_attribute(row.VARIANT.id
                                                     ,row.VARIANT_ATTRIBUTE_CURRENT.attribute_name) > 1 else ""
            ]

    for field in db.VARIANT:
        field.readable = False
    for field in db.VARIANT_ATTRIBUTE_CURRENT:
        field.readable = False

    fields= (db.VARIANT.gene
            ,db.VARIANT.id_hg19
            ,db.VARIANT.classif
            ,db.VARIANT.last_check
            ,db.VARIANT.id
            ,db.VARIANT_ATTRIBUTE_CURRENT.valid_from
            ,db.VARIANT_ATTRIBUTE_CURRENT.attribute_name
            ,db.VARIANT_ATTRIBUTE_CURRENT.attribute_value
            )

    for field in fields:
        field.readable = True

    db.VARIANT.id.readable = False
    db.VARIANT_ATTRIBUTE_CURRENT.id.readable = False

    db.VARIANT_ATTRIBUTE_CURRENT.attribute_value.represent = lambda value,row: A(value
                                                                                 ,_title=row.VARIANT_ATTRIBUTE_CURRENT.attribute_value
                                                                                 )


    d = variant_attribute_query(search_criteria_id,fl_values_criteria,fl_time_criteria, date_from,date_to,"C")
    query = d["query"]
    q = d["q"]

    field_id = db.VARIANT_ATTRIBUTE_CURRENT.id
    default_sort_order=[db.VARIANT.gene, db.VARIANT.id_hg19,db.VARIANT_ATTRIBUTE_CURRENT.attribute_name]

    #debug
    #form_head = FORM(DIV(q))
    #query = -1
    if query == -1:
        form = FORM(DIV(T('ERROR in Search criteria setting!')
                       ,A(' -> Search Criteria', _href=URL('search','search_criteria_list'), _target = 'blank')
                       ,BR()
                       ,q))
    elif query:
        form = SQLFORM.grid(query=query
                            ,fields=fields
                            #,headers=headers
                            ,field_id=field_id
                            ,links = links
                            ,links_in_grid = True
                            ,orderby=default_sort_order
                            ,create=False
                            ,deletable=False
                            ,editable=False
                            ,details=False
                            ,showbuttontext=False
                            #,maxtextlength=50
                            ,paginate=rows_for_page
                            ,csv = True
                            ,exportclasses=default_exportclasses
                            ,buttons_placement = 'left'
                            ,links_placement = 'right'
                            ,user_signature=False
                            ,args=request.args[:1]
                           )
    else:
        form = ''

    return response.render(default_subview, dict(form_head='',form=form))


def variant_attribute_query(search_criteria_id, fl_values_criteria=[],fl_time_criteria=[], date_from=None,date_to=None,fl_type_result="A"):

    from pydal.helpers.methods import smart_query

    r = db(db.SEARCH_CRITERIA.id==search_criteria_id).select().first() or None
    if not r:
        return dict(query=-1, q=T('Search criteria not exist'))

    if date_from == 'None':
        date_from = None
    if date_to == 'None':
        date_to = None

    #fl_values_criteria is only Unique or only History
    #if fl_values_criteria:
    #    fl_values_criteria = ",".join(fl_values_criteria)


    if not fl_time_criteria:
        fl_time_criteria=[]
    if not isinstance(fl_time_criteria,list):
        fl_time_criteria = [fl_time_criteria]
    if 'P' in fl_time_criteria: # se periodo e non sono impostate le date, il periodo è indifferente!
        if not date_from and not date_to:
            fl_time_criteria.remove('P')


    variant_q = None
    if  r.variant and r.variant != "":
        try:
            variant_q = smart_query([db.VARIANT], r.variant)
        except:
            return dict(query=-1, q=str(r.variant))

    attribute_q= None
    if r.attribute and r.attribute != "":
        try:
            attribute_q = smart_query([db.VARIANT_ATTRIBUTE], r.attribute)
        except:
            return dict(query=-1, q=str(r.attribute))

    attribute_prev_q = None
    PREV = db.VARIANT_ATTRIBUTE.with_alias('PREV') #usato dopo, deve rimanere fuori dall'if
    if r.attribute_prev and r.attribute_prev != "":
        cond = r.attribute_prev.replace('VARIANT_ATTRIBUTE.','PREV.')
        try:
            attribute_prev_q = smart_query([PREV], cond)
        except:
            return dict(query=-1, q=str(r.attribute_prev))


    #time criteria lookingfor in VARIANT_ATTRIBUTE.validfrom: slide in time dimension
    time_q = True
    if "C" in fl_time_criteria: #current value
        time_q &= db.VARIANT_ATTRIBUTE.id == db.VARIANT_ATTRIBUTE_CURRENT.id
    if "V" in fl_time_criteria: #after last check in Variant
        time_q &= db.VARIANT_ATTRIBUTE.valid_from > db.VARIANT.last_check   #.coalesce('1900-01-01')
    if "P" in fl_time_criteria: #valid in specified range
        if date_from and date_to: 
            time_q &= (db.VARIANT_ATTRIBUTE.valid_from >= date_from) & (db.VARIANT_ATTRIBUTE.valid_from <= date_to)
        else:
            if date_from:
                time_q &= db.VARIANT_ATTRIBUTE.valid_from >= date_from
            if date_to:
                time_q &= db.VARIANT_ATTRIBUTE.valid_from <= date_to
    if time_q == True:
        time_q = None

    #attribute criteria (New/Update)
    newupdate_q = None
    if fl_values_criteria == "U": #only Unique
        """
        a = db()._select(db.VARIANT_ATTRIBUTE.id
                            ,groupby=[db.VARIANT_ATTRIBUTE.VARIANT_id, db.VARIANT_ATTRIBUTE.attribute_name]
                            ,having=(db.VARIANT_ATTRIBUTE.id.count()==1))
        newupdate_q = db.VARIANT_ATTRIBUTE.id.belongs(a)
        """
        newupdate_q = ((db.VARIANT_ATTRIBUTE.VARIANT_id == db.VARIANT_ATTRIBUTE_COUNT.VARIANT_id) &
                       (db.VARIANT_ATTRIBUTE.attribute_name ==  db.VARIANT_ATTRIBUTE_COUNT.attribute_name) &
                       (db.VARIANT_ATTRIBUTE_COUNT.count == 1))
    elif fl_values_criteria == "H": #only with History
        if attribute_prev_q:
            newupdate_q = (db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev == PREV.id)
        else:
            newupdate_q = ((db.VARIANT_ATTRIBUTE.VARIANT_id == db.VARIANT_ATTRIBUTE_COUNT.VARIANT_id) &
                       (db.VARIANT_ATTRIBUTE.attribute_name ==  db.VARIANT_ATTRIBUTE_COUNT.attribute_name) &
                       (db.VARIANT_ATTRIBUTE_COUNT.count > 1))

    else: #all attribute
        if attribute_prev_q:
            #                        (db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev == PREV.id))
            #too slow newupdate_q = ((db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev==None) |
            #                        (db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev == PREV.id))
            newupdate_q = (db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev == PREV.id)


    if attribute_prev_q:
        #tutti hanno un record in db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id
        if attribute_q:
            attribute_q &= (db.VARIANT_ATTRIBUTE.id==db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id) & attribute_prev_q
        else:
            attribute_q = (db.VARIANT_ATTRIBUTE.id==db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id) & attribute_prev_q

    all_q = db.VARIANT.id==db.VARIANT_ATTRIBUTE.VARIANT_id
    if variant_q:
        all_q &= variant_q
    if attribute_q:
        all_q &= attribute_q
    if time_q:
        all_q &= time_q
    if newupdate_q:
        all_q &= newupdate_q

    if fl_type_result == "A":
        select_q = all_q

    if fl_type_result == "P":
        select_q = (db.VARIANT_ATTRIBUTE.id == db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id)
        select_q &= all_q

    if fl_type_result == "V":
        a = db(all_q)._select(db.VARIANT.id, distinct=True)
        select_q = db.VARIANT.id.belongs(a)

    if fl_type_result == "S":
        a = db(all_q)._select(db.VARIANT.id, distinct=True)
        b = db(db.SAMPLE_VARIANT.VARIANT_id.belongs(a))._select(db.SAMPLE_VARIANT.SAMPLE_id, distinct=True)
        select_q = db.SAMPLE.id.belongs(b)
        #b = db((db.SAMPLE_VARIANT.VARIANT_id==db.VARIANT.id) & all_q)._select(db.SAMPLE_VARIANT.SAMPLE_id, distinct=True)
        #select_q = db.SAMPLE.id.belongs(a)

    if fl_type_result == "C": # non si fa più ma lo tengo
        select_q = (db.VARIANT_ATTRIBUTE.id == db.VARIANT_ATTRIBUTE_CURRENT.VARIANT_id)
        select_q &= all_q



    try:
        select  = db(select_q)._select()
    except:
        return dict(query=-1, q=str(select_q))

    return dict(query=select_q, q=str(select_q))

"""
    if  r.variant and r.variant != "":
        cond = r.variant
    else:
        cond = "VARIANT.id>0"
    try:
        variant_q = smart_query([db.VARIANT], cond)
    except:
        return dict(query=-1, q=str(cond))

    if r.attribute and r.attribute != "":
        cond = r.attribute
    else:
        cond = "VARIANT_ATTRIBUTE.id>0"
    try:
        attribute_q = smart_query([db.VARIANT_ATTRIBUTE], cond)
    except:
        return dict(query=-1, q=str(cond))

    
    if fl_values_criteria == "N": #only New
        attribute_prev_q = db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev==None
    else:
        PREV = db.VARIANT_ATTRIBUTE.with_alias('PREV')
        if r.attribute_prev and r.attribute_prev != "":
            cond = r.attribute_prev.replace('VARIANT_ATTRIBUTE.','PREV.')
            try:
                a = smart_query([PREV], cond)
            except:
                return dict(query=-1, q=str(cond))


    attribute_prev_q = None
    if fl_values_criteria == "N": #only New
        attribute_prev_q = db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev==None
    else:
        a = None
        if r.attribute_prev and r.attribute_prev != "":
            PREV = db.VARIANT_ATTRIBUTE.with_alias('PREV')
            cond = r.attribute_prev.replace('VARIANT_ATTRIBUTE.','PREV.')
            a= None
            try:
                a = smart_query([PREV], cond)
            except:
                return dict(query=-1, q=str(cond))
        if fl_values_criteria == "U": #only Update:
            attribute_prev_q = db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev==PREV.id # not none implicit
            if a:
                attribute_prev_q &= a
        else:#indifferent
            # if not attribute_privous condition has been set, no con dition query need
            if a:
                attribute_prev_q = db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev == PREV.id
                attribute_prev_q &= a
                attribute_prev_q |= db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev==None
                #attribute_prev_q = ((db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev==None) |
                #                    (db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id_prev == PREV.id & a))


        #time criteria lookfor in VARIANT_ATTRIBUTE.validfrom: slide in time dimension
        if fl_time_criteria == "V": #valid from after last check
            attribute_q &= db.VARIANT_ATTRIBUTE.valid_from > db.VARIANT.last_check.coalesce('1900-01-01')
        if fl_time_criteria == "C": #current value
            attribute_q &= db.VARIANT_ATTRIBUTE.id == db.VARIANT_ATTRIBUTE_CURRENT.id
        elif fl_time_criteria == "P": #valid in specityed period
            if date_from and date_to: #per mettere le parentesi corrette nella and
                attribute_q &= (db.VARIANT_ATTRIBUTE.valid_from >= date_from) & (db.VARIANT_ATTRIBUTE.valid_from <= date_to)
            else:
                if date_from:
                    attribute_q &= db.VARIANT_ATTRIBUTE.valid_from >= date_from
                if date_to:
                    attribute_q &= db.VARIANT_ATTRIBUTE.valid_from <= date_to


    if attribute_prev_q:
        #tutti hanno un record in db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id
        attribute_q &= (db.VARIANT_ATTRIBUTE.id==db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id)
        attribute_q &= attribute_prev_q
        #a = db(attribute_prev_q)._select(db.VARIANT_ATTRIBUTE_PREV.VARIANT_ATTRIBUTE_id)
        #attribute_q &= db.VARIANT_ATTRIBUTE.id.belongs(a)

    select_q = None
    if fl_type_result == "V":
        if attribute_q:
            a = db(attribute_q)._select(db.VARIANT_ATTRIBUTE.VARIANT_id)
            select_q = variant_q & db.VARIANT.id.belongs(a)

    if fl_type_result == "C":
        attribute_q &= db.VARIANT_ATTRIBUTE.id == db.VARIANT_ATTRIBUTE_CURRENT.id  #only current

        select_q = variant_q & (db.VARIANT.id == db.VARIANT_ATTRIBUTE.VARIANT_id) & attribute_q
 

    if fl_type_result == "A":
        select_q = variant_q & (db.VARIANT.id == db.VARIANT_ATTRIBUTE.VARIANT_id) & attribute_q

    try:
        select  = db(select_q)._select()
    except:
        return dict(query=-1, q=str(select_q))

    return dict(query=select_q, q=str(select_q))
"""
