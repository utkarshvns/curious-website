# curious-website

Personal portfolio website for **Utkarsh Yadav**.

- **Live site:** https://yadavutkarsh.com
- **Fallback URL:** https://utkarshvns.github.io/curious-website/

> Hi, welcome to my website. To learn more about me, visit
> [www.yadavutkarsh.com](https://yadavutkarsh.com).

---

## Stack

Plain static HTML, CSS and JavaScript. There is **no build step and no package
manager** — the files in this repository are exactly what gets published.

| Part      | Detail                                                                              |
| --------- | ----------------------------------------------------------------------------------- |
| Markup    | Hand-written HTML5 (`index.html`)                                                   |
| Styling   | TEMPLATED "Intensify" `main.css`, Font Awesome 4.6.3, Montserrat / Open Sans / Pacifico webfonts |
| Behaviour | jQuery 3.7.1, jQuery Scrolly, skel 3.0.1 (`assets/js`)                            |
| Hosting   | GitHub Pages, published from the `main` branch, repository root                    |
| Domain    | `yadavutkarsh.com`, configured through the `CNAME` file                            |

## Project structure

```
.
├── index.html              # the only page
├── CNAME                   # custom domain for GitHub Pages
├── robots.txt              # crawler policy + sitemap pointer
├── sitemap.xml             # sitemap for search engines
├── .nojekyll               # publish the files as-is, without a Jekyll build
├── .gitignore
├── AGENTS.md               # rules for coding agents working on this repo
├── opencode.jsonc          # OpenCode permissions and the review / dev agents
├── assets/
│   ├── css/main.css
│   ├── css/font-awesome.min.css
│   ├── fonts/              # Font Awesome webfonts
│   └── js/                 # jquery, scrolly, skel, util, main
└── images/                 # profile photo, card images, favicon
```

## Running it locally

There is nothing to compile. Serve the repository root over HTTP (opening the
file directly also works, but a local server matches production more closely):

```powershell
python -m http.server 8000
```

Then open <http://localhost:8000/index.html>. Stop the server with `Ctrl+C`.

> On Windows, PowerShell blocks `.ps1` shims on some machines. If `npx` or
> `npm` reports a script-execution error, use `npx.cmd` / `npm.cmd` instead.

## How deployment works

1. GitHub Pages is configured to publish the **`main` branch, repository root**
   (Settings → Pages → Source: *Deploy from a branch*).
2. Every push to `main` triggers GitHub's `pages-build-deployment` workflow,
   which publishes the site. `.nojekyll` makes it publish the files as-is
   instead of running a Jekyll build.
3. The custom domain comes from the `CNAME` file. The `www` variant and the
   `*.github.io` URL both resolve to the same site.
4. **Merging to `main` publishes immediately.** There is no manual deploy step.

The workflow runs at
`github.com/utkarshvns/curious-website/actions` and can be watched from there.

### Before merging

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs a static site gate
on every pull request and on every push. It runs
[`.github/scripts/check_site.py`](.github/scripts/check_site.py) (local asset
references, placeholder text, JSON-LD, a secret scan and vendored-library
checksums) and then runs [`html-validate`](https://html-validate.org/) against
the HTML. The workflow does **not** deploy — the Pages deployment is unchanged —
but it catches broken markup, missing images, tampered vendored libraries and
regressions before they reach `main`.

## Verifying a change

There is no test suite, so these are the checks that stand in for one. All of
them run from the repository root.

```powershell
# 1. Serve the site and look at it
python -m http.server 8000     # http://localhost:8000/index.html

# 2. One-command check (same as CI)
python .github\scripts\check_site.py

# 3. HTML validation (matches CI)
npx.cmd --yes html-validate@9 index.html

# 4. Every local src/href must resolve to a file that exists
$missing = @(); Get-ChildItem -Filter *.html | ForEach-Object { $f = $_
  [regex]::Matches((Get-Content $f.FullName -Raw),
    '(?:src|href)="(?!https?:|#|mailto:|tel:)([^"]+)"') | ForEach-Object {
 $p = $_.Groups[1].Value.Split('#')[0]
      if ($p -and -not (Test-Path (Join-Path $f.DirectoryName $p))) {
        $missing += "$($f.Name) -> $p" } } }
$missing; if (-not $missing) { "OK - no broken local asset references" }

# 5. No leftover template placeholder text
git grep -n -i -E "lorem ipsum|untitled\.tld|somewhere road|\(000\) 000-0000" -- '*.html'
```

# 4. No secrets slipped into the diff
git diff | Select-String -Pattern '(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*["''][^"'']{8,}'
```

## Working with agents

This repository is configured for [OpenCode](https://opencode.ai). See
[`AGENTS.md`](AGENTS.md) for the rules an agent must follow, and
[`opencode.jsonc`](opencode.jsonc) for the permissions.

Two agents are defined:

- **`review`** (the default) — read-only. Inspects the repository and reports
  findings. It cannot edit files, commit, push, merge or install packages.
- **`dev`** — implements one scoped change, verifies it locally, and stops
  before committing.

Useful prompts:

```
Use the review agent to inspect the site and report anything broken.

Use the dev agent to add a Projects section to index.html. Do not commit.
```

Shell commands need approval by default. Read-only Git inspection
(`git status`, `git diff`, `git log`, `git show`, `git branch`) is allowed
without a prompt; commits, pushes, merges, package installs and anything
destructive are not.

## Changing the site

1. Start from a clean tree and update `main`.
2. Create a feature branch.
3. Ask an agent to inspect and propose a change.
4. Implement one clearly scoped improvement.
5. Run the verification commands above and review the diff.
6. Open a pull request.
7. Merge only after review — merging publishes.
8. Check the live site.

```powershell
git status
git fetch origin
git switch main
git pull --ff-only origin main
git switch -c feature/short-slug
# ... make the change, then verify ...
git diff
git add -A
git commit -m "Short, factual description of the change"
git push -u origin feature/short-slug
```

## License

The page markup and styles are based on the TEMPLATED "Intensify" template,
released under the Creative Commons Attribution 3.0 license
(<https://templated.co/license>).
