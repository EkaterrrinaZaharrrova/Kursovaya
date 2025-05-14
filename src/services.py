import json

from loggers import get_logger

logger = get_logger()


def simple_search(transactions: list[dict], find_word: str) -> str:
    """Простой поиск. Возвращает JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    logger.info("Запуск")

    result_search = []

    for i in transactions:
        if i.get("description") == find_word:
            result_search.append(i)

    return json.dumps(result_search, ensure_ascii=False)