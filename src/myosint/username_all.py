import json
import requests
from pathlib import Path
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress

DB_URL = "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
CACHE = Path.home() / ".cache" / "myosint" / "wmn-data.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) myosint"}


def update_db(console):
    console.print("[cyan]Скачиваю базу сайтов WhatsMyName...[/]")
    try:
        r = requests.get(DB_URL, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        console.print(f"[red]Не удалось скачать базу: {e}[/]")
        return None
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(data), encoding="utf-8")
    console.print(f"[green]База сохранена:[/] {len(data.get('sites', []))} сайтов")
    return data


def load_db(console):
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except ValueError:
            pass
    return update_db(console)


def _check(site, nick):
    name = site["name"]
    url = site["uri_check"].replace("{account}", quote(nick, safe=""))
    shown = (site.get("uri_pretty") or site["uri_check"]).replace(
        "{account}", quote(nick, safe=""))
    cat = site.get("cat", "")
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
    except requests.RequestException:
        return name, shown, cat, "unknown"
    text = r.text
    e_code, m_code = site.get("e_code"), site.get("m_code")
    e_str, m_str = site.get("e_string") or "", site.get("m_string") or ""

    if m_str and m_str in text:
        return name, shown, cat, "missing"
    if m_code is not None and r.status_code == m_code and r.status_code != e_code:
        return name, shown, cat, "missing"
    if r.status_code == e_code and (not e_str or e_str in text):
        return name, shown, cat, "found"
    if r.status_code == 404:
        return name, shown, cat, "missing"
    return name, shown, cat, "unknown"


def check_username_all(nick, console, nsfw=False):
    data = load_db(console)
    if not data:
        return
    # сайты с POST-запросами пока пропускаем
    sites = [s for s in data.get("sites", [])
             if "uri_check" in s and not s.get("post_body")
             and (nsfw or "NSFW" not in s.get("cat", ""))]
    console.print(f"[bold]Поиск ника:[/] {nick} [dim]({len(sites)} сайтов)[/]")

    found, unknown = [], 0
    with Progress(console=console, transient=True) as progress:
        task = progress.add_task("Проверка", total=len(sites))
        with ThreadPoolExecutor(max_workers=30) as ex:
            futures = [ex.submit(_check, s, nick) for s in sites]
            for f in as_completed(futures):
                name, shown, cat, state = f.result()
                if state == "found":
                    found.append((name, shown, cat))
                elif state == "unknown":
                    unknown += 1
                progress.advance(task)

    for name, shown, cat in sorted(found):
        console.print(f"[green]+ {name}[/] [dim]({cat})[/]: {shown}")
    console.print(
        f"\n[bold]Найдено: {len(found)}[/] | неясно/блокировка: {unknown} "
        f"| не найдено: {len(sites) - len(found) - unknown}"
    )
    console.print("[dim]Результаты могут содержать ложные срабатывания, "
                  "проверяй ссылки вручную.[/]")
