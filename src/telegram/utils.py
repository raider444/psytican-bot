import datetime


def separate_callback_data(data):
    """Separate the callback data"""
    return data.split(";")


def format_calndar_date(date):
    formatted_date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    return formatted_date
