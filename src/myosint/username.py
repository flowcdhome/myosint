import requests
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) myosint/0.1"}

# name: (адрес проверки, тип проверки, ссылка для показа или None)
# status - 200 найден, 404 не найден; json_list - API вернул непустой список;
# hn - Hacker News API вернул не null
SITES = {
    "GitHub":      ("https://github.com/{}", "status", None),
    "GitLab":      ("https://gitlab.com/{}", "redirect", None),
    "Codeberg":    ("https://codeberg.org/{}", "status", None),
    "Dev.to":      ("https://dev.to/{}", "status", None),
    "Docker Hub":  ("https://hub.docker.com/v2/users/{}/", "status",
                    "https://hub.docker.com/u/{}"),
    "Hacker News": ("https://hacker-news.firebaseio.com/v0/user/{}.json", "hn",
                    "https://news.ycombinator.com/user?id={}"),
    "Lichess":     ("https://lichess.org/api/user/{}", "status",
                    "https://lichess.org/@/{}"),
    "Chess.com":   ("https://api.chess.com/pub/player/{}", "status",
                    "https://www.chess.com/member/{}"),
    "Reddit":      ("https://www.reddit.com/user/{}/about.json", "status",
                    "https://www.reddit.com/user/{}"),
}


def _check(item, username):
    name, (tpl, kind, shown_tpl) = item
    nick = quote(username, safe="")
    url = tpl.format(nick)
    shown = (shown_tpl or tpl).format(nick)
    try:
        r = requests.get(url, headers=HEADERS, timeout=8,
                         allow_redirects=(kind != "redirect"))
    except requests.RequestException as e:
        return name, shown, "unknown", type(e).__name__
    if kind == "redirect":
        if r.status_code == 200:
            return name, shown, "found", 200
        if r.status_code in (301, 302, 303):
            return name, shown, "missing", r.status_code
        return name, shown, "unknown", r.status_code
    if r.status_code == 404:
        return name, shown, "missing", 404
    if r.status_code != 200:
        return name, shown, "unknown", r.status_code
    if kind == "status":
        return name, shown, "found", 200
    try:
        data = r.json()
    except ValueError:
        return name, shown, "unknown", "не JSON"
    if kind == "json_list":
        return name, shown, ("found" if data else "missing"), 200
    if kind == "hn":
        return name, shown, ("found" if data else "missing"), 200
    return name, shown, "unknown", "?"


def check_username(username, console):
    console.print(f"[bold]Поиск ника:[/] {username}")
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(lambda i: _check(i, username), SITES.items()))
    for name, url, state, code in results:
        if state == "found":
            console.print(f"[green]+ {name}:[/] {url}")
        elif state == "missing":
            console.print(f"[red]- {name}: не найден[/]")
        else:
            console.print(f"[yellow]? {name}: неясно (ответ {code}, возможно блокировка)[/]")
