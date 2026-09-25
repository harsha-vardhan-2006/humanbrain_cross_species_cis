import hashlib, os
files = [r'G:\humanbrain\full18\full8_1000um_optbal.nii.gz',
         r'G:\humanbrain\full18\full8_100um_optbal.nii.gz',
         r'G:\humanbrain\full18\full8_200um_optbal.nii.gz',
         r'G:\humanbrain\full18\full8_300um_optbal.nii.gz',
         r'G:\humanbrain\full18\full8_400um_optbal.nii.gz']
out = r'D:\HumanBrain\00_Metadata\CHECKSUMS_G_reference.sha256'
with open(out, 'w') as o:
    for f in files:
        h = hashlib.sha256()
        with open(f, 'rb') as fh:
            for c in iter(lambda: fh.read(1024 * 1024), b''):
                h.update(c)
        o.write(h.hexdigest() + '  ' + f + '\n')
        print('hashed', os.path.basename(f), os.path.getsize(f))
print('written', out)
