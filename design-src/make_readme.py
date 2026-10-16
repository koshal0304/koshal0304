import os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
tpl = open(os.path.join(HERE, "README.template.md"), encoding="utf-8").read()
stl = open(os.path.join(ROOT, "assets", "model", "koshal-monogram.stl"), encoding="utf-8").read()
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(tpl.replace("{{STL}}", stl))
print("README.md written")
