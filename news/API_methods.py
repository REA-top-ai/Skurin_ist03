import requests as r
import json


def get_everything(endpoint: str,
                   apikey: str,
                   params: dict[str]) -> dict[str, str]:
    final_params = {key: value for key, value in params.items() if value is not None}
    return _make_request('everything', apikey, final_params)


base_url = 'https://newsapi.org/v2'


def _make_request(endpoint: str, api_key: str, params: dict = None) -> dict:
    url = f'{base_url}/{endpoint}'
    default_params = {'apikey': api_key}

    if params:
        default_params.update(params)  # если есть параметры, то добавляет к api

    try:
        response = r.get(url, params=default_params, timeout=10)
        return response.json()  # переробатывает в строку 
    except r.exceptions.RequestException as e:
        raise Exception(f"Ошибка обращения к newsAPI ({endpoint}: {e}, {default_params})")
    except ValueError as e:
        raise Exception(f"Ошибка парсинга json ({endpoint}: {e})")

def summarize_with_mistral(api_key: str, articles: list[dict]) -> str:
    url = "https://api.mistral.ai/v1/chat/completions"
    articles_text = ''
    for i, article in enumerate(articles[:10],1):
        articles_text += f"{i}. {article.get('title')} - {article.get('description')}\n"

    prompt = f"""
Ты аналитик новостей. Сделай аннотацию (250-300 слов) на русском языке
по этим статьям за последний день. Добавь оценку ситуации и общий вывод..

{articles_text}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = r.post(url, headers=headers, json=data)

    return response.json()["choices"][0]["message"]["content"]