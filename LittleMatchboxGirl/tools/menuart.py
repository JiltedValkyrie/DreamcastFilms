#!/usr/bin/env python3
"""Menu artwork for a disc image on an optical drive emulator: turns a box picture and an icon picture into the
texture files and the small databases the openMenu launcher reads.

    python tools/menuart.py --key KEY [--box BOX.png] [--icon ICON.png]
                                            [--description TEXT [--players N] [--vmu-blocks N]]
                                            [--box-base BOX_EX.DAT] [--icon-base ICON_EX.DAT] [--meta-base META.DAT | --meta-new]
                                            --out DIR

What it writes into --out (a folder that must not yet hold these files: nothing is replaced):

  <KEY>_box.pvr    the box picture, 256 x 256, as a PVR texture: "GBIX" block (global index 1001), "PVRT" block,
                   pixel format RGB565, square twiddled, no mipmaps: 32 bytes of header and 131,072 of texels.
  <KEY>_icon.pvr   the icon picture, 128 x 128, the same way: 32 + 32,768 bytes.
  BOX_EX.DAT       the launcher's add-on box database with this one picture, or, with --box-base, the entries of
                   that database plus this one (an entry with the same key is replaced).
  ICON_EX.DAT      the same for the icon (--icon-base).
  META.DAT         only with --description AND --meta-base: the entries of that database plus this disc's (players,
                   memory card blocks, description). The launcher reads one metadata database and no add-on one, so
                   without a base to add to, the entry is written alone as META_<KEY>.DAT for adding later, and is
                   NOT a file to install as it is (it would replace every other disc's metadata). With --meta-new
                   (the launcher has no metadata database at all yet) META.DAT is written with this one record.

The key is how the launcher finds a disc's art: the disc's product number with the dashes removed and cut at the first
space, in capitals, at most 10 characters ("AB-CD12345" has the key "ABCD12345").

The pictures must already have their final size (256 x 256 and 128 x 128): the tool converts pixel for pixel and does not
scale, so a one pixel line stays a one pixel line. Each channel is cut to RGB565 (5, 6, 5 bits) without dither; a colour
that already lies on that grid (red and blue multiples of 8, green a multiple of 4) comes through exactly as its top
bits. After writing, every texture is decoded again and compared with its source; the report gives the largest
difference a channel and the colour of the picture's top left pixel as it will be shown.

The database layout is that of the launcher's own packer (version 1): a 16 byte header ("DAT", the byte 1, u32 chunk size,
u32 chunk count, u32 header chunks beyond the first), then 16 bytes an entry (12 characters of key, NUL padded, and the
u32 number of the chunk that holds it), zeros up to a chunk boundary, then the chunks, all one size. Little-endian.

The pictures are build inputs, not part of the repository. Needs Python 3.8 or later with Pillow.
Copyright (c) 2026 Jilted Valkyrie. See ../../LICENSE.
"""
import argparse
import os
import struct
import sys

BOX_SIDE = 256            # the launcher's box texture, texels a side
ICON_SIDE = 128           # its icon texture
GBIX_INDEX = 1001         # the global index the launcher's own art carries
PVR_RGB565 = 0x01         # PVRT pixel format byte: RGB565
PVR_TWIDDLED = 0x01       # PVRT data format byte: square, twiddled, no mipmaps
PVR_HEADER_BYTES = 32     # "GBIX" block (16) and "PVRT" block header (16)
KEY_MAX = 10              # characters of a key the launcher's packer keeps
ENTRY_BYTES = 16          # one table entry: 12 characters and a u32
HEADER_BYTES = 16         # the database header
META_BYTES = 384          # one metadata record: 8 bytes of numbers and 376 of description
META_TEXT = 376           # room for the description, with its closing NUL


def twiddle_index(x, y):
    """The place of texel (x, y) in a twiddled square texture: the bits of y and x interleaved, y's lowest bit first."""
    n = 0
    for bit in range(16):
        n |= ((y >> bit) & 1) << (2 * bit)
        n |= ((x >> bit) & 1) << (2 * bit + 1)
    return n


def to_pvr(png, side):
    """Reads a picture that must be side x side and returns (its PVR file's bytes, its pixels as RGB tuples in rows)."""
    from PIL import Image
    im = Image.open(png)
    if im.size != (side, side):
        raise SystemExit("menuart: %s is %d x %d; it must be %d x %d (the tool does not scale)" % (png, im.size[0], im.size[1], side, side))
    if im.mode in ("RGBA", "LA", "P") and im.convert("RGBA").getchannel("A").getextrema()[0] < 255:
        raise SystemExit("menuart: %s has transparent pixels; the launcher's art has no transparency: flatten it first" % png)
    raw = im.convert("RGB").tobytes()                           # three bytes a pixel, in rows
    px = [(raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw), 3)]
    texels = [0] * (side * side)
    for y in range(side):
        for x in range(side):
            r, g, b = px[y * side + x]
            texels[twiddle_index(x, y)] = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
    data = struct.pack("<%dH" % len(texels), *texels)
    head = b"GBIX" + struct.pack("<III", 8, GBIX_INDEX, 0)
    head += b"PVRT" + struct.pack("<IBBHHH", len(data) + 8, PVR_RGB565, PVR_TWIDDLED, 0, side, side)
    return head + data, px


def from_pvr(blob):
    """Decodes a PVR file this tool wrote back to rows of RGB tuples, each channel widened as the PVR shows it (the top
    bits repeated into the low ones). Returns (side, pixels)."""
    if blob[:4] != b"GBIX" or blob[16:20] != b"PVRT" or blob[24] != PVR_RGB565 or blob[25] != PVR_TWIDDLED:
        raise SystemExit("menuart: not a twiddled RGB565 texture with a GBIX block")
    side, height = struct.unpack_from("<HH", blob, 28)
    if side != height or len(blob) != PVR_HEADER_BYTES + side * side * 2:
        raise SystemExit("menuart: the texture's size and its length do not agree")
    texels = struct.unpack_from("<%dH" % (side * side), blob, PVR_HEADER_BYTES)
    out = []
    for y in range(side):
        for x in range(side):
            t = texels[twiddle_index(x, y)]
            r, g, b = t >> 11, (t >> 5) & 63, t & 31
            out.append(((r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)))
    return side, out


def dat_read(path):
    """Reads a database: returns (chunk size, {key: chunk bytes}) with the keys in the file's order."""
    with open(path, "rb") as f:
        blob = f.read()
    if len(blob) < HEADER_BYTES or blob[:3] != b"DAT" or blob[3] != 1:
        raise SystemExit("menuart: %s is not a version 1 database" % path)
    chunk, count, _ = struct.unpack_from("<III", blob, 4)
    entries = {}
    for i in range(count):
        at = HEADER_BYTES + ENTRY_BYTES * i
        key = blob[at:at + 12].split(b"\0")[0].decode("ascii")
        number = struct.unpack_from("<I", blob, at + 12)[0]
        if chunk == 0 or (number + 1) * chunk > len(blob):
            raise SystemExit("menuart: %s: the entry %s points past the end of the file" % (path, key))
        entries[key] = blob[number * chunk:(number + 1) * chunk]
    return chunk, entries


def dat_bytes(chunk, entries):
    """Lays a database out as the launcher's packer does: header, table, zeros to a chunk boundary, the chunks."""
    extra = (HEADER_BYTES + ENTRY_BYTES * len(entries)) // chunk      # chunks the header and table take beyond the first
    out = b"DAT\x01" + struct.pack("<III", chunk, len(entries), extra)
    for i, key in enumerate(entries):
        out += key.encode("ascii").ljust(12, b"\0") + struct.pack("<I", extra + i + 1)
    out += b"\0" * ((extra + 1) * chunk - len(out))
    for key in entries:
        if len(entries[key]) != chunk:
            raise SystemExit("menuart: the entry %s is %d bytes; every entry of this database is %d" % (key, len(entries[key]), chunk))
        out += entries[key]
    return out


def write_new(path, blob):
    """Writes a file that must not exist yet (open mode "x"): the tool never replaces a file."""
    with open(path, "xb") as f:
        f.write(blob)
    return "%s  %d B" % (os.path.basename(path), len(blob))


def main():
    ap = argparse.ArgumentParser(description="Builds a disc's menu artwork: PVR textures and the launcher's databases.")
    ap.add_argument("--key", required=True, help="the disc's product number without dashes, at most 10 characters")
    ap.add_argument("--box", help="the box picture, 256 x 256, no transparency")
    ap.add_argument("--icon", help="the icon picture, 128 x 128, no transparency")
    ap.add_argument("--description", help="the disc's description for the metadata database (at most 375 characters)")
    ap.add_argument("--players", type=int, default=1)
    ap.add_argument("--vmu-blocks", type=int, default=0)
    ap.add_argument("--box-base", help="an existing add-on box database to add the entry to")
    ap.add_argument("--icon-base", help="an existing add-on icon database to add the entry to")
    ap.add_argument("--meta-base", help="the existing metadata database to add the entry to")
    ap.add_argument("--meta-new", action="store_true", help="the launcher has no metadata database yet: write META.DAT with this one record")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    key = a.key.upper()
    if not key or len(key) > KEY_MAX or not all(c.isalnum() or c == "_" for c in key):
        raise SystemExit("menuart: the key must be 1 to %d letters, digits or underscores (no dashes), got '%s'" % (KEY_MAX, a.key))
    os.makedirs(a.out, exist_ok=True)
    report = []
    for png, side, base, name in ((a.box, BOX_SIDE, a.box_base, "BOX_EX.DAT"), (a.icon, ICON_SIDE, a.icon_base, "ICON_EX.DAT")):
        if not png:
            continue
        blob, source = to_pvr(png, side)
        _, shown = from_pvr(blob)
        worst = max(max(abs(s[c] - d[c]) for c in range(3)) for s, d in zip(source, shown))
        chunk, entries = dat_read(base) if base else (len(blob), {})
        if chunk != len(blob):
            raise SystemExit("menuart: %s holds entries of %d bytes; this texture is %d" % (base, chunk, len(blob)))
        entries[key] = blob
        kind = "box" if side == BOX_SIDE else "icon"
        report.append(write_new(os.path.join(a.out, "%s_%s.pvr" % (key, kind)), blob))
        report.append(write_new(os.path.join(a.out, name), dat_bytes(chunk, entries)) + "  %d entr%s, this one as %s" % (
            len(entries), "y" if len(entries) == 1 else "ies", key))
        report.append("  %s decoded again: top left pixel shown as %s (source %s), largest difference from the source %d of 255 a channel" % (
            kind, shown[0], source[0], worst))
    if a.description is not None:
        text = a.description.encode("ascii")
        if len(text) >= META_TEXT or not (0 <= a.players <= 255) or not (0 <= a.vmu_blocks <= 255):
            raise SystemExit("menuart: the description takes at most %d characters; players and blocks 0 to 255" % (META_TEXT - 1))
        # players, memory card blocks, an unused byte, network (0: none), genre flags (0), accessory flags (0), the text
        record = struct.pack("<BBBBHH", a.players, a.vmu_blocks, 0, 0, 0, 0) + text.ljust(META_TEXT, b"\0")
        if a.meta_base:
            chunk, entries = dat_read(a.meta_base)
            if chunk != META_BYTES:
                raise SystemExit("menuart: %s holds records of %d bytes, not %d" % (a.meta_base, chunk, META_BYTES))
            entries[key] = record
            report.append(write_new(os.path.join(a.out, "META.DAT"), dat_bytes(META_BYTES, entries)) + "  %d entries, this one as %s" % (len(entries), key))
        elif a.meta_new:
            report.append(write_new(os.path.join(a.out, "META.DAT"), dat_bytes(META_BYTES, {key: record})) +
                          "  1 entry, this one as %s: for a launcher that has no metadata database yet" % key)
        else:
            report.append(write_new(os.path.join(a.out, "META_%s.DAT" % key), dat_bytes(META_BYTES, {key: record})) +
                          "  this disc's record alone: NOT to be installed as META.DAT (give --meta-base to add it to the real one)")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, ValueError, IndexError, struct.error, UnicodeError) as e:     # a missing or existing file, a malformed database: one line, no trace
        raise SystemExit("%s: %s: %s" % (os.path.basename(__file__), type(e).__name__, e))
