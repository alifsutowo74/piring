# Copies the app page (src/piring.html) into the Android app as a full offline page.
import re, pathlib
root = pathlib.Path(__file__).parent
src = (root / "src/piring.html").read_text()
body = src.replace("const STANDALONE = false;", "const STANDALONE = true;")
assert "const STANDALONE = true;" in body
title = re.search(r"<title>.*?</title>", body).group(0)
body = body.replace(title, "", 1)
head = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{title}
<style>body{{margin:0;font-size:14px;font-family:system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head><body>
"""
out = root / "android/app/src/main/assets/index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(head + body + "\n</body></html>\n")
print("wrote", out)
