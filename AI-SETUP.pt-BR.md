# Instalar o juanig neste computador

Cole este arquivo inteiro na sua IA de código (Cursor, Claude, Copilot, Windsurf, Cline, Continue ou similar).

## O que você precisa fazer

Instalar a CLI **juanig** nesta máquina e configurar a skill no IDE/IA atual. Depois disso, qualquer link de post do Instagram que a pessoa mandar pode ser baixado com `juanig` na pasta de assets do projeto.

Repositório: https://github.com/Juancunhaa-dev/juanig  
Release mais recente: https://github.com/Juancunhaa-dev/juanig/releases/latest

## Passos

1. Detecte o sistema operacional e o IDE atual.
2. Instale a CLI:
   - Prefira pip:
     ```bash
     pip install juanig
     juanig --setup
     ```
   - Ou npm se o Node existir:
     ```bash
     npm i -g juanig
     ```
   - **Windows:** se não tiver npm, rode no PowerShell e abra um terminal novo:
     ```powershell
     irm https://github.com/Juancunhaa-dev/juanig/releases/latest/download/install.ps1 | iex
     ```
     Não baixe nem execute `juanig.exe`.
   - **macOS / Linux:**
     ```bash
     curl -fsSL https://raw.githubusercontent.com/Juancunhaa-dev/juanig/main/installer/install.sh | bash
     ```
3. Grave o arquivo da skill do repositório (`juanig/data/SKILL.md`) em toda pasta relevante que existir:
   - Cursor: `~/.cursor/skills/juanig/SKILL.md`
   - Claude Code: `~/.claude/skills/juanig/SKILL.md`
   - Windsurf: `~/.codeium/windsurf/skills/juanig/SKILL.md`
   - Continue: `~/.continue/skills/juanig/SKILL.md`
   - Projeto atual, se essas pastas existirem: `.cursor/skills/juanig/SKILL.md`, `.claude/skills/juanig/SKILL.md`
   O comando `juanig --install-skills` faz isso.
4. Confira:
   ```bash
   juanig --version
   juanig --help
   ```
5. Avise que está pronto. Da próxima vez a pessoa pode falar:
   `usando o juanig, baixa esses posts do Instagram em public/images` e mandar os links.

## Como baixar depois de instalado

```bash
juanig "https://www.instagram.com/p/SHORTCODE/" -o public/images --json
```

- Não suba servidor Python
- Não recrie um scraper do Instagram
- Sempre use o comando `juanig`
- Pasta padrão se a pessoa não escolher: a pasta Downloads do usuário
- Arquivos anônimos: `photo.jpg`, `photo_2.jpg`, `video.mp4` — sem nome de perfil
- Nunca commite `JUANIG_SESSIONID` nem cookies
