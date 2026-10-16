"""Rebuild every SVG asset + README.md.   pip install fonttools brotli pillow   then:  python design-src/build_all.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import gen_hero, gen_cards, gen_story, gen_projects, gen_stack, gen_extra
gen_hero.build(); gen_cards.buttons(); gen_cards.terminal(); gen_cards.impact()
gen_story.experience(); gen_story.blueprint()
for p in gen_projects.PROJECTS: gen_projects.card(p)
gen_stack.build(); gen_extra.cta(); gen_extra.stl()
import make_readme  # noqa: E402,F401
