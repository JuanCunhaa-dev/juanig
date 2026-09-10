---
name: juanig
description: >-
  Downloads Instagram posts, carousels, Reels, and videos via the juanig CLI
  for realistic website images. Use when the user says juanig, mentions skill
  juanig, asks to download Instagram posts, or needs real photos from a profile
  for a site.
---

# juanig

Public Instagram media downloader. Always run the `juanig` CLI. Do not write a scraper.

## Command

```bash
juanig "URL" ["URL2" ...] -o FOLDER --json
```

- Files are saved as `photo.jpg` / `video.mp4` (no profile names)
- Default folder is the user Downloads directory
- Pass multiple links, `@links.txt`, or `-` for stdin
- `--first` / `--index N` download one carousel item
- `--dry-run` resolves without writing files
- `--json` returns paths, caption, width, and height
- Private posts: `JUANIG_SESSIONID` cookie only. Never commit it.

If `juanig` is not on PATH, tell the user to run `juanig --setup` or follow [AI-SETUP.md](https://github.com/Juancunhaa-dev/juanig/blob/main/AI-SETUP.md).

## Where to save in a project

If the user does not pick a folder, use their Downloads folder. For a site, pass `-o public/images` (or `src/assets` / `static` / `assets` if that fits the project).

## Flow

1. Collect Instagram URLs
2. Pick the project assets folder
3. Run `juanig` with `--json`
4. Confirm the files exist
5. Wire the images into the layout

## Examples

```bash
juanig "https://www.instagram.com/p/DRH53C9EYV4/" -o public/images --json
juanig "https://www.instagram.com/p/AAA/" --first -o public/images --json
juanig @links.txt -o src/assets/instagram --json
```
