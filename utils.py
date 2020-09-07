import os


def file_access(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def year_from_date(date):
    return str(date.split('-')[0])