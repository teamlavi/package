import base64

pkgs = [
    "cGlw:dXJsbGliMw==:MS45LjE=",
      "cGlw:cmVxdWVzdHM=:Mi45LjI=",
      "cGlw:Ym90bzM=:MS45Ljk5",
      "cGlw:cGlw:OS4wLjM=",
      "cGlw:bnVtcHk=:MS45LjM=",
      "cGlw:cHk=:MS45LjA=",
      "cGlw:aHR0cGxpYjI=:MC45LjI=",
      "cGlw:bXlzcWwtY29ubmVjdG9yLXB5dGhvbg==:OC4wLjY=",
      "cGlw:cHl6bXE=:MjQuMC4x",
      "cGlw:aHR0cHg=:MC45LjU=",
      "cGlw:anVweXRlci1jbGllbnQ=:Ny40Ljc=",
      "cGlw:bmJjb252ZXJ0:Ny4yLjU=",
      "cGlw:ZmFzdGFwaQ==:MC45LjE=",
      "cGlw:cmV0cnk=:MC45LjI=",
      "cGlw:aXB5a2VybmVs:Ni45LjI=",
      "cGlw:bmJjbGllbnQ=:MC43LjI=",
      "cGlw:dXZpY29ybg==:MC45LjE=",
      "cGlw:bm90ZWJvb2s=:Ni41LjI=",
      "cGlw:cHljcnlwdG8=:Mi42LjE=",
      "cGlw:aXB5d2lkZ2V0cw==:OC4wLjI=",
      "cGlw:anVweXRlci1zZXJ2ZXI=:MS45LjA=",
      "cGlw:Z3JlbWxpbnB5dGhvbg==:My42LjE=",
      "cGlw:cHl0ZXN0LWZvcmtlZA==:MS40LjA=",
      "cGlw:dG94:My45LjA=",
      "cGlw:bmJjbGFzc2lj:MC40Ljg=",
      "cGlw:bm90ZWJvb2stc2hpbQ==:MC4yLjI=",
      "cGlw:ZGphbmdvcmVzdGZyYW1ld29yaw==:My45LjQ=",
      "cGlw:YXp1cmUtY2xpLWNvcmU=:Mi45LjE=",
      "cGlw:cHl0b3JjaC1saWdodG5pbmc=:MS44LjM=",
      "cGlw:cXRjb25zb2xl:NS40LjA=",
      "cGlw:dGFibGVhdXNlcnZlcmNsaWVudA==:MC45LjA=",
      "cGlw:anVweXRlci1jb25zb2xl:Ni40LjQ=",
      "cGlw:anVweXRlcg==:MS4wLjA=",
      "cGlw:cHl0ZXN0LWh0bWw=:My4yLjA="
]
out = []
for pkg in pkgs:
    _, name, version = pkg.split(":")
    out.append(str(base64.b64decode(name)) + "==" + str(base64.b64decode(version)))

print (out)