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

@auth.requires_permission('ADMIN', '')
def user():
    response.title = 'Users Management'
    form_head=head_title(response.title) 

    query= (db.auth_user)

    #left = db.auth_membership.on(db.auth_membership.user_id == db.auth_user.id )

    fields= (db.auth_user.id
            ,db.auth_user.first_name
            ,db.auth_user.last_name
            #,db.auth_user.username
            ,db.auth_user.email
            ,db.auth_user.password
            )
    
    links = [ dict(header='',
                  body=lambda row: A(T('Groups'),_class='btn btn-success btn-sm',_title=T('Groups'),_href=URL('admin','membership_list',args=[row.id]))
                  )
            ]

    def is_editable(rows): return (auth.has_permission('ADMIN', ''))
    def is_create():   return (auth.has_permission('ADMIN', ''))
   
    def oncreate(form): return redirect(URL('admin','user'))
    def onupdate(form): return redirect(URL('admin','user'))

    form = SQLFORM.grid(query=query
                       ,fields=fields
                      #,headers=headers
                      #,left=left
                       ,links = links
                       ,create=is_create()
                       ,deletable=False
                       ,editable=is_editable
                       ,oncreate= oncreate
                       ,onupdate= onupdate
                       ,csv = False
                       ,sorter_icons=(XML('&#x2191;'), XML('&#x2193;'))
                       ,showbuttontext=False
                       ,maxtextlength=50
                      #,maxtextlengths=maxtextlengths
                       ,paginate=15
                       ,buttons_placement = 'left'
                       ,links_placement = 'right'
                       ,user_signature=False
                       ,args=request.args[:1]
                      )


    return response.render(default_view, dict(form_head=form_head,form=form))


@auth.requires_permission('ADMIN', '')
def membership_list():

    user_id = request.args(0) or redirect(URL('admin','user'))

    response.title = 'Authorizations User'
    form_head=head_title(response.title) 

    query = (db.auth_membership.user_id==user_id)

    db.auth_membership.id.readable=False
    db.auth_membership.id.writeable=False

    db.auth_membership.user_id.default = user_id
    db.auth_membership.user_id.writable = False

    def is_create()      :return (auth.has_permission('ADMIN', ''))
    def is_deletable()   :return (auth.has_permission('ADMIN', ''))
    def is_editable()    :return (auth.has_permission('ADMIN', ''))
    def is_visible()     :return (auth.has_permission('ADMIN', ''))


    links = [(lambda row: A('', _title=T('Detail')
                            ,_class='btn btn-default btn-sm glyphicon glyphicon-pencil'
                            ,_href=URL("admin","membership",args=[row.id])) if is_visible() else '')
            ]


    def create_membership(form):
        if 'new' in request.args:
           redirect(URL("admin","membership",args=[form.vars.id]))
        return True


    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid=True
                        ,create=is_create()
                        ,deletable=is_deletable()
                        ,editable=False
                        ,details=False
                        #,sorter_icons=(XML('&#x2191;'), XML('&#x2193;'))
                        ,showbuttontext=False
                        ,maxtextlength=50
                        #,maxtextlengths=maxtextlengths
                        ,paginate=10
                        ,csv = False
                        #,exportclasses=exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,oncreate=create_membership
                        ,user_signature=False
                        ,args=request.args[:1]
                        )

    back = A(' ' , _title=T('User'), _class='button btn btn-default glyphicon glyphicon-arrow-left', _href=URL('admin','user'))
    form[0].insert(0,back)

    return response.render(default_view, dict(form_head=form_head,form=form))


@auth.requires_permission('ADMIN', '')
def membership():
#è solo per edit/delete. Insert non passa di qui, ma viene gestito dall 'insert della grid
    membership_id = request.args(0) or redirect(URL('admin','membership_list'))
    if membership_id=='None': 
        session.flash = T('Error occurred during call "membership"')
        redirect(URL('admin','user'))

    record = db.auth_membership(db.auth_membership.id==membership_id) or redirect(URL('admin','user'))

    response.title = T('Authorization User')
    form_head=head_title(response.title) 

    db.auth_membership.id.readable = False
    db.auth_membership.id.writable = False

    db.auth_membership.user_id.readable = True
    db.auth_membership.user_id.writable = False


    def is_readonly() : return not (auth.has_permission('ADMIN', ''))
    def is_deletable(): return   (auth.has_permission('ADMIN', ''))

    form=SQLFORM(db.auth_membership
                ,record
                ,readonly=is_readonly()
                ,deletable=is_deletable()
                )

    back = A(' ' , _title=T('Authorizations User'), _class='button btn btn-default glyphicon glyphicon-arrow-left', _href=URL('admin','membership_list',args=[record.user_id]))
    form[0].insert(0,back)

    if form.process().accepted:
        if form.deleted:
            session.flash = T('delete done')
            redirect(URL('admin','membership_list',args=[record.user_id]))
        else:
            if record:
                response.flash = T('modify done')
            else:
                session.flash = T('insert done')
                redirect(URL("admin","membership",args=[id]))


    return response.render(default_view, dict(form_head=form_head,form=form))

#visibile a tutti
def news_list():

    response.title = 'News List'
    form_head=head_title(response.title) 

    query = (db.NEWS.id>0)

    db.NEWS.id.readable=False
    db.NEWS.id.writeable=False

    def is_create()      :return (auth.has_permission('NEWS', ''))
    def is_deletable()   :return (auth.has_permission('NEWS', ''))
    def is_editable()    :return (auth.has_permission('NEWS', ''))
    def is_visible()     :return True


    default_sort_order=[~db.NEWS.data_dal]

    links = [(lambda row: A('', _title=T('Detail')
                            ,_class='btn btn-default btn-sm glyphicon glyphicon-pencil'
                            ,_href=URL("admin","news",args=[row.id])) if is_visible() else '')
            ]


    def create_news(form):
        if 'new' in request.args:
           redirect(URL("admin","news_list"))
        return True


    form = SQLFORM.grid(query=query
                        #,fields=fields
                        #,headers=headers
                        ,links = links
                        ,links_in_grid=True
                        ,orderby=default_sort_order
                        ,create=is_create()
                        ,deletable=is_deletable()
                        ,editable=False
                        ,details=False
                        #,sorter_icons=(XML('&#x2191;'), XML('&#x2193;'))
                        ,showbuttontext=False
                        ,maxtextlength=255
                        #,maxtextlengths=maxtextlengths
                        ,paginate=10
                        ,csv = False
                        #,exportclasses=exportclasses
                        ,buttons_placement = 'left'
                        ,links_placement = 'right'
                        ,oncreate=create_news
                        ,user_signature=False
                        ,args=request.args[:1]
                        )

    """
    back = A(' ' , _title=T('Users'), _class='button btn btn-default glyphicon glyphicon-arrow-left', _href=URL('admin','user'))
    form[0].insert(0,back)
    """
    return response.render(default_view, dict(form_head=form_head,form=form))

#vedono tutti
def news():
#è solo per edit/delete. Insert non passa di qui, ma viene gestito dall 'insert della grid
    news_id = request.args(0) or redirect(URL('admin','news_list'))
    if news_id=='None': 
        session.flash = T('Error occurred during call "Edit News"')
        redirect(URL('admin','news_list'))

    record = db.NEWS(db.NEWS.id==news_id) or redirect(URL('admin','news_list'))

    response.title = T('Edit News')
    form_head=head_title(response.title) 

    db.NEWS.id.readable = False
    db.NEWS.id.writable = False

    def is_readonly() : return not (auth.has_permission('NEWS', ''))
    def is_deletable(): return   (auth.has_permission('NEWS', ''))

    form=SQLFORM(db.NEWS
                ,record
                ,readonly=is_readonly()
                ,deletable=is_deletable()
                )

    back = A(' ' , _title=T('News List'), _class='button btn btn-default glyphicon glyphicon-arrow-left', _href=URL('admin','news_list'))
    form[0].insert(0,back)

    if form.process().accepted:
        if form.deleted:
            session.flash = T('delete done')
            redirect(URL('admin','news_list'))
        else:
            if record:
                response.flash = T('modify done')
            else:
                session.flash = T('insert done')
                redirect(URL("admin","news",args=[id]))


    return response.render(default_view, dict(form_head=form_head,form=form))
