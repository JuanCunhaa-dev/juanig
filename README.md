# juanig

CLI that downloads Instagram photos, carousels, videos, and Reels from a link. Built for building websites with real images.

```bash
juanig "https://www.instagram.com/p/DRH53C9EYV4/" -o public/images
```

By default files go to your **Downloads** folder as `photo.jpg` / `video.mp4`, with no profile names. No web server. Windows install uses Python plus a `.cmd` launcher, so Smart App Control does not block an unsigned `.exe`.

Portuguese guide: [README.pt-BR.md](README.pt-BR.md)  
Give this file to an AI: [AI-SETUP.md](AI-SETUP.md)

## Install

Needs **Python 3**. Node is optional and only used for `npm i -g`.

### npm

```bash
npm i -g juanig
```

Until the package is on the npm registry, use GitHub:

```bash
npm i -g github:JuanCunhaa-dev/juanig
```

That runs `pip install` under the hood and puts `juanig` on PATH.

### Windows (PowerShell)

```powershell
irm https://github.com/Juancunhaa-dev/juanig/releases/latest/download/install.ps1 | iex
```

### pip / source

```bash
pip install git+https://github.com/Juancunhaa-dev/juanig.git
juanig --setup
```

Upgrade later with `juanig --update`.

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
| `--setup` | Put juanig on PATH and write AI skills for installed IDEs |
| `--install-skills` | Only write the skill files for installed IDEs |
| `--update` | Upgrade to the latest GitHub version |
| `-V`, `--version` | Print the installed version |
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
- Private or gated posts need `--sessionid` / `JUANIG_SESSIONID`
- Instagram can rate-limit anonymous access
- CDN URLs expire; juanig downloads the file immediately
- Never commit cookies

## Disclaimer

juanig is unofficial and is not affiliated with Meta or Instagram. Use it for personal, lawful downloads of public media or content you have rights to (for example, assets for a site you are building). Respect Instagram's terms and copyright. Do not use it to scrape at scale.

## License

MIT
