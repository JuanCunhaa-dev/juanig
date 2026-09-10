# juanig

CLI que baixa fotos, carrosséis, vídeos e Reels do Instagram a partir de um link. Feita para montar sites com imagens reais.

```bash
juanig "https://www.instagram.com/p/DRH53C9EYV4/" -o public/images
```

Por padrão os arquivos vão para a pasta **Downloads** como `photo.jpg` / `video.mp4`, sem nome de perfil. Sem servidor web. No Windows a instalação usa Python e um `juanig.cmd`, para o Smart App Control não bloquear um `.exe` sem assinatura.

English guide: [README.md](README.md)  
Mande este arquivo para uma IA: [AI-SETUP.pt-BR.md](AI-SETUP.pt-BR.md)

## Instalar

Precisa de **Python 3**. Node é opcional e só entra no `npm i -g`.

### npm

```bash
npm i -g juanig
```

Por baixo isso roda `pip install` e coloca o `juanig` no PATH.

### Windows (PowerShell)

```powershell
irm https://github.com/Juancunhaa-dev/juanig/releases/latest/download/install.ps1 | iex
```

### pip

```bash
pip install juanig
juanig --setup
```

Para atualizar depois: `juanig --update`.

`--setup` / `--install-skills` só copia a skill nos IDEs que já estão instalados.

## CLI

```text
juanig [URL ...] [opções]
```

| Argumento | Descrição |
|---|---|
| `URL` | Um ou mais links, `@links.txt`, ou `-` para ler do stdin |
| `-o`, `--output` | Pasta de destino. Padrão: a pasta `Downloads` do usuário |
| `--first` | Baixa só o primeiro item do carrossel |
| `--index N` | Baixa só o item N do carrossel (começando em 1) |
| `--dry-run` | Resolve o post e mostra os caminhos sem baixar |
| `--json` | Imprime JSON com caminhos, legenda e tamanhos (melhor para agentes) |
| `--sessionid` | Cookie `sessionid` do Instagram se o post exigir login |
| `--setup` | Coloca o juanig no PATH e grava skills só nos IDEs instalados |
| `--install-skills` | Só grava a skill nos IDEs instalados |
| `--update` | Atualiza para a versão mais recente do PyPI |
| `-V`, `--version` | Mostra a versão instalada |
| `-h`, `--help` | Mostra a ajuda |

Variáveis de ambiente: `JUANIG_OUTPUT`, `JUANIG_SESSIONID`.

### Exemplos

```bash
juanig "https://www.instagram.com/p/AAAA/"
juanig "https://www.instagram.com/p/AAAA/" --first -o public/images
juanig @links.txt -o public/images --json
juanig "https://www.instagram.com/p/AAAA/" --dry-run --json
```

### Saída

Padrão:

```text
1 file(s)
  C:\Users\voce\Downloads\photo.jpg
```

`--json`:

```json
{
  "ok": true,
  "dry_run": false,
  "output": "C:\\Users\\voce\\Downloads",
  "posts": [{
    "shortcode": "AAAA",
    "kind": "Photo",
    "caption": "Legenda opcional",
    "files": ["C:\\Users\\voce\\Downloads\\photo.jpg"],
    "media": [{ "index": 1, "kind": "image", "width": 1440, "height": 1800 }]
  }],
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
- Post privado ou bloqueado pede `--sessionid` / `JUANIG_SESSIONID`
- O Instagram pode limitar acesso anônimo
- URLs do CDN expiram; o juanig baixa o arquivo na hora
- Nunca commite cookies

## Aviso

O juanig é extraoficial e não tem ligação com a Meta ou o Instagram. Use para baixar, de forma pessoal e lícita, mídia pública ou conteúdo que você tem direito de usar (por exemplo, assets de um site). Respeite os termos do Instagram e os direitos autorais. Não use para coletar em massa.

## Licença

MIT
