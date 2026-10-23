# myosint

[🇬🇧 English](README.md) | 🇷🇺 Русский

Небольшой OSINT-инструмент для командной строки, работающий **только с открытыми данными**.

## Возможности

- Поиск ника на нескольких открытых сайтах
- Проверка email: MX-записи и профиль Gravatar
- Автоопределение типа цели (ник или email)
- Проверка обновлений через GitHub Releases

## Установка

Рекомендуется (изолированная установка через pipx):

```bash
pipx install git+https://github.com/flowcdhome/myosint.git
```

Или через pip в виртуальном окружении:

```bash
python -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/flowcdhome/myosint.git
```

Для Arch Linux сначала нужны пакеты:

```bash
sudo pacman -S --needed git python python-pipx
```

Зависимости (`requests`, `rich`, `packaging`, `dnspython`) ставятся автоматически.

## Использование

```bash
myosint -help                  # справка
myosint -user johndoe          # поиск ника
myosint -m user@example.com    # проверка email
myosint -at johndoe            # автоопределение: ник или email
myosint -at user@example.com
myosint -u                     # проверить обновления на GitHub
myosint -v                     # версия
```

Флаги можно комбинировать: `myosint -user johndoe -u`

| Флаг | Описание |
|------|----------|
| `-user NICK` | Поиск ника на открытых сайтах |
| `-m EMAIL` | Проверка email (MX-записи, Gravatar) |
| `-at TARGET` | Автоопределение типа цели и запуск нужной проверки |
| `-u` | Проверить, есть ли новый релиз на GitHub |
| `-v`, `--version` | Показать версию |
| `-help`, `-h`, `--help` | Справка |

## Обновление

```bash
myosint -u
pipx upgrade myosint
```

## Ограничения

- Проверка ника основана на HTTP-статусе, поэтому возможны ложные срабатывания и пропуски (часть сайтов отдаёт 200 на любую страницу или блокирует ботов).
- Найденная MX-запись или Gravatar не доказывают, что почтовый ящик существует.

## Правовое уведомление

Используй инструмент только с данными, к которым у тебя законный доступ, соблюдай правила сайтов и законы своей страны. Автор не отвечает за неправомерное использование.

## Лицензия

MIT, см. [LICENSE](LICENSE).
