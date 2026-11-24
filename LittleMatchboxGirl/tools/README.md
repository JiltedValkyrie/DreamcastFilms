# Build tools

| Tool | What it makes |
|---|---|
| `fetch_deps.py` | Fetches SH4DER-PVR and SH4ZAM into `../deps/` at pinned commits. |
| `audio.py` | The disc's sound effects (`sfx/*.wav`) and the long effects' stream (`fx.wav`) from a manifest. |
| `narration.py` | The narrator's voice track, the song under it, the subtitle type and the typed subtitles. |
| `credits.py` | The end credits (`credits.bin`) and the licence texts on the disc. |
| `title.py` | The title card (`title.bin`) from a 640 x 480 picture. |
| `menuart.py` | Box and icon artwork for the openMenu launcher of an optical drive emulator. |

Each tool's own head comment says what it reads, what it writes and what it needs.

## Your own sounds

The repository's manifest, `../audio_public.json`, names only CC0 sounds, and a build from it is free to share. A few
sounds of the film have no CC0 source in it and stay silent in such a build.

To build with sounds of your own (a sound library you have a licence for, your own recordings), write a manifest of
your own and keep it and the sound files OUTSIDE the repository:

    python tools/audio.py --manifest <your manifest.json> --assets <folder of your files> [--library <root of a sound library>] --out build/disc

A manifest has the same shape as `audio_public.json`: under `"sounds"`, each of the film's sound names (they are listed
in `ml_sound_names` in `../matchlight_scene.h`) gets a `"path"` under `--assets` (or, with `"root": "library"`, under
`--library`), a `"rate"`, and optionally `"start"`, `"dur"`, an ffmpeg filter `"af"`, and `"stream": true` for a sound
longer than three seconds or so. An optional `"bed"` names one sound to loop quietly under the whole film.

Whether you may pass on a disc image that holds such sounds is a matter of their licences: check them before you share
an image. Never add licensed sound files, a recording of a voice, or a manifest that names them to this repository.
