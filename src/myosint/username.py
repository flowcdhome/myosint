import requests
from concurrent.futures import ThreadPoolExecutor

SITES = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Dev.to": "https://dev.to/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
}
HEADERS = {"User-Agent": "Mozilla/5.0 (myosint)"}


def _check(item, username):
    name, tpl = item
    url = tpl.format(username)
    try:
        r = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        return name, url, r.status_code == 200
    except requests.RequestException:
        return name, url, None


def check_username(username, console):
    console.print(f"[bold]Поиск ника:[/] {username}")
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(lambda i: _check(i, username), SITES.items()))
    for name, url, found in results:
        if found is None:
            console.print(f"[yellow]? {name}: ошибка запроса[/]")
        elif found:
            console.print(f"[green]+ {name}:[/] {url}")
        else:
            console.print(f"[red]- {name}[/]")
