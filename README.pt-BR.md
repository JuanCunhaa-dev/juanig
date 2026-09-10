# juanig

CLI que baixa fotos, carrosséis, vídeos e Reels do Instagram a partir de um link. Feita para montar sites com imagens reais.

```bash
juanig "https://www.instagram.com/p/DRH53C9EYV4/" -o public/images
```

Salva em `public/images/username/arquivo.jpg`. Sem servidor web. No Windows a instalação usa Python e um `juanig.cmd`, para o Smart App Control não bloquear um `.exe` sem assinatura.

English guide: [README.md](README.md)  
Mande este arquivo para uma IA: [AI-SETUP.pt-BR.md](AI-SETUP.pt-BR.md)

## Instalar

### Windows (recomendado)

No PowerShell:

```powershell
irm https://github.com/Juancunhaa-dev/juanig/releases/latest/download/install.ps1 | iex
```

Isso instala o Python se precisar e coloca um `juanig.cmd` no PATH. Depois abra um terminal novo. Não baixe o `juanig.exe` — o Windows bloqueia executável sem assinatura.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/Juancunhaa-dev/juanig/main/installer/install.sh | bash
```

### Pelo código

```bash
pip install git+https://github.com/Juancunhaa-dev/juanig.git
juanig --install-skills
```

`--setup` / `--install-skills` copia a skill para pastas do Cursor, Claude Code, Windsurf, Continue e afins, quando existirem.

## CLI

```text
juanig [URL ...] [opções]
```

| Argumento | Descrição |
|---|---|
| `URL` | Um ou mais links de post, carrossel ou Reel |
| `-o`, `--output` | Pasta base. Cada perfil vira uma subpasta. Padrão: `./downloads` |
| `--json` | Imprime JSON com os caminhos salvos (melhor para agentes) |
| `--sessionid` | Cookie `sessionid` do Instagram se o post exigir login |
| `--setup` | Instala o exe no PATH e grava as skills de IA |
| `--install-skills` | Só grava os arquivos da skill |
| `-h`, `--help` | Mostra a ajuda |

Variáveis de ambiente: `JUANIG_OUTPUT`, `JUANIG_SESSIONID`.

### Exemplos

```bash
juanig "https://www.instagram.com/p/AAAA/"
juanig "https://www.instagram.com/p/AAAA/" "https://www.instagram.com/reel/BBBB/" -o public/images --json
```

### Saída

Padrão:

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

## Usar com uma IA

Mande o [AI-SETUP.pt-BR.md](AI-SETUP.pt-BR.md) para o Cursor, Claude, Copilot, Windsurf ou qualquer agente. Peça para instalar o juanig e baixar os posts.

```text
Leia o AI-SETUP.pt-BR.md, instale o juanig e baixe estes posts em public/images:
https://www.instagram.com/p/AAAA/
```

## Observações

- Só posts públicos, a menos que você passe um `sessionid`
- O Instagram pode limitar acesso anônimo
- URLs do CDN expiram; o juanig baixa o arquivo na hora
- Nunca commite cookies

## Licença

MIT
