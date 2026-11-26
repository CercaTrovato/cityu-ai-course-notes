from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
o=Path(__file__).parent
fs=sorted((o/'pages').glob('p-*.png'))
(o/'sheets').mkdir(exist_ok=True)
for i in range(0,len(fs),2):
    sh=Image.new('RGB',(1250,1460),'white')
    for j,f in enumerate(fs[i:i+2]):
        im=ImageOps.contain(Image.open(f),(1250,690))
        sh.paste(im,(0,j*730+30))
        ImageDraw.Draw(sh).text((5,j*730+5),'p.'+str(i+j+1),fill='black')
    sh.save(o/'sheets'/('sheet%02d.png'%(i//2+1)))
print(len(fs))
