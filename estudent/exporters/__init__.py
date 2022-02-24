
from . import (
    console,
    csv,
    csv2,
    ics,
    ios_class_timetable,
    xlsx
)

exporters_reg = {
    'console': console.Console,
    'csv': csv.Csv,
    'csv2': csv2.Csv2,
    'ics': ics.Ics,
    'ios_class_timetable': ios_class_timetable.ClassTimetable,
    'xlsx': xlsx.Xlsx
}
