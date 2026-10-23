import hashlib
import dns.resolver
import requests


def check_email(email, console):
    console.print(f"[bold]Проверка email:[/] {email}")
    domain = email.partition("@")[2]

    try:
        mx = dns.resolver.resolve(domain, "MX")
        hosts = ", ".join(str(r.exchange).rstrip(".") for r in mx)
        console.print(f"[green]+ MX найден:[/] {hosts}")
    except Exception:
        console.print("[red]- MX не найден[/]")

    h = hashlib.md5(email.strip().lower().encode()).hexdigest()
    try:
        r = requests.get(f"https://www.gravatar.com/avatar/{h}?d=404", timeout=8)
        if r.status_code == 200:
            console.print(f"[green]+ Gravatar найден:[/] https://gravatar.com/{h}")
        else:
            console.print("[red]- Gravatar не найден[/]")
    except requests.RequestException:
        console.print("[yellow]? Gravatar: ошибка запроса[/]")
