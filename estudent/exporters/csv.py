import csv
from ._base import TimetableExporter
from ..class_ import RegisteredClass

class Csv(TimetableExporter):
    def __init__(self, **writer_options):
        if 'quoting' not in writer_options:
            writer_options['quoting'] = csv.QUOTE_ALL
        self.writer_options = writer_options

    def dump(self, study_period, file):
        writer = csv.writer(file, **self.writer_options)
        writerow = writer.writerow

        units = study_period.units()
        classes = [c for u in units for c in u.classes if isinstance(c, RegisteredClass)]

        writerow('who what when where'.split())
        for c in classes:
            start_time = c.start_time.strftime('%H:%M')
            end_time = c.end_time.strftime('%H:%M')
            when = f"{c.day.name.title()} {start_time}-{end_time}"
            location = c.location
            if location.startswith('North Ryde '):
                location = location[11:]
            row = (c.unit_code, c.name, when, location)
            writerow(row)
