"""Fingerprint source bytes and framed encoded audio packets without modifying audio.

Run in an existing environment with PyAV, e.g. lecture-transcribe/.venv.
Equal audio_identity_sha256 means matching codec configuration, packet payloads,
packet time bases and timings. This does not assert classroom completeness.
"""
from __future__ import annotations
import argparse,hashlib,json,struct
from pathlib import Path
import av

def file_sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def fingerprint(path:Path)->dict:
    with av.open(str(path)) as c:
        stream=c.streams.audio[0]; cc=stream.codec_context
        config={'codec':cc.name,'sample_rate':cc.sample_rate,'channels':cc.channels,
                'layout':cc.layout.name,'extradata_hex':(cc.extradata or b'').hex(),
                'time_base':str(stream.time_base),'stream_start_time':stream.start_time}
        payload=hashlib.sha256();timing=hashlib.sha256();count=0;payload_bytes=0
        for packet in c.demux(stream):
            data=bytes(packet)
            if not data:continue
            payload.update(struct.pack('>Q',len(data)));payload.update(data)
            timing.update(json.dumps([packet.pts,packet.dts,packet.duration,str(packet.time_base)],separators=(',',':')).encode()+b'\n')
            count+=1;payload_bytes+=len(data)
        identity={'config':config,'packets':count,'framed_payload_sha256':payload.hexdigest(),'timing_sha256':timing.hexdigest()}
        return {'path':str(path),'bytes':path.stat().st_size,'file_sha256':file_sha256(path),
                'duration_seconds':c.duration/av.time_base if c.duration else None,**identity,
                'audio_identity_sha256':hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':')).encode()).hexdigest()}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('audio',type=Path,nargs='+');ap.add_argument('--out',type=Path)
    a=ap.parse_args();rows=[fingerprint(p) for p in a.audio]
    groups={}
    for i,r in enumerate(rows):groups.setdefault(r['audio_identity_sha256'],[]).append(i)
    data={'schema':'encoded-audio-identity-v1','method':'codec-config + length-framed audio packet bytes + packet timing','files':rows,'identical_audio_groups':[g for g in groups.values() if len(g)>1]}
    raw=json.dumps(data,ensure_ascii=False,indent=2)
    if a.out:a.out.write_text(raw,encoding='utf-8')
    print(raw)

if __name__=='__main__':main()
