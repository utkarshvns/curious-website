# Vendored assets

This site has no build step and no package manager, so every third-party
library is committed to the repository. This file records what is vendored,
where it came from, and a checksum so that an accidental edit or a corrupted
download is caught by CI.

The checksums below are SHA-256, base64 encoded (the same format used by
Subresource Integrity). `.github/scripts/check_site.py` verifies them on every
run, so **upgrading a library means updating this file in the same change**.

## Third-party libraries

| File                              | Library         | Version   | Source                                  |
| --------------------------------- | --------------- | --------- | --------------------------------------- |
| `assets/js/jquery.min.js`         | jQuery          | 3.7.1     | <https://code.jquery.com/jquery-3.7.1.min.js> |
| `assets/js/jquery.scrolly.min.js` | jQuery Scrolly  | 1.0.0-dev | <https://github.com/jquery/jquery-scrolly> |
| `assets/js/skel.min.js`           | skel            | 3.0.1     | <https://skel.io>                       |
| `assets/css/font-awesome.min.css` | Font Awesome    | 4.6.3     | <https://fontawesome.com/v4.6.3/>       |
| `assets/fonts/*`                  | Font Awesome webfonts | 4.6.3 | <https://fontawesome.com/v4.6.3/>       |

jQuery, jQuery Scrolly and skel remain vendored for checksum continuity and
are no longer loaded by the page.

## Checksums

```
/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=  assets/js/jquery.min.js
i2Vx6iw2Mf9Qu0uW5/kIHG4z66re+csspZVdXgtiWgI=  assets/js/jquery.scrolly.min.js
3e+NvOq+D/yeJy1qrWpYkEUr6SlOCL5mHpc2nZfX74E=  assets/js/skel.min.js
7Q8FEB1IBybFi81JVqHnsC8StTjQIFjxsOv9q+in70I=  assets/css/font-awesome.min.css
```

## Local template source

These are part of the site, not third-party downloads. They are edited freely
and are deliberately **not** checksummed.

- `assets/css/main.css` — TEMPLATED "Intensify" stylesheet
- `assets/js/util.js` — TEMPLATED jQuery plugins (`navList`, `panel`, `placeholder`)
- `assets/js/main.js` — page bootstrap (vanilla JS: menu, header state, section highlight)

## Template licence

The template is released under the Creative Commons Attribution 3.0 licence
(<https://templated.co/license>). The attribution comment at the top of
`index.html` and `assets/css/main.css` must be kept.
