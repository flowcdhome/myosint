import hashlib
import dns.resolver
import requests

DOH = [
    ("https://cloudflare-dns.com/dns-query", {"accept": "application/dns-json"}),
    ("https://dns.google/resolve", {}),
]


def _mx_system(domain):
    res = dns.resolver.Resolver()
    res.lifetime = 5
    try:
        ans = res.resolve(domain, "MX")
        return [str(r.exchange).rstrip(".") for r in sorted(ans, key=lambda r: r.preference)]
    except dns.resolver.NXDOMAIN:
        raise
    except Exception:
        return []


def _mx_doh(domain):
    for url, headers in DOH:
        try:
            r = requests.get(url, params={"name": domain, "type": "MX"},
                             headers=headers, timeout=8)
            data = r.json()
        except Exception:
            continue
        if data.get("Status") == 3:
            raise dns.resolver.NXDOMAIN()
        answers = [a for a in data.get("Answer", []) if a.get("type") == 15]
        if answers:
            answers.sort(key=lambda a: int(a["data"].split()[0]))
            return [a["data"].split()[1].rstrip(".") for a in answers]
    return []


def _lookup_mx(domain):
    try:
        hosts = _mx_system(domain)
        if hosts:
            return hosts, "системный DNS"
        hosts = _mx_doh(domain)
        if hosts:
            return hosts, "DNS-over-HTTPS"
    except dns.resolver.NXDOMAIN:
        return None, "домен не существует"
    return None, "нет MX-записей или DNS недоступен (VPN/фильтрация?)"


def check_email(email, console):
    console.print(f"[bold]Проверка email:[/] {email}")
    domain = email.partition("@")[2]

    hosts, info = _lookup_mx(domain)
    if hosts:
        console.print(f"[green]+ MX найден[/] ({info}): {', '.join(hosts)}")
    else:
        console.print(f"[red]- MX не найден:[/] {info}")

    h = hashlib.md5(email.strip().lower().encode()).hexdigest()
    try:
        r = requests.get(f"https://www.gravatar.com/avatar/{h}?d=404", timeout=8)
        if r.status_code == 200:
            console.print(f"[green]+ Gravatar найден:[/] https://gravatar.com/{h}")
        else:
            console.print("[red]- Gravatar не найден[/]")
    except requests.RequestException:
        console.print("[yellow]? Gravatar: ошибка запроса[/]")
