import json
from collections import defaultdict


logs = [
    "2025-02-01 10:15:33|INFO|user=anna action=login status=success ip=10.0.0.1",
    "2025-02-01 10:17:10|ERROR|user=bob action=payment status=fail amount=120",
    "2025-02-01 10:20:01|INFO|user=anna action=logout status=success",
    "2025-02-01 10:22:45|WARNING|user=anna action=payment status=fail amount=300",
    "2025-02-01 10:30:12|ERROR|user=tom action=login status=fail ip=10.0.0.5"
]


def parsing(stroka):
    parts = stroka.split("|")
    date = parts[0]
    level = parts[1] #проверить длину списка на предмет ошибки out of range
    message = parts[2]

    result = {
        "date": date,
        "level": level
    }

    for field in message.split():
        key, value = field.split("=")
        if value.isdigit():
            result[key] = int(value)
        else:
            result[key] = value

    return result


def json_parsing(logs, q='n'):
    parsed = [parsing(line) for line in logs]

    if q == 'y':
        with open("logs.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=4, ensure_ascii=False)

    return parsed


def filter_logs(logs, **filters):
    return [
        log for log in logs
        if all(log.get(key) == value for key, value in filters.items())
    ]


def countering_yo(logs):
    count_by_level = defaultdict(int)
    count_by_user = defaultdict(int)
    failed_payment_sum = 0

    for log in logs:
        if "level" in log:
            count_by_level[log["level"]] += 1

        if "user" in log:
            count_by_user[log["user"]] += 1

        if log.get("action") == "payment" and log.get("status") == "fail":
            failed_payment_sum += log.get("amount", 0)

    return {
        "count_by_level": dict(count_by_level),
        "count_by_user": dict(count_by_user),
        "failed_payment_sum": failed_payment_sum
    }


if __name__ == "__main__":
    parsed_logs = json_parsing(logs)

    print(filter_logs(parsed_logs, status="fail"))
    print(filter_logs(parsed_logs, level="ERROR"))
    print(filter_logs(parsed_logs, user="anna", action="payment"))
    print(countering_yo(parsed_logs))