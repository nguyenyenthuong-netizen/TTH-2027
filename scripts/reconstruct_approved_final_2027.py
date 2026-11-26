#!/usr/bin/env python3
"""Reconstruct approved byte-exact mockups from immutable, checksum-verified sources."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import base64, mimetypes, subprocess, os, re, sys, tempfile

def digest(b): return sha256(b).hexdigest()
def checked(b, expected, name):
    assert digest(b)==expected,(name,digest(b),expected)
    return b
folder=Path("release-final-2027")
root=Path(sys.argv[1])
approved=Path("_release-approved")
patchfiles=[folder/"arch.patch.b64",folder/"hc.patch.b64"]
assert all(p.is_file() for p in patchfiles),"Both approved deltas are required"
with tempfile.TemporaryDirectory() as td:
    temp=Path(td)
    z=Path("pages-overrides/catalog/TTH-2027-V8-preview.zip")
    checked(z.read_bytes(),"fc44868aa5e678709dbc6f34da835ea543ce10afb9bd10f4f0966309fa27bd72","V8 original archive")
    with ZipFile(z) as f:
        s=f.read("index.html")
        for n in f.namelist():
            if n.startswith("assets/") and not n.endswith("/"):
                mime=mimetypes.guess_type(n)[0] or "application/octet-stream"
                s=s.replace(n.encode(),b"data:"+mime.encode()+b";base64,"+base64.b64encode(f.read(n)))
    arch_base=temp/"arch-base.html"
    arch_base.write_bytes(checked(s,"b1d34d2cbeb0107fb1b07d8064835e7eb14a8445ce0a096d317abaa1f761d4d2","architecture base"))
    hc_base=temp/"hc-base.html"
    expected_hc="1b83c6c62c16063ffcde5f2145e1f531c465dd4eab3716916fdc720f6a221feb"
    # Prefer deterministic reconstruction from the unchanged pre-FINAL build, rather than relying on an expiring artifact.
    raw=(root/"healthcare-website/index.html").read_bytes()
    if digest(raw)=="8644f1cadbcad3e408a26029aa6de5b607ff5be3c54a98452a76b693512ebdff":
        src=Path(".github/qa/healthcare_review_candidate.py").read_text("utf-8")
        code=src.split("with sync_playwright() as p:",1)[0]
        code,n=re.subn(r'with urlopen\(Request\(url,headers=\{"User-Agent":"TTH-2027-review/1.0"\}\),timeout=90\) as r:\n    raw=r.read\(\)',"raw=Path("+repr(str((root/'healthcare-website/index.html').resolve()))+").read_bytes()",code,count=1)
        assert n==1,"Candidate source reader changed"
        code=code.replace('out=Path("artifacts/healthcare-review")',"out=Path("+repr(str(temp/"base-review"))+")",1)
        exec(compile(code,"<verified-candidate-reconstruction>","exec"),{"__name__":"__main__"})
        generated=temp/"base-review/TTH-Healthcare-ban-duyet.html"
        if generated.is_file() and digest(generated.read_bytes())==expected_hc:
            hc_base.write_bytes(generated.read_bytes())
    if not hc_base.is_file():
        subprocess.run(["gh","run","download","45853840739","--repo","nguyenyenthuong-netizen/TTH-2027","--name","tth-healthcare-review-candidate","--dir",str(temp/"base-artifact")],check=True)
        hc_base.write_bytes(checked((temp/"base-artifact/TTH-Healthcare-ban-duyet.html").read_bytes(),expected_hc,"Healthcare review base"))
    for filename,basis,patch_sha,route,expected,size in [
        ("arch.patch.b64",arch_base,"4458f3672704b055dad38165000786d678d2a379ff66db2ffb4afc057a178693","kien-truc-thuong-hieu","b8499f4f774baff7904a453a9d17f8c8106ebf4fc57724ade191fc5633793571",34527312),
        ("hc.patch.b64",hc_base,"02bff0610ffeb7d065ef212210865de1d779e701f91dd7f56527d8c041d2d28c","healthcare-website","4326f4c79e1e66b4cc550221cc6ba39d2e2e7ddd7b6861797b3030800b3c9367",35406360)]:
        b64="".join((folder/filename).read_text("ascii").split())
        patch=temp/(filename+".zst")
        patch.write_bytes(checked(base64.b64decode(b64,validate=True),patch_sha,filename))
        dest=approved/route/"index.html"
        dest.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(["zstd","-q","-d","-f","--patch-from="+str(basis),str(patch),"-o",str(dest)],check=True)
        b=checked(dest.read_bytes(),expected,route)
        assert len(b)==size
        print("FINAL_RECONSTRUCT_VERIFIED",route,len(b),expected,flush=True)
