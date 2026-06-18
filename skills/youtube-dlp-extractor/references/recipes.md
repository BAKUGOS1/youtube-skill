# yt-dlp recipes

## Metadata JSON

```bash
yt-dlp --skip-download --dump-single-json URL
```

## Available formats

```bash
yt-dlp --list-formats URL
```

## Subtitles only

```bash
yt-dlp --skip-download --write-subs --write-auto-subs \
  --sub-langs "en.*,hi.*" --sub-format "vtt/srt/best" URL
```

## Audio for permitted transcription

```bash
yt-dlp -x --audio-format m4a --audio-quality 0 URL
```

## Bounded playlist metadata

```bash
yt-dlp --flat-playlist --playlist-end 50 --dump-single-json URL
```

Prefer the bundled wrapper because it avoids shell interpolation and applies safer defaults.
