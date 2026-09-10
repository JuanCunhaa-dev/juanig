# juanig

CLI that downloads Instagram photos, carousels, videos, and Reels from a link. Built for building websites with real images.

```bash
juanig "https://www.instagram.com/p/DRH53C9EYV4/" -o public/images
```

By default files go to your **Downloads** folder as `photo.jpg` / `video.mp4`, with no profile names. No web server. Windows install uses Python plus a `.cmd` launcher, so Smart App Control does not block an unsigned `.exe`.

Portuguese guide: [README.pt-BR.md](README.pt-BR.md)  
Give this file to an AI: [AI-SETUP.md](AI-SETUP.md)

## Install

### Windows (recommended)

In PowerShell:

```powershell
irm https://github.com/Juancunhaa-dev/juanig/releases/latest/download/install.ps1 | iex
```

That installs Python if needed, then puts a `juanig.cmd` on PATH. Open a new terminal afterwards. Do not download `juanig.exe` — Windows blocks unsigned executables.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/Juancunhaa-dev/juanig/main/installer/install.sh | bash
```

### From source

```bash
pip install git+https://github.com/Juancunhaa-dev/juanig.git
juanig --install-skills
```

`--setup` / `--install-skills` copies the skill only into IDEs that are already installed (the app folder already exists). It will not create Claude/Windsurf/Continue folders just because you have Cursor.

## CLI

```text
juanig [URL ...] [options]
```

| Argument | Description |
|---|---|
| `URL` | One or more Instagram post, carousel, or Reel links |
| `-o`, `--output` | Destination folder. Default: the user `Downloads` folder |
| `--json` | Print JSON with saved paths (best for agents) |
| `--sessionid` | Instagram `sessionid` cookie for private/restricted posts |
| `--setup` | Install the exe on PATH and write AI skills |
| `--install-skills` | Only write the skill files |
| `-h`, `--help` | Show help |

Environment variables: `JUANIG_OUTPUT`, `JUANIG_SESSIONID`.

### Examples

```bash
juanig "https://www.instagram.com/p/AAAA/"
juanig "https://www.instagram.com/p/AAAA/" "https://www.instagram.com/reel/BBBB/" -o public/images --json
```

### Output

Default:

```text
1 file(s)
  C:\Users\you\Downloads\photo.jpg
```

`--json`:

```json
{
  "ok": true,
  "output": "C:\\Users\\you\\Downloads",
  "posts": [{ "files": ["C:\\Users\\you\\Downloads\\photo.jpg"] }],
  "errors": []
}
```

## Use with an AI

Send [AI-SETUP.md](AI-SETUP.md) to Cursor, Claude, Copilot, Windsurf, or any coding agent. Ask it to install juanig and then download the posts you need.

```text
Read AI-SETUP.md, install juanig, then download these posts into public/images:
https://www.instagram.com/p/AAAA/
```

## Notes

- Public posts only, unless you pass a `sessionid`
- Instagram can rate-limit anonymous access
- CDN URLs expire; juanig downloads the file immediately
- Never commit cookies

## License

MIT
