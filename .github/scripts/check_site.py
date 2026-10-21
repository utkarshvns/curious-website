#!/usr/bin/env python3
"""Static checks for the portfolio site.

Runs with the Python standard library only - no dependencies to install.

    python .github/scripts/check_site.py

Exits non-zero and prints one line per problem if anything fails.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Files that are allowed to contain a raw "text" placeholder, matched case
# insensitively.
PLACEHOLDER_PATTERNS = [
    r"lorem ipsum",
    r"untitled\.tld",
    r"\(000\)\s*000-0000",
    r"somewhere road",
    r"information@untitled",
    r"powered by:\s*templated",
]

# Deliberately coarse: catches obvious key material that should never be
# committed to a public repository.
SECRET_PATTERNS = [
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"AKIA[0-9A-Z]{16}",
    r"gh[pousr]_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{32,}",
    r"xox[baprs]-[A-Za-z0-9-]{10,}",
    r"AIza[0-9A-Za-z_-]{35}",
    r"(?i)(api[_-]?key|secret|passwd|password|access[_-]?token)\s*[=:]\s*[\"'][^\"'\s]{8,}",
]

SCAN_EXTENSIONS = (".html", ".css", ".js", ".json", ".jsonc", ".md", ".xml", ".txt")
SKIP_DIRS = {".git", "node_modules"}

# SHA-256 (base64) of the vendored third-party libraries. Keep this in sync
# with assets/VERSIONS.md whenever a library is upgraded.
VENDOR_CHECKSUMS = {
    "assets/js/jquery.min.js": "/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=",
    "assets/js/jquery.scrolly.min.js": "i2Vx6iw2Mf9Qu0uW5/kIHG4z66re+csspZVdXgtiWgI=",
    "assets/js/skel.min.js": "3e+NvOq+D/yeJy1qrWpYkEUr6SlOCL5mHpc2nZfX74E=",
    "assets/css/font-awesome.min.css": "7Q8FEB1IBybFi81JVqHnsC8StTjQIFjxsOv9q+in70I=",
}


def iter_repo_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield os.path.join(dirpath, name)


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def html_files():
    return [p for p in iter_repo_files() if p.lower().endswith(".html")]


def check_asset_references(problems):
    """Every relative src/href must point at a file that exists."""
    pattern = re.compile(
        r"""(?:src|href)\s*=\s*["'](?!https?:|//|#|mailto:|tel:|data:)([^"']+)["']""",
        re.IGNORECASE,
    )
    for path in html_files():
        with open(path, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        for match in pattern.finditer(content):
            target = match.group(1).split("#")[0].split("?")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                line = content[: match.start()].count("\n") + 1
                problems.append(
                    "%s:%d references missing file %r" % (rel(path), line, target)
                )


def check_placeholders(problems):
    """No leftover template filler in published content."""
    for path in html_files():
        with open(path, encoding="utf-8", errors="replace") as fh:
            for number, line in enumerate(fh, start=1):
                for pattern in PLACEHOLDER_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        problems.append(
                            "%s:%d contains placeholder text matching /%s/"
                            % (rel(path), number, pattern)
                        )


def check_structured_data(problems):
    """Every JSON-LD block must be valid JSON."""
    pattern = re.compile(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        re.IGNORECASE | re.DOTALL,
    )
    for path in html_files():
        with open(path, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        for match in pattern.finditer(content):
            line = content[: match.start()].count("\n") + 1
            try:
                json.loads(match.group(1))
            except ValueError as error:
                problems.append("%s:%d has invalid JSON-LD: %s" % (rel(path), line, error))


def check_secrets(problems):
    """No key material in tracked text files."""
    for path in iter_repo_files():
        if not path.lower().endswith(SCAN_EXTENSIONS):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for number, line in enumerate(fh, start=1):
                for pattern in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        problems.append(
                            "%s:%d looks like it contains a secret (matched /%s/)"
                            % (rel(path), number, pattern)
                        )


def check_vendor_checksums(problems):
    """The vendored third-party libraries must be byte-for-byte as recorded."""
    import base64
    import hashlib

    for relative, expected in VENDOR_CHECKSUMS.items():
        path = os.path.join(ROOT, relative.replace("/", os.sep))
        if not os.path.exists(path):
            problems.append("%s is missing" % relative)
            continue
        with open(path, "rb") as fh:
            digest = base64.b64encode(hashlib.sha256(fh.read()).digest()).decode()
        if digest != expected:
            problems.append(
                "%s does not match the checksum in assets/VERSIONS.md "
                "(expected %s, got %s)" % (relative, expected, digest)
            )


def main():
    problems = []
    check_asset_references(problems)
    check_placeholders(problems)
    check_structured_data(problems)
    check_secrets(problems)
    check_vendor_checksums(problems)

    if problems:
        print("Static site checks FAILED (%d problem(s)):" % len(problems))
        for problem in problems:
            print("  - %s" % problem)
        return 1

    print("Static site checks passed: asset references, placeholder text, "
          "JSON-LD, secret scan and vendored library checksums.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
