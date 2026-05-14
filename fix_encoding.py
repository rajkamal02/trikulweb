# encoding: utf-8
import re
with open(r'D:\All Projects\trikul-academy\public\index.html', 'r', encoding='latin-1') as f:
    raw = f.read()
# Latin-1 mojibake ko UTF-8 mein convert karo
try:
    fixed = raw.encode('latin-1').decode('utf-8')
    print('Encoding fix: SUCCESS')
except:
    fixed = raw
    print('Encoding fix: skipped')
with open(r'D:\All Projects\trikul-academy\public\index.html', 'w', encoding='utf-8') as f:
    f.write(fixed)
print('DONE!')
