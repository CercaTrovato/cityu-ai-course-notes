from pathlib import Path
import hashlib, re, subprocess
from PIL import Image, ImageDraw
root=Path('D:/上课资料/CityU/EF5560_Fintech_and_AI_in_Finance')
out=Path('E:/app-data/codex/scratchpad/ef5560-final-20261128/independent-review')
jobs=[('m11',root/'course_files_export/canvas-20261118/Lec11_Lending_and_Crowdfunding.pdf',[39,45,46,47,49,50,52]),('m12',root/'course_files_export/canvas-20261126-review/Lec12_Robo_Cybersecurity_and_RegTech.pdf',[24,26,27,29,30,31,32,33,34,35,36,37,38])]
for name,path,pages in jobs:
    images=[]; texts=[]
    for p in pages:
        prefix=out/f'{name}-p{p}'
        subprocess.run(['D:/poppler/Library/bin/pdftoppm.exe','-f',str(p),'-l',str(p),'-r','110','-singlefile','-png',str(path),str(prefix)],check=True,capture_output=True)
        file=prefix.with_suffix('.png')
        images.append((p,file))
        raw=subprocess.run(['D:/poppler/Library/bin/pdftotext.exe','-f',str(p),'-l',str(p),'-layout',str(path),'-'],check=True,capture_output=True).stdout.decode('utf-8')
        texts.append(f'PAGE {p}\n{raw}')
    (out/f'{name}-sample-source.txt').write_text('\n\n'.join(texts),encoding='utf-8')
    for ix in range(0,len(images),4):
        batch=images[ix:ix+4]
        ims=[Image.open(f).convert('RGB') for p,f in batch]
        w=max(im.width for im in ims); h=max(im.height for im in ims)
        sheet=Image.new('RGB',(2*w,2*(h+35)), 'white'); draw=ImageDraw.Draw(sheet)
        for j,((p,f),im) in enumerate(zip(batch,ims)):
            x=(j%2)*w; y=(j//2)*(h+35)
            draw.text((x+8,y+8),f'{name} physical p{p}',fill='black')
            sheet.paste(im,(x,y+35))
        sheet.save(out/f'{name}-source-sheet-{ix//4+1}.png')
    print(name,'PDF SHA',hashlib.sha256(path.read_bytes()).hexdigest(),'pages',pages)
text=Path('E:/app-data/codex/outputs/ef5560-final-20261128/public-source/M11-M12-transcript-source35-redacted.txt').read_text(encoding='utf-8')
print('TRANSCRIPT START',repr(text[:450]))
