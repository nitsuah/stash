"""Writes icon16/48/128.png (blue rounded tile with a white check) using only the standard library. Run in python:3-slim."""
from pathlib import Path
import struct
import zlib


def png(size):
    rows = []
    r = size * 0.2
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            cx, cy = min(x, size - 1 - x), min(y, size - 1 - y)
            inside = not (cx < r and cy < r and (r - cx) ** 2 + (r - cy) ** 2 > r * r)
            u, v = x / size, y / size
            # check mark: two line segments (0.22,0.52)->(0.42,0.72) and (0.42,0.72)->(0.78,0.30)
            def near(ax, ay, bx, by):
                dx, dy = bx - ax, by - ay
                t = max(0, min(1, ((u - ax) * dx + (v - ay) * dy) / (dx * dx + dy * dy)))
                return ((u - ax - t * dx) ** 2 + (v - ay - t * dy) ** 2) ** 0.5 < 0.075
            if not inside:
                row += bytes([0, 0, 0, 0])
            elif near(0.22, 0.52, 0.42, 0.72) or near(0.42, 0.72, 0.78, 0.30):
                row += bytes([255, 255, 255, 255])
            else:
                row += bytes([11, 92, 173, 255])
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")



def main():
    out_dir = Path(__file__).parent
    for s in (16, 48, 128):
        (out_dir / f"icon{s}.png").write_bytes(png(s))
        print("icon", s)


if __name__ == "__main__":
    main()
