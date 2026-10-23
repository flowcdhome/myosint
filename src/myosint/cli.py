import argparse
import re
import sys
from rich.console import Console

from . import __version__
from .username import check_username
from .username_all import check_username_all, update_db
from .email_check import check_email
from .updater import check_update

console = Console()
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def detect(target):
    return "email" if EMAIL_RE.match(target) else "user"


def build_parser():
    p = argparse.ArgumentParser(
        prog="myosint",
        description="myosint - мини OSINT-инструмент (только открытые данные)",
        add_help=False,
        allow_abbrev=False,
    )
    p.add_argument("-help", "-h", "--help", action="help", help="показать справку")
    p.add_argument("-user", metavar="NICK", help="поиск по нику")
    p.add_argument("-m", metavar="EMAIL", help="проверка email")
    p.add_argument("-at", metavar="TARGET", help="автоопределение (ник или email)")
    p.add_argument("-u", action="store_true", help="проверить обновления на GitHub")
    p.add_argument("-all", action="store_true", help="с -user: проверить 600+ сайтов (WhatsMyName)")
    p.add_argument("-db", action="store_true", help="обновить базу сайтов")
    p.add_argument("-nsfw", action="store_true", help="с -all: включить NSFW-сайты")
    p.add_argument("-v", "--version", action="version", version=f"myosint {__version__}")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not any([args.user, args.m, args.at, args.u, args.db]):
        parser.print_help()
        sys.exit(0)

    if args.u:
        check_update(console)

    if args.db:
        update_db(console)

    if args.at:
        kind = detect(args.at)
        console.print(f"[cyan]Определено как:[/] {kind}")
        (check_email if kind == "email" else check_username)(args.at, console)

    if args.user:
        if args.all:
            check_username_all(args.user, console, nsfw=args.nsfw)
        else:
            check_username(args.user, console)

    if args.m:
        check_email(args.m, console)


if __name__ == "__main__":
    main()
