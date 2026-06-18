# Final PRD repository audit

This audit separates foundational dependencies from pattern-only references. Check current licenses and releases before implementation.

## Final shortlist

| Moviq capability | Recommended repositories | Use |
|---|---|---|
| Public captions | `jdepoix/youtube-transcript-api`, `yt-dlp/yt-dlp` | Caption-first ingest with language and timestamp metadata |
| Captionless transcription | `SYSTRAN/faster-whisper`, `openai/whisper` | GPU/CPU ASR fallback |
| Word timing and speakers | `m-bain/whisperX`, `jianfch/stable-ts`, `pyannote/pyannote-audio` | Alignment, subtitle timing, optional diarization |
| Speech segmentation | `snakers4/silero-vad`, `WyattBlue/auto-editor` | Speech/silence signals and edit-decision patterns |
| Scene segmentation | `Breakthrough/PySceneDetect` | Cuts, fades, chapters, thumbnails, and clip boundaries |
| Smart 9:16 reframing | `google-ai-edge/mediapipe` AutoFlip patterns | Face/object tracking and smooth crop paths |
| Programmatic rendering | `FFmpeg/FFmpeg`, `remotion-dev/remotion` | Deterministic media core plus React compositions |
| Output quality | `Netflix/vmaf` | Perceptual quality regression checks |
| YouTube platform APIs | `youtube/api-samples` plus current official docs | Owned-channel metadata and analytics; samples repo is archived |
| End-to-end inspiration | `mutonby/openshorts`, `AgriciDaniel/claude-shorts` | Workflow ideas only; audit licenses and architecture before reuse |

## Architecture decisions for the PRD

1. Use captions first, then permitted audio ASR fallback.
2. Default to `faster-whisper`; add WhisperX only for word alignment or speaker-aware workflows.
3. Rank clips using transcript semantics, scene boundaries, speech activity, and visual saliency together.
4. Use MediaPipe-style tracked reframing rather than a static center crop.
5. Use FFmpeg for media operations and Remotion for branded/template compositions.
6. Treat render completion and render quality as separate checks.
7. Use the official YouTube API for authenticated owned-channel features; use `yt-dlp` only for public extraction paths.
8. Keep external projects as references, not copied subsystems.

## Remaining implementation gaps

The six skills are usable, but these production features belong in Moviq rather than the generic skill pack:

- ASR worker with model selection, batching, caching, and GPU fallback;
- scene/VAD feature extraction service;
- multimodal clip-ranking model and evaluation dataset;
- smart-crop trajectory generator;
- authenticated YouTube Data/Analytics integration;
- render-quality regression harness using FFprobe and VMAF.
