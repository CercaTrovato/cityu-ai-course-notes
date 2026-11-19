from pathlib import Path
from zipfile import ZipFile
import hashlib,json,xml.etree.ElementTree as ET
R=Path('D:/上课资料/CityU');S=Path(__file__).resolve().parent;P=R/'IS6400_Business_Data_Analytics/course_files_export/canvas-20261118/Sample Final.docx'
h=lambda b:hashlib.sha256(b).hexdigest()
assert h(P.read_bytes())=='04ac67e3e3aa92ab2fff2895fde321d22d091e70d1b24fd1f7f202562e5fe0e7'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(P) as z:
    root=ET.fromstring(z.read('word/document.xml'));body=root.find('w:body',ns)
    out=[];tables=[];paras=[]
    for child in body:
        text=''.join(x.text or '' for x in child.iter() if x.tag.endswith('}t'))
        if child.tag.endswith('}p'):out.append(text);paras.append(text)
        elif child.tag.endswith('}tbl'):
            rows=[[''.join(x.text or '' for x in c.iter() if x.tag.endswith('}t')) for c in row.findall('w:tc',ns)] for row in child.findall('w:tr',ns)]
            tables.append(rows);out+=['TABLE:']+[' | '.join(row) for row in rows]
    images=[]
    for member in z.namelist():
        if member.startswith('word/media/'):
            b=z.read(member);dest=S/'source-media'/Path(member).name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(b)
            images.append({'member':member,'local':str(dest),'sha256':h(b),'bytes':len(b)})
    report={'source':str(P),'source_sha256':h(P.read_bytes()),'paragraphs':paras,'native_tables':tables,'media':images,'embedded_objects':[n for n in z.namelist() if n.startswith('word/embeddings/')],'source_package_members':len(z.namelist())}
(S/'source-extraction.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(S/'source-extracted-text.txt').write_text('\n\n'.join(out),encoding='utf-8')
print('\n\n'.join(out));print(json.dumps({'tables':len(tables),'images':images,'embedded_objects':report['embedded_objects']},ensure_ascii=False,indent=2))
