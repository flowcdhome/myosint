<div align="center">

# 🔎 myosint

**Lightweight OSINT CLI: usernames, emails, 600+ sites. Public data only.**

🇬🇧 English · [🇷🇺 Русский](README.ru.md)

[![Release](https://img.shields.io/github/v/release/flowcdhome/myosint?style=for-the-badge&color=2ea44f)](https://github.com/flowcdhome/myosint/releases)
[![License](https://img.shields.io/github/license/flowcdhome/myosint?style=for-the-badge)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Linux-informational?style=for-the-badge&logo=linux&logoColor=white)

</div>

---

## ✨ Features

| | |
|---|---|
| ⚡ **Fast mode** | Curated list of reliable sites, no false positives |
| 🌐 **`-all` mode** | 600+ sites via the [WhatsMyName](https://github.com/WebBreacher/WhatsMyName) database |
| 📧 **Email checks** | MX records (DNS-over-HTTPS fallback, works behind VPN) and Gravatar |
| 🤖 **Auto-detect** | `-at` decides whether the target is a username or an email |
| 🔄 **Self-update check** | `-u` compares your version with the latest GitHub release |

## 🚀 Quick start

```bash
# 1. Install pipx (Arch; Ubuntu/Debian: sudo apt install git python3 pipx)
sudo pacman -S --needed git python python-pipx
pipx ensurepath            # then open a new terminal

# 2. Install myosint
pipx install git+https://github.com/flowcdhome/myosint.git

# 3. Run
myosint -user johndoe
```

## 📖 Usage

```bash
myosint -user johndoe             # curated sites (fast)
myosint -db                       # download the 600+ site database (once)
myosint -user johndoe -all        # 600+ sites
myosint -user johndoe -all -nsfw  # include adult sites
myosint -m user@example.com       # email check
myosint -at johndoe               # auto-detect username / email
myosint -u                        # check for updates
```

<details>
<summary><b>All flags</b></summary>

| Flag | Description |
|------|-------------|
| `-user NICK` | Search a username on curated public sites |
| `-all` | With `-user`: check 600+ sites |
| `-nsfw` | With `-all`: include adult sites (hidden by default) |
| `-db` | Download / update the site database |
| `-m EMAIL` | Check an email (MX, Gravatar) |
| `-at TARGET` | Auto-detect the target type |
| `-u` | Check GitHub for a newer release |
| `-v`, `--version` | Show version |
| `-help`, `-h`, `--help` | Show help |

</details>

## 🖥️ Example

```text
$ myosint -user torvalds
Поиск ника: torvalds
+ GitHub: https://github.com/torvalds
+ GitLab: https://gitlab.com/torvalds
+ Codeberg: https://codeberg.org/torvalds
- Dev.to: не найден
+ Docker Hub: https://hub.docker.com/u/torvalds
? Reddit: неясно (ответ 403, возможно блокировка)
```

**How to read it:** 🟢 `+` profile exists (does *not* prove it is the person you want) · 🔴 `-` not found · 🟡 `?` blocked or no answer.

## 🔄 Updating

```bash
myosint -u
pipx upgrade myosint
```

## ⚠️ Limitations

- Many sites block bots or are unreachable via VPN, such results show as unknown.
- A found MX record or Gravatar does not prove a mailbox exists.
- Matches rely on site signatures and may include false positives, verify manually.

## ⚖️ Legal

Use only on data you are legally allowed to access, and respect site terms and applicable laws. The author is not responsible for misuse.

## 🙏 Credits

Site signatures for `-all` come from [WhatsMyName](https://github.com/WebBreacher/WhatsMyName) (CC BY-SA 4.0). The database is downloaded on the user's machine and is not bundled here.

## 📄 License

MIT, see [LICENSE](LICENSE).
