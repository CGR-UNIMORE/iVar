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

from gluon.sqlhtml import ExportClass
from gluon.sqlhtml import ExporterCSV
from gluon.sqlhtml import ExporterTSV

#if request.vars._export_type
# when export is called

from cStringIO import StringIO
import csv

class ExporterCSVLabel(ExportClass):
    """This class is used to export header from label end not from field name"""
    file_ext = "csv"
    content_type = "text/csv"

    def __init__(self, rows):
        self.rows = rows

    def export(self):
        if self.rows:
            s = StringIO()
            csv_writer = csv.writer(s)
            # obtain column names of current table
            #col = self.rows.colnames
            # col contains list of column names
            # e.g: ["employee.id", "employee.name",
            #       "employee.email", "employee.company"]
            # get label of field
            header = list()
            for col in self.rows.colnames:
                col = col.replace('"','')
                (t, f) = col.split('.')
                field = self.rows.db[t][f]
                colname = field.label
                header.append(colname)
            # Write explicitly the heading in CSV
            csv_writer.writerow(header)
            # don't write default colnames
            self.rows.export_to_csv_file(
                s, represent=True, write_colnames=False)
            return s.getvalue()
        else:
            return ''

class ExporterTSVLabel(ExportClass):
    label = 'TSV'
    file_ext = "csv"
    content_type = "text/tab-separated-values"

    def __init__(self, rows):
        self.rows = rows

    def export(self):
        if self.rows:
            s = StringIO()
            csv_writer = csv.writer(s, delimiter='\t')
            # obtain column names of current table
            #col = self.rows.colnames
            # col contains list of column names
            # e.g: ["employee.id", "employee.name",
            #       "employee.email", "employee.company"]
            # get label of field
            header = list()
            for col in self.rows.colnames:
                col = col.replace('"','')
                (t, f) = col.split('.')
                field = self.rows.db[t][f]
                colname = field.label
                header.append(colname)
            # Write explicitly the heading in CSV
            csv_writer.writerow(header)
            # don't write default colnames
            self.rows.export_to_csv_file(
                s, represent=True, write_colnames=False, delimiter='\t', newline='\n')
            return s.getvalue()
        else:
            return ''
