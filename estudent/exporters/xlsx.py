import csv
import xlsxwriter
import os
from ._base import TimetableExporter
from ..class_ import RegisteredClass

class Xlsx(TimetableExporter):
    def __init__(self, **writer_options):
        if 'quoting' not in writer_options:
            writer_options['quoting'] = csv.QUOTE_ALL
        self.writer_options = writer_options

    def dump(self, study_period, file):
        savePath = os.path.dirname(os.path.dirname(__file__)) + "\\timetables\\timetable.xlsx"
        print("Saving file to " + savePath)
        workbook = xlsxwriter.Workbook(savePath)
        worksheet = workbook.add_worksheet('timetable')

        days = ['','Monday','Tuesday','Wednesday','Thursday','Friday']
        dayAbbr = ['Mon', 'Tue', 'Wed','Thu', 'Fri']

        hours = []
        for i in range(7,22):
            hours.append(str(i) + ":00");
            worksheet.write((i+1)-7,0, str(i) + ":00")

        for i in range(len(days)):
            worksheet.write(0,i, days[i]);
        
        units = study_period.units()
        classes = [c for u in units for c in u.classes if isinstance(c, RegisteredClass)]

        #cell_format = workbook.add_format({'bg_color' : 'red'})
        
        #https://xlsxwriter.readthedocs.io/format.html#set_bg_color
        #colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#F0F0F0', '#F000F0']
        colors = ['blue', 'green', 'magenta', 'orange', 'pink', 'purple', 'red', 'yellow', 'navy']

        codes = []
        formats = []
        
        for c in classes:
            codes.append(c.unit_code)
        codes = list(dict.fromkeys(codes))

        for c in codes:
            formats.append(workbook.add_format({'bg_color' : colors[codes.index(c)]}))

        for c in classes:
            sHour = c.start_time.strftime('%H')
            sMinute = c.start_time.strftime('%M')

            eHour = c.end_time.strftime('%H')
            eMinute = c.end_time.strftime('%M')

            worksheet.write((int(sHour) - 7) + 1, dayAbbr.index(c.day.name.title()) + 1, str(c.unit_code), formats[codes.index(c.unit_code)])  
            
            #when = f"{c.day.name.title()} {start_time}-{end_time}"
            #location = c.location
            #if location.startswith('North Ryde '):
            #    location = location[11:]
        workbook.close()
