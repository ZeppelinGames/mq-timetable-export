
import sys
import pyppeteer
import asyncio

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path as op
    path = op.realpath(op.abspath(__file__))
    sys.path.insert(0, op.dirname(op.dirname(path)))

async def main():
    import argparse
    from getpass import getpass

    import estudent

    exporters_reg = estudent.exporters.exporters_reg
    exporters_list = list(exporters_reg)
    desc = f'format: {{{",".join(exporters_list)}}}'

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-u', dest='username', help='your student ID')
    parser.add_argument('-p', dest='password', help='your eStudent password')
    parser.add_argument('-o', dest='output', help='the output file')
    parser.add_argument('format', default='console', const='all',
            nargs='?', choices=exporters_list, metavar='format')

    args = parser.parse_args()

    username = args.username
    if username is None:
        username = input('Username: ')

    password = args.password
    if password is None:
        password = getpass('Password: ')

    exporter_name = args.format
    exporter = exporters_reg[exporter_name]()
    b = await pyppeteer.launch(headless=True)

    client = estudent.Client(b)
    await client.login(username, password)
    my_classes_page = await client.fetch_my_classes_page()
    timetable_resources = my_classes_page.timetable()
    study_period = timetable_resources.study_period()

    output = args.output
    if output is None:
        exporter.dump(study_period, sys.stdout)
    else:
        with open(output, 'w') as fh:
            exporter.dump(study_period, fh)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    #main()
