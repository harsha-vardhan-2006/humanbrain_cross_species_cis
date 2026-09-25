# BigBrain source throughput + dual-host acquisition notes

Observed during the 2015 full-resolution coronal acquisition (7,404 PNGs, ~64 GB).

## Measured client link capacity
| Test | Result |
|---|---|
| `speed.cloudflare.com` 30–50 MB while downloads active | 3.17–3.76 MB/s |
| Client link is therefore **not** the constraint | — |

## Measured BigBrain server behaviour (per IP)
| Configuration | Aggregate |
|---|---|
| 1 HTTPS stream, idle server | ~50 KB/s |
| 4 streams (`dl_batch`, main host) | ~265 KB/s |
| 4 main + 4 mirror streams (dual-host) | **~463 KB/s** |
| +8 extra streams to main host | +22 KB/s (no gains) |
| +8 extra streams to mirror | +22 KB/s (no gains) |

Conclusion: `ftp.bigbrainproject.org` rate-limits our IP to roughly **50–65 KB/s per
connection**, and the rate degrades further over a session (bursts of 2.7–3.75 MB/s were
observed early on, dropping to the values above later). Adding connections beyond ~4 per
host does not help.

## Dual-host strategy (adopted)
The same `BigBrainRelease.2015` tree is served by two independent hosts:

* primary: `https://ftp.bigbrainproject.org/bigbrain-ftp/`
* mirror:  `https://bigbrain-ftp.loris.ca/bigbrain-ftp/` (LORIS, McGill)

Because each host throttles independently, the remaining coronal files are split in half
(`split_coronal.py`) and fetched concurrently — one downloader per host, disjoint file sets:

* `dl_F_coronal_main.txt`   — even slots, primary host URLs
* `dl_F_coronal_mirror.txt` — odd slots, mirror URLs (same destination paths)

Both downloaders append to the same `download_manifest.csv`. Concurrent appends were
validated: 0 malformed rows across 3,400+ rows. Each file is size-verified against the
official size from the server listings, so a mirror file that differs in length is
quarantined rather than accepted. `verify_downloads.py` subsequently applies the normal
structural checks (PNG signature + IEND) to mirror-sourced files exactly as to primary ones.

## Mirror integrity evidence
`mirror_equiv1.py` re-downloaded `pm0001o.png` from the mirror and compared SHA-256 against
the locally downloaded (already size- and structure-verified) copy:

```
pm0001o.png local_sha=e9577cf07c4483c9 mirror_sha=e9577cf07c4483c9
            mirror_bytes=72465 local_bytes=72465 EQUAL=True
```

=> the LORIS mirror serves byte-identical content to the primary host. Mirror-sourced files
are additionally size-checked against the official server listing and pass the same
PNG signature/IEND verification as primary-sourced files.

## Consequence
Coronal full-resolution PNGs complete at the server-limited ~0.45 MB/s. There is no known
CDN-backed third source for the 2015 2D sections; the two academic hosts above are the only
mirrors. Throughput is the sole remaining constraint, not correctness — all downloads are
resumable, size-verified and structurally validated.

