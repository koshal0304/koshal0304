# Setup guide: Koshal's GitHub profile

Takes about 10 minutes. Everything is self-hosted in this repo: no third-party stats services that can rate-limit or go down.

## 1. Create the special profile repo

GitHub shows a README on your profile when a **public** repo has exactly the same name as your username.

1. Go to <https://github.com/new>
2. Repository name: **`koshal0304`** (exactly), set to **Public**, don't add a README
3. Create it

## 2. Push these files

Use git so the hidden `.github/` folder is included (drag-and-drop uploads often skip it):

```bash
git clone https://github.com/koshal0304/koshal0304.git
cd koshal0304
# copy everything from this folder (incl. .github/) into here, then:
git add -A
git commit -m "feat: new profile README"
git push
```

## 3. Turn on the live visuals (one click)

1. Open the repo → **Actions** tab → enable workflows if asked
2. Pick **Profile visuals** → **Run workflow**
3. After ~2 minutes it commits:
   - `profile-3d-contrib/*.svg`: the 3D contribution skyline
   - `assets/generated/snake-*.svg`: the contribution snake
   - `assets/generated/stats.svg`: the Neural-Dark stats card

It then refreshes twice a day on its own.

**If the push step fails with 403:** Settings → Actions → General → Workflow permissions → **Read and write permissions** → Save, then run it again.

## 4. Profile settings (high impact for recruiters)

Go to <https://github.com/settings/profile>:

| Field | Suggested value |
|---|---|
| Profile picture | your headshot (same photo as the README) |
| Name | Koshal Kumar |
| Bio (160 chars) | `AI Engineer · production LLM systems: LangGraph agents, RAG, NL→SQL, evals · open to AI/LLM Engineer roles` |
| Company | `@ Alphabetum Technology` |
| Location | Bengaluru, India |
| Website | https://myportfoliodsjfv.netlify.app/ |
| Social | your LinkedIn URL |

Also tick **"Include private contributions on my profile"** (Settings → Public profile → Contributions & activity). Most of your production work is in private repos, so this makes your contribution graph and 3D skyline look much fuller.

## 5. Pinned repos: add descriptions + topics

Your pinned repos currently have no descriptions. Click ⚙ next to "About" on each repo:

| Repo | Description | Topics |
|---|---|---|
| personal-knowledge-assistant | RAG chatbot over your own documents: Gemini, LangChain, BGE embeddings, Pinecone, Streamlit | `rag` `llm` `langchain` `gemini` `pinecone` |
| Hiring-Assistant | TalentScout: Gemini-powered candidate screening with tech-stack-specific questions and SHA-256 PII anonymization | `llm` `gemini` `streamlit` `hr-tech` |
| webcamyolodetector | YOLO Vision Pro: real-time YOLOv8 object detection (ONNX Runtime) for images and live webcam | `yolov8` `onnx` `computer-vision` |
| genai | RTSP camera capture + Gemini vision for automated phone-usage detection | `gemini` `computer-vision` `rtsp` |

Add the website/live-demo link in each repo's About box too. If your CLIP + FAISS image-search project has a repo, pin it as well and point its card in `README.md` to the repo instead of the demo.

## 6. Editing later

- **Text-only tweaks** (links, table rows, the about paragraph): edit `README.md` directly.
- **Visual cards** (new job, new metric, new project): edit the data at the top of the matching file in `design-src/` and rebuild:

  ```bash
  pip install fonttools brotli pillow
  python design-src/build_all.py
  ```

  | File | Builds |
  |---|---|
  | `gen_hero.py` | hero banner (name, typing lines, photo orbits) |
  | `gen_cards.py` | buttons, terminal, impact metrics |
  | `gen_story.py` | experience timeline (`ROLES`), system blueprint |
  | `gen_projects.py` | project cards (`PROJECTS`) |
  | `gen_stack.py` | tech stack + rotating 3D core (`STACK`) |
  | `gen_extra.py` | contact banner, 3D STL monogram |
  | `README.template.md` | the README source (`build_all.py` regenerates `README.md` from it) |

  If you build, edit `README.template.md` rather than `README.md`, or your edits get overwritten.

## What's in here

```
README.md                         profile page
assets/*.svg                      animated, self-contained SVGs (fonts embedded, no JS)
assets/model/koshal-monogram.stl  3D model (GitHub renders it interactively)
assets/generated/                 refreshed by the workflow
profile-3d-contrib/               refreshed by the workflow
scripts/generate_stats.py         stats card generator (GitHub GraphQL API)
.github/workflows/                automation
design-src/                       sources for every visual
```

Resume note: the README leaves out your phone number on purpose. If you'd like a "Download resume" button, export a version without your phone number and add it as `assets/Koshal_Kumar_Resume.pdf`.
