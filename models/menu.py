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




response.menu = [
      (T('Home'), False,URL('default', 'index'))
     ,(T('VCF files'), True, '#',[
             (T('Import VCF'), False, URL('vcf','import_file') ) if auth.has_permission('import', 'VCF') else ('',False,None)
            ,(T('Processes VCF'), False, URL('vcf','list_edit')) if auth.has_permission('manage', 'VCF') else ('',False,None)
            ,(T('VCF files'), False, URL('vcf','vcf_list'))
            ,(T('VCF types'), False, URL('vcf','vcf_type_list'))
            ,(T('VCF analysis panel'), False,URL('vcf','panel_list'))
            ,(T('Virtual panel for VCF filtering'),False, URL('vcf','virtual_panel_list'))
                                ] )  if auth.has_permission('view', 'VCF') else ('',False,None)
       ,(T('Text files'), False, '#',[
             (T('Export VCF for re-annotation'), False, URL('annotation','export_vcf')) if auth.has_permission('import', 'ANNOTATION') else ('',False,None)
            ,(T('Import Text files'), False, URL('annotation','import_file')) if auth.has_permission('import', 'ANNOTATION') else ('',False,None)
            ,(T('Processes Text files'), False, URL('annotation','list_edit')) if auth.has_permission('manage', 'ANNOTATION') else ('',False,None)
            ,(T('Text files'), False, URL('annotation','annotation_file_list'))
            ,(T('Text file types'), False, URL('annotation','annotation_type_list'))
                                   ] ) if auth.has_permission('view', 'ANNOTATION') else ('',False,None)
     ,(T('Samples'), False, '#',[
             (T('Samples'), False, URL('sample','list'))
            ,(T('Samples manage'), False, URL('sample','list_edit'))
            ,(T('Samples and variants'), False, URL('sample_variant','list'))
            ,(T('Tissue type'), False, URL('sample','tissue_type_list'))
                                ] )  if auth.has_permission('view', 'SAMPLE') else ('',False,None)
   ,(T('Variants'), False, '#',[
             (T('Variants'), False, URL('variant','list'))
            ,(T('special attributes'), False, URL('variant_query','special_attribute'))
            ,(T('current attributes'), False, URL('variant_query','attribute_current'))
            ,(T('all attributes'), False, URL('variant_query','attribute'))
            ,(T('with samples list'), False, URL('variant_query','samples_list'))
                               ] ) if auth.has_permission('view', 'VARIANT') else ('',False,None)

     ,(T('Search'), False, '#',[
             (T('Variants and attributes'), False, URL('search','variant_attribute'))
            ,(T('Search criteria'), False, URL('search','search_criteria_list'))
                               ] ) if auth.has_permission('view', 'VARIANT') else ('',False,None)
   ,(T('Admin'), False, '#',[
             (T('User'), True, URL('admin','user'))
           #,(T('Log'), False, URL('admin','visualizza_log'))
            ,(T('Delete Variants attribute'), False, URL('variant','delete_attribute')) if auth.has_permission('delete', 'VARIANT') else ('',False,None)
                            ]) if auth.has_permission('ADMIN', '') else ('',False,None)  
    ]
