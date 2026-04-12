from API_methods import get_everything, summarize_with_mistral

topic = ("погода в москве")   #о чем писать
if __name__ =='__main__':
    result = get_everything('everything','1b48faa621944374aa3aa1eb5966422d',{'q':topic})
    articles = result.get("articles", [])

    text = summarize_with_mistral('TeysC5oIWemkrSK9QKCet9WVUb8b64C8', articles)

    with open("../../text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open("../../text.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print(content)