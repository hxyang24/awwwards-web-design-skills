"""Optional authoring step: remux our own VP8 packets into a seekable WebM.

Requires PyAV16.1.0 (used for this fixture), not a runtime/test dependency.
MediaRecorder output can omit duration metadata; no footage is fetched here.
"""
from pathlib import Path
import av,json,hashlib
R=Path(__file__).resolve().parents[1];folder=R/'page_skills/editorial/reference';source=folder/'three-beats.webm';target=folder/'three-beats.remux.webm'
if target.exists():raise SystemExit('Inspect existing authoring output before reuse')
original=hashlib.sha256(source.read_bytes()).hexdigest();count=0
with av.open(str(source))as input, av.open(str(target),'w',format='webm')as output:
 stream=output.add_stream_from_template(input.streams.video[0])
 for packet in input.demux(input.streams.video[0]):
  if packet.dts is None:continue
  packet.stream=stream;output.mux(packet);count+=1
with av.open(str(target))as input:
 duration=input.duration/av.time_base if input.duration is not None else None
 if not duration or not 5.5<duration<7.5:raise ValueError('Review the original media duration')
 if len(input.streams.audio):raise ValueError('The original study is silent')
 decoded=sum(1 for frame in input.decode(video=0))
if decoded<100:raise ValueError('Original motion fixture incomplete')
target.replace(source);origin=json.loads((folder/'media-origin.json').read_text(encoding='utf-8'));origin.update(raw_recorder_sha256=original,sha256=hashlib.sha256(source.read_bytes()).hexdigest(),bytes=source.stat().st_size,container_remux='Own VP8 packets only; PyAV '+av.__version__+', no re-encoding or external footage',finalizer='tools/finalize_reference_media.py',verified_seconds=duration,decoded_frames=decoded,remux_packets=count)
(folder/'media-origin.json').write_text(json.dumps(origin,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(origin))
