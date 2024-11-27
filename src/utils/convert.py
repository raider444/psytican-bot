import re
from datetime import date as _date

ERA = 2000
DATE_PATTERN = r"(\d{1,2})(?:\.|\/)(\d{1,2})(?:(?:\.|\/?)((?:\d{2}){1,2}))?"


class Convert:
    @staticmethod
    def camelcase_snakecase(value: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()

    @staticmethod
    def camelcase_kebabcase(value: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "-", value).lower()

    @staticmethod
    def snakecase_camelcase_upper(value):
        return value.title().replace("_", "")

    @staticmethod
    def snakecase_camelcase_lower(value):
        return value[0].lower() + Convert.snakecase_camelcase_upper(value)[1:]


class DateParser:
    @staticmethod
    def parse_date(date):
        regex = re.compile(DATE_PATTERN)
        if not regex.match(date):
            raise ValueError(f'Date "{date}" does not match pattern')
        parsed_date = regex.findall(date)[0]
        day, month, year = parsed_date
        if not year:
            year = _date.today().year
        if len(str(year)) == 2:
            year = int(year) + ERA
        print(f"{day=}, {month=}, {year=}")
        return _date(year=int(year), month=int(month), day=int(day))
