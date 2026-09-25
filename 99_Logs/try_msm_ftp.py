"""Final MSM-tar alternative-source sweep: DataLad/OSF/EBRAINS/Zenodo mirrors."""
import requests, sys

EXPECT = 264898560
URLS = [
    # OSF mirrors
    'https://osf.io/download/BigBrain1_MSM_2023/',
    # EBRAINS
    'https://data.ebrain.eu/bucket/BigBrainRelease.2015/BigBrain1_MSM_2023.tar',
    # Dataverse / Zenodo search-based candidates
    'https://zenodo.org/records/10159314/files/BigBrain1_MSM_2023.tar',
    'https://zenodo.org/records/8423140/files/BigBrain1_MSM_2023.tar',
    # CONP / Loris direct
    'https://bigbrain-ftp.loris.ca/bigbrain-ftp/BigBrainRelease.2015/BigBrain1_MSM_2023.tar?download=1',
    'https://bigbrain-ftp.loris.ca/bigbrain-ftp/BigBrainRelease.2015/BigBrain1_MSM_2023.tar/download',
]

for u in URLS:
    try:
        r = requests.get(u, timeout=25, stream=True,
                         headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        cl = r.headers.get('content-length')
        head = next(r.iter_content(512), b'')
        real = (r.status_code == 200 and cl and head[:4] != b'<htm' and b'html' not in head[:100].lower())
        print(f'{r.status_code} cl={cl} head={head[:24]!r} {u[:70]}')
        r.close()
        if real:
            print('WORKING SOURCE FOUND:', u)
            sys.exit(0)
    except Exception as e:
        print(f'EXC {type(e).__name__}: {str(e)[:80]} {u[:70]}')
print('NO ALTERNATIVE SOURCE AVAILABLE')
