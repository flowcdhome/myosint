# myosint

🇬🇧 English | [🇷🇺 Русский](README.ru.md)

A small OSINT command-line tool that works with **publicly available data only**.

## Features

- Username lookup across several public sites
- Email checks: MX records and Gravatar profile
- Auto-detection of the target type (username or email)
- Update check against GitHub Releases

## Installation

Recommended (isolated install with pipx):

```bash
pipx install git+https://github.com/flowcdhome/myosint.git
```

Or with pip inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/flowcdhome/myosint.git
```

Arch Linux prerequisites:

```bash
sudo pacman -S --needed git python python-pipx
```

Dependencies (`requests`, `rich`, `packaging`, `dnspython`) are installed automatically.

## Usage

```bash
myosint -help                  # show help
myosint -user johndoe          # search a username
myosint -m user@example.com    # check an email
myosint -at johndoe            # auto-detect: username or email
myosint -at user@example.com
myosint -u                     # check for updates on GitHub
myosint -v                     # show version
```

Flags can be combined: `myosint -user johndoe -u`

| Flag | Description |
|------|-------------|
| `-user NICK` | Search a username on public sites |
| `-m EMAIL` | Check an email (MX records, Gravatar) |
| `-at TARGET` | Auto-detect the target type and run the matching check |
| `-u` | Check GitHub for a newer release |
| `-v`, `--version` | Show the version |
| `-help`, `-h`, `--help` | Show help |

## Updating

```bash
myosint -u
pipx upgrade myosint
```

## Limitations

- A username check is based on the HTTP status code, so false positives and false negatives are possible (some sites return 200 for any page or block bots).
- A found MX record or Gravatar does not prove that a mailbox exists.

## Legal notice

Use this tool only on data you are legally allowed to access, and respect the terms of service of the sites involved and applicable laws. The author is not responsible for misuse.

## License

MIT, see [LICENSE](LICENSE).

## Credits

Site signatures for `-all` come from [WhatsMyName](https://github.com/WebBreacher/WhatsMyName) (CC BY-SA 4.0). Use `-nsfw` to include adult sites.
