#!/usr/bin/env python3
"""Make the android14-6.1 SUSFS namespace hunk apply on 6.1.124.

The gki-android14-6.1 tip was rebased onto 6.1.176, whose fs/namespace.c
includes trace/hooks/blk.h. The 2025-02 / 6.1.124 tree has neither that
line nor the header. Drop the one context line and fix the hunk counts.
Trees that already contain the include must not call this.
"""
import sys
from pathlib import Path


def main():
      path = Path(sys.argv[1])
      text = path.read_text()
      start = text.find("diff --git a/fs/namespace.c b/fs/namespace.c")
      if start < 0:
                sys.exit("namespace.c diff not found")
            nxt = text.find("\ndiff --git ", start + 1)
    end = nxt if nxt > 0 else len(text)
    block = text[start:end]
    old_hdr = "@@ -32,11 +32,21 @@\n"
    needle = " #include <trace/hooks/blk.h>\n"
    if old_hdr not in block or needle not in block:
              sys.exit("namespace hunk is not the 6.1.176 form")
          block = block.replace(old_hdr, "@@ -32,10 +32,20 @@\n", 1)
    block = block.replace(needle, "", 1)
    path.write_text(text[:start] + block + text[end:])
    print("Adjusted fs/namespace.c hunk for kernels without trace/hooks/blk.h")


if __name__ == "__main__":
      main()
