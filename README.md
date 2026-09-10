# juanig

CLI that downloads Instagram photos, carousels, videos, and Reels from a link. Built for building websites with real images.

```bash
juanig "https://www.instagram.com/p/DRH53C9EYV4/" -o public/images
```

Saves to `public/images/username/file.jpg`. No web server. Windows install uses Python plus a `.cmd` launcher, so Smart App Control does not block an unsigned `.exe`.

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

`--setup` / `--install-skills` copies the skill into Cursor, Claude Code, Windsurf, Continue, and similar folders when they exist.

## CLI

```text
juanig [URL ...] [options]
```

| Argument | Description |
|---|---|
| `URL` | One or more Instagram post, carousel, or Reel links |
| `-o`, `--output` | Base folder. Each profile gets a subfolder. Default: `./downloads` |
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
barbeariaemilio · DRH53C9EYV4 · 1 file(s)
  C:\site\public\images\barbeariaemilio\barbeariaemilio_DRH53C9EYV4_01.jpg
```

`--json`:

```json
{
  "ok": true,
  "output": "C:\\site\\public\\images",
  "posts": [{ "username": "barbeariaemilio", "files": ["...jpg"] }],
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
