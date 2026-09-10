# Instalar o juanig neste computador

Cole este arquivo inteiro na sua IA de código (Cursor, Claude, Copilot, Windsurf, Cline, Continue ou similar).

## O que você precisa fazer

Instalar a CLI **juanig** nesta máquina e configurar a skill no IDE/IA atual. Depois disso, qualquer link de post do Instagram que a pessoa mandar pode ser baixado com `juanig` na pasta de assets do projeto.

Repositório: https://github.com/Juancunhaa-dev/juanig  
Release mais recente: https://github.com/Juancunhaa-dev/juanig/releases/latest

## Passos

1. Detecte o sistema operacional e o IDE atual.
2. Instale a CLI:
   - **Windows:** rode no PowerShell e depois abra um terminal novo:
     ```powershell
     irm https://github.com/Juancunhaa-dev/juanig/releases/latest/download/install.ps1 | iex
     ```
     Se falhar, instale o Python 3 e rode:
     ```powershell
     python -m pip install --upgrade git+https://github.com/JuanCunhaa-dev/juanig.git
     python -m juanig --setup
     ```
     Não baixe nem execute `juanig.exe`. O Smart App Control do Windows bloqueia o arquivo sem assinatura.
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
- Pastas padrão se a pessoa não escolher: `public/images`, depois `src/assets`, depois `./downloads`
- Os arquivos caem em `PASTA/username/arquivo`
- Nunca commite `JUANIG_SESSIONID` nem cookies
