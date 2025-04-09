from bs4 import BeautifulSoup


def detect_protest_page(html, protest_keywords):
    html = html.lower()
    return any(kw in html for kw in protest_keywords)


def detect_av_indicators(text, age_keywords):
    matched_snippets = []
    for keyword in age_keywords:
        if keyword in text:
            start = text.find(keyword)
            snippet = text[max(0, start - 50): start + len(keyword) + 50]
            matched_snippets.append(snippet.strip())
    return matched_snippets


def detect_providers(text, providers):
    return [p for p in providers if p.lower() in text]
