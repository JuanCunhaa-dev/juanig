# Install juanig for this computer

Paste this whole file to your coding AI (Cursor, Claude, Copilot, Windsurf, Cline, Continue, or similar).

## What you must do

Install the **juanig** CLI on this machine and configure the skill for the current AI/IDE. After that, any Instagram post URL the user gives you can be downloaded with `juanig` into the project assets folder.

Repo: https://github.com/Juancunhaa-dev/juanig  
Latest release: https://github.com/Juancunhaa-dev/juanig/releases/latest

## Steps

1. Detect the OS and the current IDE.
2. Install the CLI:
   - Prefer npm if Node is available:
     ```bash
     npm i -g github:JuanCunhaa-dev/juanig
     ```
     or, after the package is on npm: `npm i -g juanig`
   - **Windows:** if npm is not available, run this in PowerShell, then use a new terminal:
     ```powershell
     irm https://github.com/Juancunhaa-dev/juanig/releases/latest/download/install.ps1 | iex
     ```
     Do not download or run `juanig.exe`.
   - **macOS / Linux:**
     ```bash
     curl -fsSL https://raw.githubusercontent.com/Juancunhaa-dev/juanig/main/installer/install.sh | bash
     ```
3. Write the skill file from the repo (`juanig/data/SKILL.md`) into every relevant folder that exists:
   - Cursor: `~/.cursor/skills/juanig/SKILL.md`
   - Claude Code: `~/.claude/skills/juanig/SKILL.md`
   - Windsurf: `~/.codeium/windsurf/skills/juanig/SKILL.md`
   - Continue: `~/.continue/skills/juanig/SKILL.md`
   - Current project, if those folders exist: `.cursor/skills/juanig/SKILL.md`, `.claude/skills/juanig/SKILL.md`
   Running `juanig --install-skills` does this.
4. Verify:
   ```bash
   juanig --help
   ```
5. Tell the user it is ready. Next time they can say:
   `using juanig, download these Instagram posts into public/images` plus the URLs.

## How to download after install

```bash
juanig "https://www.instagram.com/p/SHORTCODE/" -o public/images --json
```

- Do not start a Python server
- Do not rebuild an Instagram scraper
- Always use the `juanig` command
- Default folder if the user does not choose: the user Downloads directory
- Files are anonymous: `photo.jpg`, `photo_2.jpg`, `video.mp4` — no profile names
- Never commit `JUANIG_SESSIONID` or cookies
