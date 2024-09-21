import re


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
