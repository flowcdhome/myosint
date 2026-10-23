import requests
from packaging.version import Version
from . import __version__

REPO = "flowcdhome/myosint"


def check_update(console):
    console.print(f"[bold]Текущая версия:[/] {__version__}")
    try:
        r = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest", timeout=8)
        if r.status_code == 404:
            console.print("[yellow]На GitHub пока нет релизов[/]")
            return
        r.raise_for_status()
        latest = r.json()["tag_name"].lstrip("v")
        if Version(latest) > Version(__version__):
            console.print(f"[green]Доступна новая версия: {latest}[/]")
            console.print(f"Обновить: [cyan]pipx upgrade myosint[/]")
        else:
            console.print("[green]У тебя последняя версия[/]")
    except Exception as e:
        console.print(f"[yellow]Не удалось проверить обновления: {e}[/]")
