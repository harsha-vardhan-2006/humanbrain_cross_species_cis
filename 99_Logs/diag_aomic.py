"""Diagnose the AOMIC download: check HTTP status/headers for the Zenodo content URL."""
import requests

URL = 'https://zenodo.org/api/records/19796783/files/connectomes_part_1.zip/content'

for ua in (None, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'):
    h = {} if ua is None else {'User-Agent': ua}
    try:
        r = requests.get(URL, headers=h, stream=True, timeout=(30, 60))
        print('UA:', ua, '-> status', r.status_code, '| len hdr:', r.headers.get('Content-Length'),
              '| final url:', r.url[:90])
        got = 0
        for c in r.iter_content(1 << 20):
            got += len(c)
            if got >= 3_000_000:
                break
        print('   received first', got, 'bytes OK')
        r.close()
    except Exception as e:
        print('UA:', ua, '-> ERROR', type(e).__name__, str(e)[:150])
