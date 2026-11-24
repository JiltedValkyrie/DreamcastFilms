# The Little Match Girl

A two minute short film for the Sega Dreamcast, rendered live by the console.

It is New Year's Eve and the cold is deep. A girl who has sold no matches all day strikes them one by one against a wall, and
in each small light she sees something warm: a stove, a table, a tree, and at last her grandmother.

Based on Hans Christian Andersen's fairy tale "The Little Match Girl" (Den lille Pige med Svovlstikkerne, first published
1845). The tale is in the public domain. The narration is new English wording written for this film and quotes no
translation.

A title card, twelve shots in 120 seconds for one narrator's voice, with typed subtitles, sound, a music-box song and 32
seconds of silent-film end credits; then it returns to its title card and waits for START. Every shape is built from numbers by the program; the only files it
reads are sound, the subtitle and credit type, the title card, and their timing.

Tale: public domain. Narration text and film: (c) 2026 Jilted Valkyrie. The film is free and is never to be sold: its
code is under the PolyForm Noncommercial License 1.0.0 and the film content under CC BY-NC-SA 4.0 (see `../LICENSE` and
`../LICENSES/`). The effects library SH4DER-PVR keeps its own licence.

## Credits

The nine cards of the film's end credits, as text:

| Card | Text |
|---|---|
| 1 | Directed & Narrated By: **Jilted Valkyrie** |
| 2 | Music: **Aureolus Omicron** (CC0 1.0 Public Domain) |
| 3 | Rendered In Real Time On: **Sega Dreamcast**, SH-4 RISC, PowerVR |
| 4 | Tale: The Little Match Girl, Hans Christian Andersen, 1845, public domain |
| 5 | Sound: qubodup: Flare ignition; qubodup: 4 dry snow steps; AntumDeluge: Fire Crackling; SketchMan3: wind whoosh loop; n4: Basic Sound Effects |
| 6 | Fonts: Aldrich: Matthew Desmond, 2011; Cinzel: Natanael Gama; Cormorant Garamond: C. Thalmann |
| 7 | Font Licence: SIL Open Font License 1.1, covers all three fonts above |
| 8 | Libraries: KallistiOS: KOS License; SH4ZAM: Falco Girgis & contributors; SH4DER-PVR: Jilted Valkyrie |
| 9 | Look Inspired By: **NTSCRT**, Finn McKenty |

Thanks: Finn McKenty, author of [NTSCRT](https://github.com/finnmckenty/NTSCRT), whose work on the look of old screens prompted
this film's old-film look. No NTSCRT code is part of the film.

Every sound in the public build is CC0 1.0 from opengameart.org; pages, authors and checksums are in `CREDITS.md` and
`audio_public.json`, licence notices of the libraries and fonts in `THIRD_PARTY_NOTICES.md`. The narrator's recording is
the film maker's own and is not in this repository; a build without it plays the film with its subtitles and no voice.
"Sega" and "Dreamcast" are trademarks of their owner; this is an unofficial, non-commercial homebrew work and is not
endorsed by it.

## Files

| File | What it is |
|---|---|
| `matchlight_scene.h` | The whole film as tables and plain functions: shots, cameras, lights, the girl, the set, the snow, the visions, the sound cues, the credits' timing. No hardware calls, so a PC can test it. |
| `matchlight.c` | The Dreamcast program: boot stages, pad, clock, drawing, sound, subtitles, title card, credits, readout. |
| `test/matchlight_scene_test.c` | Host test of `matchlight_scene.h`. |
| `tools/audio.py` | Builds the disc's sound effects (`sfx/*.wav`) and the long effects' stream (`fx.wav`) from a manifest. |
| `tools/narration.py` | Builds the narrator's voice track (`voice.wav`) from an edit list of a recording, the song under it (`music.wav`), the subtitle type (`font.bin`) and the typed subtitles (`subs.bin`). |
| `tools/credits.py` | Builds the end credits (`credits.bin`) and copies licence texts into `LICENSES/`. |
| `tools/title.py` | Builds the title card (`title.bin`) from a 640 x 480 picture of your own. |
| `tools/fetch_deps.py` | Fetches SH4DER-PVR and SH4ZAM into `deps/` at pinned commits. |
| `tools/menuart.py` | Builds box and icon artwork for the openMenu launcher of an optical drive emulator from two pictures of your own. |
| `narration.json`, `credits.json` | The narrator's lines, one per shot; the credit cards' text. |
| `audio_public.json` | The public set: every source (URL, sha256, author, licence) and how each sound is cut from it. |
| `CREDITS.md`, `THIRD_PARTY_NOTICES.md` | Who made what; the notices of the libraries and fonts. |

The working name of the program and of its files is "Match Light".

## Build

What it needs:

- [KallistiOS](https://github.com/KallistiOS/KallistiOS) and its SH-4 toolchain, installed by you as its own instructions say,
  environment sourced (`kos-cc` on the path). It is not fetched by this repository.
- [SH4ZAM](https://github.com/gyrovorbis/sh4zam): all of the film's maths goes through it. Fetched by `tools/fetch_deps.py`.
- [SH4DER-PVR](https://github.com/JiltedValkyrie/SH4DER-PVR): the effects library the film is drawn with, fetched the same way
  (snow, fog, rising lights, spark pools, snow footprints, old-film wear, frame texture). The film needs it at the commit
  that has `sh4der_deform.h`, `sh4der_mist.h`, `sh4der_rise.h` and `sh4der_film.h` beside `sh4der_lens.h`, `sh4der_taa.h`,
  `sh4der_ca.h` with `src/sh4der_ca.c`, and `sh4der_guard.h`: fa8bebd5596891e957723cf50b6642b5a681fbdb.
- On the PC: Python 3.8 or later, ffmpeg 4.4 or later, Pillow 9.2 or later (for the tools that draw type and pictures),
  and [mkdcdisc](https://gitlab.com/simulant/mkdcdisc) to write the image.

The two libraries (into `deps/`, each at the commit the film was made with; the script prints where their licences lie and
never replaces a folder that is there):

    python tools/fetch_deps.py

Host test (no console, no KallistiOS):

    make test

Disc files (nothing these tools read or write is in the repository; they write into `build/disc/`):

    python tools/audio.py --fetch
    python tools/narration.py --font assets/files/Aldrich-Regular.ttf --font-licence assets/files/OFL-Aldrich.txt \
        [--edit voice_edit.json --takes <folder of recordings>] [--music assets/unpack/musicbox/musicbox3_sad_tune.ogg]
    python tools/credits.py --title-font assets/files/Cinzel-wght.ttf --body-font assets/files/CormorantGaramond-wght.ttf \
        --licence OFL1.TXT=assets/files/OFL-Aldrich.txt --licence OFL2.TXT=assets/files/OFL-Cinzel.txt \
        --licence OFL3.TXT=assets/files/OFL-CormorantGaramond.txt --licence SH4ZAM.TXT=<SH4ZAM>/LICENSE --licence KOS.TXT=<KallistiOS>/doc/LICENSE.md
    python tools/title.py --image <a title card of your own, 640 x 480>      (optional: without it the film opens on its first shot)

Program and image (KallistiOS environment sourced):

    make CDI=build/<name>.cdi

(`make SH4DER=<checkout> SH4ZAM=<checkout>` uses checkouts of your own in place of `deps/`.)

`make` puts the contents of `build/disc/` on the image and never replaces an existing image. Any file that is missing from
the disc is simply not played or shown: the film still runs. The host test passes and the Dreamcast build compiles with no
warning; the numbers under "Cost" are counted from the tables, not measured on a console.
(A compiler note: the `NOINLINE` marks in `matchlight.c` keep the large functions out of `main`; with everything inlined this
toolchain's SH compiler stopped with an internal error in its register reload pass.)

## Pad

| Button | Action |
|---|---|
| A | pause / resume the clock (the snow stops too) |
| D-pad right / left | jump to the start of the next / previous shot; right from the last shot jumps to the credits |
| Y | lens pass (chromatic aberration and temporal anti-aliasing) off / on (on at start) |
| START | play the film from the waiting title card |
| D-pad up | show / hide the readout: shot, time, frames a second, frame time, TA kilobytes used, triangles sent, VRAM free (hidden at start) |
| B | old-film look off / on (on at start) |
| X | show / hide the debug caption: the shot's name and a few words on what it shows, on the upper letterbox bar (hidden at start) |

## The shots

The lens column is the HORIZONTAL field of view. The girl is a silhouette, 6.0 m or more from the lens in every shot. The street
is an open lane 14 m wide (house fronts 7.0 to 7.6 m out from its middle) and every camera stands inside the lane; the test walks
the line from each lens to the girl, the tree and both ends of the footprint trail.

| Shot | Time | Lens | Match | What it shows |
|---|---|---|---|---|
| M1 | 0:00 - 0:13 | 60 deg | none | Fades up from black. The street: ten gabled house fronts, warm lit windows with glows, night sky, shaped snow, fog, falling snow, the girl as a dark shape far away. |
| M2 | 0:13 - 0:25 | 45 deg | none | She walks in from 24 m to 15 m, stooped, in short steps; seventeen bare footprints sink into the snow behind her, a footfall sounding for each. |
| M2b | 0:25 - 0:32 | 35 deg, lens 0.45 m | none | Low and static, looking past her along the trail of pits; the slipper she lost lies in the snow, left foreground; a carriage is heard. |
| M3 | 0:32 - 0:44 | 35 deg | struck on the cut, 1.2 m pool | Opens on the strike flash. The warm pool, the girl lit from below, and the first vision: an iron stove with brass feet, tongs and shovel. |
| M4 | 0:44 - 0:50 | 40 deg, slow pull | out in 0.4 s | The flame dies; the stove goes with it; the camera pulls back. |
| M4b | 0:50 - 0:58 | 34 deg, lens 1.4 m | none | She sits in the snow, the fog closed in behind her. She stays seated through M9. |
| M5 | 0:58 - 1:07 | 40 deg | struck on the cut, 1.6 m pool | A table with a white cloth and a roast goose, which hops off its dish and waddles 1.2 m toward the lens before the match is out. |
| M6 | 1:07 - 1:19 | 62 deg, crane 1.0 to 2.4 m | struck on the cut, 1.6 m pool | The Christmas tree, 4.5 m, three ornaments. From 4 s its 48 candles lift off and come to rest as stars (`sh4der_rise`). |
| M7 | 1:19 - 1:25 | 50 deg, tilted up | none | The night sky with the candle stars. At 0.6 s a falling star crosses, its streak 42 % of the frame's width. |
| M8 | 1:25 - 1:34 | 40 deg | struck on the cut, 1.4 m pool | The grandmother, a pale figure with open arms; the whole frame is lifted warm. |
| M9 | 1:34 - 1:48 | 50 deg | struck on the cut, 2.5 m pool | The whole bundle: the frame peaks bright for 1 s. From 10 s two pale figures, the grandmother leading the girl's spirit by the hand, rise 1.7 m from where she sits, and ten lights lift off. Fades to black. |
| M10 | 1:48 - 2:00 | 60 deg, lens 0.8 m, pull 6 to 9 m | none | Cool dawn. She lies in the snow, three burned matches by her hand; the pits fill with new snow. No warm colour. Fades to black. |

The picture is letterboxed (`ML_LETTERBOX` 1 in `matchlight_scene.h`; 0 shows all 480 rows): the film is framed for 16:9, so the
60 rows above and below the middle 640 x 360 band are black bars (the subtitles are typed on the lower one). A shot that opens
on a struck match is cut hard, on two frames of gold-white. Every other cut is a dip through black (0.5 s out, 0.5 s in): the
program draws one picture a frame and has no second one to dissolve with.

## How things are drawn

- All shapes are flat vertex-coloured polygons; the set has no texture. The houses are boxes without roofs.
- The girl is a few dark quads and a round eight-sided head, turned to the camera: standing, seated or lying. No face.
- The visions (stove, table and goose, grandmother) and the two spirits are flat cut-outs of ADDED light: they exist only while
  their match burns and are gone 0.4 s after it. The slipper and the burned matches are solid dark cut-outs.
- Candles, stars, ornaments and the falling star are soft additive quads from a 4-cell generated atlas (`sh4der_spark`).
- The fog bank is ten upright sheets (`sh4der_mist`) with a 64 x 64 generated noise texture; the falling snow is `sh4der_motes`.

## The old-film look

The picture is laid under the wear of old film (B switches it): darker corners and grain (`sh4der_lens`), and from `sh4der_film`
a brightness that swings by 5 % peak to peak at 1.3 and 2.1 hertz (far from a strobe: the effect refuses more than 8 % peak to peak or 3 hertz),
a faint warm tint, up to three thin scratches that live 0.1 to 0.33 s and stay out of the middle of the picture, 6 to 12 dust
specks a frame (at most two over the footprint trail in the low shot), and a gate weave of 0.3 pixel that moves the 3D picture
only. Nothing is drawn on the letterbox bars, the subtitles or the credits; the title card gets a lighter wear. The film keeps
its colour and its frame rate. Cost: 8 KB of video memory (the grain tile), about 4 KB of RAM, about 350 triangles.

## The lens pass

The film's picture is drawn into a 640 x 480 frame texture (`sh4der_ca`) and put on the screen as three colour channels, each
at its own scale about the centre: chromatic aberration at strength 0.5, red and blue 1.5 pixels apart in the corner, none in
the middle. With a second frame texture the picture is anti-aliased over time (`sh4der_taa`): each frame is drawn a fraction
of a pixel aside (eight offsets in turn, a quarter pixel at the most) and the frame before is blended into it at 0.45, so an edge averages out and the
falling snow keeps its shape; a new shot keeps nothing of the frame before. The title card, the film wear, the bars, the
subtitles and the credits are drawn after the pass, at full sharpness. Cost: 640 KB of video memory a frame texture (two:
1,280 KB); the program takes two, one or none so that 448 KB stay free, and says which on the serial line. The picture is
rendered twice a frame (once into the texture, once from it: three screen-sized layers); the frame time is not measured.

## The snow

The ground is shaped, not flat (`ml_snow_height`): wall banks 0.67 to 1.62 m high at the house fronts, rolling drifts of 0 to
0.44 m, six piles of 0.75 to 1.20 m, and a level path within 1.25 m of the street's middle. A slope is shaded by a fixed moon
direction (40 % to 140 % of level snow).

Footprints are real pits. The ground grid's 1 m quads cannot show one, so the grid's middle column along her walk is replaced
by the trail patch: 8 x 88 quads at 0.125 m whose vertices take their height, darkening and slope shade from the `sh4der_deform`
grid. Each foot presses two round stamps (heel and toe) and SINKS in: the pit deepens for as long as that step's footfall
sound plays. No two prints are alike: place, depth (0.12 to 0.20 m), size, length and the turn of the foot come from a seeded
hash, so the film always has the same trail. A pit is about 0.24 m wide and 0.36 m long and ends before the next begins. The patch's outer vertices lie on the ground grid's edge at the ground's own height and colour, and a strip of snow 1.5 cm under the surface backs the join on every side, so no line shows where the two meshes meet.

## Sound

| Part | How |
|---|---|
| Sound effects | Short sounds are AICA sound effects in the disc's `sfx/` (KallistiOS `snd_sfx`, mono ADPCM at 11,025 or 22,050 Hz; the wind and crackle loops are 16-bit PCM because an ADPCM loop clicks at its seam). The program plays them from `ml_cues` (shot, seconds into the shot, sound, loudness, pan), one footfall per footprint, the wind loop through the film (it fades out over the last 3 s), the crackle loop while a match burns. |
| Long effects | A sound longer than 65,534 samples cannot be an AICA sound effect. A manifest marks such a sound `"stream": true` and `tools/audio.py` lays it into `fx.wav` at the times `ml_cues` and `ml_holds` give it; a held sound (`ml_holds`) is faded out over 0.325 s when its animation is done. |
| Narrator | `voice.wav`, cut from the film maker's recording by an edit list (start and end of each line, the time of each word); never in the repository. |
| Music | `music.wav`: a song given to `tools/narration.py --music`, laid 20 dB under the voice's level (23 dB while a line is spoken), then 14 dB under it through the credits. |
| Sound bed | A manifest may name one sound as a `"bed"`: `tools/audio.py` loops it under the whole film inside `fx.wav` at a stated level, with a fade at each end. The public manifest has none (no CC0 source is chosen yet), so a public build plays without one. |
| Streams | `voice.wav`, `music.wav` and `fx.wav` are 22,050 Hz 16-bit mono PCM streamed from the disc (KallistiOS `snd_stream`, a 32 KB buffer each), polled once a frame and moved to the clock's place whenever the clock jumps (pause, shot jump, the loop). They are three separate files read at once: fine from a GDEMU or an emulator; a real GD-ROM drive may have to seek back and forth between them. |

The public manifest uses CC0 sources only (the sounds `carriage` and `spirit` have no source in it yet and stay silent). A
private build may use `--manifest` with a file that points at a sound library licensed to one person (`"root": "library"`,
`--library <its folder>`): such a disc is for that person's own console and is not for publishing.

## Subtitles

The narrator's sentences are typed on the lower letterbox bar, letter by letter, in step with the voice: each word's letters
appear over the first 80 % of the time the word is spoken. `font.bin` holds the printable ASCII glyphs at 16 pixels in one
256 x 128 ARGB4444 picture; `subs.bin` holds each sentence's letters with their place and moment (the program reads at most 48
sentences and 12 KB; the tool refuses more). Without an edit list the subtitles are typed at 2.1 words a second.

## Title card

The film opens on a title card that comes up from black over 1 s and then WAITS, with "PRESS START" pulsing on the lower bar (in the subtitle type; snow keeps falling behind the card). START sends the card down to black over 1 s, then the first shot fades up. After the credits the loop comes back to the card and waits again. The card
is a 640 x 480 picture at full size and not compressed: two ARGB1555 tiles (512 x 512 and 128 x 512, ordered dither), 640 KB of
video memory. Its translucency is kept apart from its colour, as bands of rows with one alpha each, and drawn as blended
rectangles over the first shot's first frame: the card lies on the picture like a sheet of slightly clear film, and the
falling snow glimmers through it. Without `title.bin` the prompt stands over the first shot's first frame; without the subtitle type as well the film just runs. On the clock the card is the last
stretch of the loop (film, credits, card) and the program starts there, so no film time moved.

## End credits

After the film come 32 s of silent-film intertitle cards: nine cards of 3 s, a 0.5 s dissolve between two cards, the first up
from black, the last down to black over 1 s. A card is a near-black ground with a hairline border, a label in letter-spaced
capitals, one short amber rule, and a name, or up to three lines of at most 36 characters, or (the sound sources) up to six lines in two columns. `credits.bin` holds each letter's
place and one 256 x 256 picture of the glyphs the cards use; `tools/credits.py` refuses a card list that is not exactly the
nine cards the program shows. One card thanks the author of NTSCRT, whose work on the look of old screens prompted the film's
old-film look; no NTSCRT code is part of the film.

## Library modules used

`sh4der_film` and `sh4der_lens` (the old-film look), `sh4der_ca` and `sh4der_taa` (the lens pass), `sh4der_pool` (the warm pool fans), `sh4der_spark` (flame, glows, stars, candles), `sh4der_motes` (falling snow),
`sh4der_deform` (the footprint grid), `sh4der_mist` (the fog bank), `sh4der_rise` (candles and lights lifting), `sh4der_guard`
(every header and triangle is checked before it is sent), `sh4der_core` (SH4ZAM wrappers for all the maths).
`sh4der_motes` works in a z-up space, so the snow's emitters and view are stored with y and z swapped.

## Cost (counted from the tables and constants, not measured on a console)

- Triangles a frame, upper bound with no culling: 3,882 (M4b) to 4,028 (M9); the test prints each shot. The ground is 1,978 of
  them and the trail patch 1,408.
- Video memory textures: about 921 KB (title card 640 KB, readout 64 KB, subtitle glyphs 64 KB, credit glyphs 128 KB, sprite atlas 8 KB, fog
  noise 8 KB, caption 8 KB, snow mask 0.5 KB), plus the KallistiOS frame buffers and two 512 KB TA vertex buffers.
- RAM, static: about 310 KB (three 32 KB stream buffers, readout image 64 KB, ground and trail tables about 70 KB, snow dent
  grid 25 KB, subtitle and credit records 20 KB, the rest small).
- Sound RAM: about 270 KB of 2,048 KB for the resident effects, plus three 32 KB stream buffers.
- Disc: voice 5.3 MB, long effects 5.3 MB, music 6.4 MB.
- CPU: not measured.
