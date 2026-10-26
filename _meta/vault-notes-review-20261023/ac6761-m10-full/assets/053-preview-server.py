from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
OUT=Path(__file__).parent
DEPS=Path(r'E:\app-data\diagram-tools\node_modules')
CANDIDATE=OUT.parent/'ac6761-m10-full/author/candidate-v1.md'
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(OUT),**kwargs)
    def do_GET(self):
        files={'/candidate.md':CANDIDATE,'/marked.js':DEPS/'marked/lib/marked.umd.js','/mermaid.js':DEPS/'mermaid/dist/mermaid.min.js','/katex.js':DEPS/'katex/dist/katex.min.js','/auto-render.js':DEPS/'katex/dist/contrib/auto-render.min.js','/katex.css':DEPS/'katex/dist/katex.min.css'}
        path=self.path.split('?')[0]
        if path in files:
            p=files[path]; b=p.read_bytes(); self.send_response(200); self.send_header('Content-Type','text/css' if path.endswith('.css') else 'text/javascript' if path.endswith('.js') else 'text/plain; charset=utf-8'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
        elif path.startswith('/fonts/'):
            p=DEPS/'katex/dist/fonts'/Path(path).name
            if p.exists():
                b=p.read_bytes(); self.send_response(200); self.end_headers(); self.wfile.write(b)
            else: self.send_error(404)
        else: super().do_GET()
print('M10 own preview http://127.0.0.1:8811/preview.html',flush=True)
ThreadingHTTPServer(('127.0.0.1',8811),Handler).serve_forever()
