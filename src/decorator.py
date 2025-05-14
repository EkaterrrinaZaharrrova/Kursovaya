import json
from functools import wraps
from typing import Any

from loggers import get_logger

logger = get_logger()


def log(filename: Any = None) -> Any:
    """Запись логов в файл, если имя не указано создаётся информационный файл
    not_specified_name_to_logs"""
    logger.info("Запуск декоратора.")

    def decorator_log(function: Any) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = ""
            if not filename:
                write_to_log = (
                    "\nВы не указали имя файла для записи логов.\n"
                    "Укажите имя файла и попробуйте ещё раз!\n"
                )
                with open("not_specified_name_to_logs.logs", mode="a", encoding="utf-8") as file:
                    file.write(write_to_log)
                    return result

            result = function(*args, **kwargs)
            dt_excel = result.to_dict("records")
            result = json.dumps(dt_excel, default=str, ensure_ascii=False)
            write_to_log = f"\nРезультат работы функции {function.__name__}\n{result}"
            with open(filename, mode="a", encoding="utf-8") as file:
                file.write(write_to_log)
            return result

        return wrapper

    return decorator_log