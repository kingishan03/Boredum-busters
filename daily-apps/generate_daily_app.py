import html
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY_ROOT = ROOT / "daily-apps"
STATE_FILE = DAILY_ROOT / "state.json"
START_MARKER = "<!-- DAILY_APPS_START -->"
END_MARKER = "<!-- DAILY_APPS_END -->"

IDEAS = [
    {
        "slug": "pocket-riddles",
        "title": "Pocket Riddles",
        "kind": "game",
        "icon": "🧩",
        "tag": "BRAIN TEASER",
        "description": "Crack a quick riddle with a hint if you get stuck.",
        "mode": "riddle",
        "items": [
            {"prompt": "What has a face and two hands but no arms or legs?", "hint": "You might wear one on your wrist.", "answer": "A clock"},
            {"prompt": "What gets wetter the more it dries?", "hint": "It lives near the sink or shower.", "answer": "A towel"},
            {"prompt": "What has many keys but cannot open a single lock?", "hint": "It can make beautiful music.", "answer": "A piano"},
            {"prompt": "What has one eye but cannot see?", "hint": "It helps pull thread through fabric.", "answer": "A needle"},
            {"prompt": "What goes up but never comes back down?", "hint": "You celebrate it once a year.", "answer": "Your age"},
        ],
    },
    {
        "slug": "tiny-quest",
        "title": "Tiny Quest",
        "kind": "game",
        "icon": "🗺️",
        "tag": "MINI CHALLENGE",
        "description": "Pick a tiny real-world quest and collect a point when you finish.",
        "mode": "quest",
        "items": [
            {"prompt": "Find something nearby that is your favorite color."},
            {"prompt": "Stretch your arms up high and take one slow breath."},
            {"prompt": "Think of one small thing you are grateful for."},
            {"prompt": "Draw a tiny star without lifting your pen."},
            {"prompt": "Tidy one small spot for just one minute."},
            {"prompt": "Name three things you can hear right now."},
        ],
    },
    {
        "slug": "this-or-that",
        "title": "This or That",
        "kind": "game",
        "icon": "↔️",
        "tag": "QUICK PICK",
        "description": "Make a choice on a series of delightfully difficult dilemmas.",
        "mode": "choice",
        "items": [
            {"prompt": "Which would you choose?", "choices": ["Explore the ocean", "Explore outer space"]},
            {"prompt": "Pick your perfect day:", "choices": ["Endless summer", "Cozy winter"]},
            {"prompt": "Choose a new skill:", "choices": ["Speak every language", "Play every instrument"]},
            {"prompt": "Choose a sidekick:", "choices": ["A tiny dragon", "A clever robot"]},
            {"prompt": "Your weekend adventure:", "choices": ["A cabin in the woods", "A night in a castle"]},
        ],
    },
    {
        "slug": "joke-jar",
        "title": "Joke Jar",
        "kind": "game",
        "icon": "😄",
        "tag": "GIGGLE BREAK",
        "description": "Open the jar for a kid-friendly joke and a little laugh.",
        "mode": "reveal",
        "button": "Tell me another",
        "items": [
            {"prompt": "Why did the bicycle fall over?", "answer": "It was two-tired."},
            {"prompt": "What do you call a sleeping dinosaur?", "answer": "A dino-snore!"},
            {"prompt": "Why did the math book look sad?", "answer": "It had too many problems."},
            {"prompt": "What kind of tree fits in your hand?", "answer": "A palm tree."},
            {"prompt": "Why did the cookie visit the doctor?", "answer": "It was feeling crumby."},
        ],
    },
    {
        "slug": "story-spark",
        "title": "Story Spark",
        "kind": "tool",
        "icon": "📖",
        "tag": "GET CREATIVE",
        "description": "Grab a surprising story starter and see where your imagination goes.",
        "mode": "prompt",
        "button": "Spark another story",
        "items": [
            {"prompt": "A tiny door appears in the trunk of an ordinary tree."},
            {"prompt": "The moon sends you a postcard with a very strange map."},
            {"prompt": "A library book whispers your name when you open it."},
            {"prompt": "Your shadow starts dancing a few seconds before you do."},
            {"prompt": "A lost robot asks you to help it find the color blue."},
            {"prompt": "Every clock in town stops at the exact same moment."},
        ],
    },
    {
        "slug": "micro-trivia",
        "title": "Micro Trivia",
        "kind": "game",
        "icon": "💡",
        "tag": "TRIVIA",
        "description": "Answer bite-size questions from science, nature, and the world.",
        "mode": "quiz",
        "items": [
            {"prompt": "Which planet is closest to the Sun?", "choices": ["Mercury", "Venus", "Mars"], "answer": "Mercury"},
            {"prompt": "How many sides does an octagon have?", "choices": ["Six", "Eight", "Ten"], "answer": "Eight"},
            {"prompt": "Which animal is the largest mammal?", "choices": ["African elephant", "Blue whale", "Giraffe"], "answer": "Blue whale"},
            {"prompt": "What is the chemical symbol for water?", "choices": ["CO2", "H2O", "O2"], "answer": "H2O"},
            {"prompt": "Which season comes after spring?", "choices": ["Autumn", "Winter", "Summer"], "answer": "Summer"},
        ],
    },
    {
        "slug": "activity-picker",
        "title": "Activity Picker",
        "kind": "tool",
        "icon": "🎲",
        "tag": "NEED AN IDEA?",
        "description": "Let the picker choose a simple, screen-free mini activity.",
        "mode": "prompt",
        "button": "Pick another",
        "items": [
            {"prompt": "Make up a secret handshake."},
            {"prompt": "Build the tallest tower you can from nearby objects."},
            {"prompt": "Invent a new holiday and decide how people celebrate it."},
            {"prompt": "Take a five-minute walk and notice something new."},
            {"prompt": "Draw a map of an imaginary island."},
            {"prompt": "Make up a 10-second dance move."},
            {"prompt": "Write down three things you want to learn."},
        ],
    },
    {
        "slug": "kindness-generator",
        "title": "Kindness Generator",
        "kind": "tool",
        "icon": "💛",
        "tag": "GOOD VIBES",
        "description": "Get one small, thoughtful idea to brighten someone's day.",
        "mode": "prompt",
        "button": "Another idea",
        "items": [
            {"prompt": "Send someone a message telling them something you appreciate."},
            {"prompt": "Let someone go first and give them a friendly smile."},
            {"prompt": "Thank someone who helped you recently."},
            {"prompt": "Share a favorite song, book, or joke with a friend."},
            {"prompt": "Leave a kind note for someone to find."},
        ],
    },
]


APP_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#19152e" />
    <title>__TITLE__ — Boredom-Busters</title>
    <style>
      * { box-sizing: border-box; }
      body { display: grid; min-height: 100vh; place-items: center; margin: 0; padding: 22px 14px; background: radial-gradient(ellipse at 20% 5%, #453565, transparent 48%), #19152e; color: #fbf8ff; font-family: Arial, sans-serif; }
      main { width: min(100%, 620px); }
      .topbar { display: flex; justify-content: space-between; align-items: center; gap: 14px; margin-bottom: 16px; }
      .topbar a { color: #cbbaff; font-weight: 700; }
      h1 { margin: 0; font-size: clamp(1.7rem, 7vw, 2.7rem); letter-spacing: -0.04em; }
      .panel { padding: clamp(20px, 6vw, 34px); border: 1px solid rgb(255 255 255 / 13%); border-radius: 22px; background: #25203b; box-shadow: 0 18px 48px rgb(0 0 0 / 28%); text-align: center; }
      .icon { display: grid; width: 64px; height: 64px; place-items: center; margin: 0 auto 15px; border-radius: 20px; background: rgb(203 186 255 / 12%); font-size: 2rem; }
      .description { color: #c4bfd4; line-height: 1.55; }
      #prompt { margin: 26px 0; color: #fff; font-size: clamp(1.3rem, 5vw, 1.9rem); font-weight: 800; line-height: 1.45; }
      #extra { min-height: 1.4em; color: #cbbaff; }
      .actions { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }
      button { min-height: 46px; padding: 10px 16px; border: 0; border-radius: 11px; background: linear-gradient(110deg, #c2adff, #ffa0ce); color: #201830; font: inherit; font-weight: 800; cursor: pointer; }
      button:hover { filter: brightness(1.08); transform: translateY(-1px); }
      button:focus-visible, a:focus-visible { outline: 3px solid white; outline-offset: 3px; }
      #score { margin: 18px 0 0; color: #a9efd8; font-weight: 700; }
      .site-logo { position: fixed; top: 12px; left: 12px; z-index: 1000; display: block; width: 52px; height: 52px; }
      .site-logo img { display: block; width: 100%; height: 100%; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 16px rgb(0 0 0 / 28%); }
      .topbar { padding-left: 60px; }
      @media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0.01ms !important; scroll-behavior: auto !important; } }
    </style>
  </head>
  <body>
    <a class="site-logo" href="../../../home.html" aria-label="Boredom-Busters home"><img src="../../../Website logo.png" alt="" /></a>
    <main>
      <header class="topbar"><h1>__TITLE__</h1><a href="../../home.html">All apps</a></header>
      <section class="panel" aria-label="__TITLE__">
        <div class="icon" aria-hidden="true">__ICON__</div>
        <p class="description">__DESCRIPTION__</p>
        <p id="prompt"></p>
        <div id="actions" class="actions"></div>
        <p id="extra" aria-live="polite"></p>
        <p id="score" role="status" aria-live="polite"></p>
      </section>
    </main>
    <script>
      const app = __CONFIG__;
      const prompt = document.querySelector("#prompt");
      const actions = document.querySelector("#actions");
      const extra = document.querySelector("#extra");
      const scoreDisplay = document.querySelector("#score");
      let index = 0;
      let points = 0;
      let revealed = false;
      function current() { return app.items[index]; }
      function button(label, onClick) {
        const element = document.createElement("button");
        element.type = "button";
        element.textContent = label;
        element.addEventListener("click", onClick);
        actions.append(element);
      }
      function next() {
        index = (index + 1) % app.items.length;
        revealed = false;
        render();
      }
      function render() {
        const item = current();
        prompt.textContent = item.prompt;
        actions.replaceChildren();
        extra.textContent = "";
        scoreDisplay.textContent = app.mode === "quest" ? `Quests completed: ${points}` : "";
        if (app.mode === "riddle" || app.mode === "reveal") {
          button(revealed ? "Next one" : app.mode === "riddle" ? "Show hint" : "Reveal answer", () => {
            if (revealed) return next();
            revealed = true;
            extra.textContent = app.mode === "riddle" ? item.hint : item.answer;
            if (app.mode === "riddle") {
              actions.replaceChildren();
              button("Reveal answer", () => { extra.textContent = item.answer; actions.replaceChildren(); button("Next riddle", next); });
              button("Skip to next", next);
            } else {
              actions.replaceChildren();
              button("Tell me another", next);
            }
          });
        } else if (app.mode === "quiz") {
          item.choices.forEach((choice) => button(choice, () => {
            actions.replaceChildren();
            if (choice === item.answer) {
              points += 1;
              extra.textContent = "Correct! Nice one.";
            } else {
              extra.textContent = `Not quite — the answer is ${item.answer}.`;
            }
            scoreDisplay.textContent = `Correct answers: ${points}`;
            button("Next question", next);
          }));
        } else if (app.mode === "choice") {
          item.choices.forEach((choice) => button(choice, () => {
            extra.textContent = `Great choice: ${choice}`;
            actions.replaceChildren();
            button("Next dilemma", next);
          }));
        } else if (app.mode === "quest") {
          button("I did it! +1", () => {
            points += 1;
            next();
          });
          button("Give me another", next);
        } else {
          button(app.button || "Surprise me", next);
        }
      }
      render();
    </script>
  </body>
</html>
"""


def load_state():
    if not STATE_FILE.exists():
        return {"last_date": "", "count": 0}
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not read daily app state at {STATE_FILE}: {error}") from error
    if not isinstance(state, dict) or not isinstance(state.get("count"), int):
        raise RuntimeError(f"Daily app state is invalid: {STATE_FILE}")
    return state


def write_atomic(path, content):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def render_page(idea):
    title = html.escape(idea["title"], quote=True)
    page = APP_TEMPLATE.replace("__TITLE__", title)
    page = page.replace("__ICON__", html.escape(idea["icon"], quote=True))
    page = page.replace("__DESCRIPTION__", html.escape(idea["description"], quote=True))
    serialized = json.dumps(idea, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return page.replace("__CONFIG__", serialized)


def render_card(idea, relative_href):
    title = html.escape(idea["title"])
    description = html.escape(idea["description"])
    icon = html.escape(idea["icon"])
    tag = html.escape(idea["tag"])
    kind = html.escape(idea["kind"], quote=True)
    href = html.escape(relative_href, quote=True)
    return (
        f'<a class="card" data-kind="{kind}" href="{href}">\n'
        f'  <div class="card-top"><span class="icon" aria-hidden="true">{icon}</span><span class="tag">{tag}</span></div>\n'
        f'  <h3>{title}</h3><div class="card-description"><p>{description}</p><span class="category-pill">{"Games" if kind == "game" else "Tools"}</span></div><span class="card-cta">Open mini app <span class="arrow" aria-hidden="true">→</span></span>\n'
        f'</a>'
    )


def main():
    DAILY_ROOT.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    state = load_state()
    if state.get("last_date") == today:
        print(f"A daily app is already published for {today}.")
        return

    index = state["count"]
    idea = IDEAS[index % len(IDEAS)].copy()
    item_offset = (index // len(IDEAS)) % len(idea["items"])
    idea["items"] = idea["items"][item_offset:] + idea["items"][:item_offset]
    idea["title"] = f'{idea["title"]} #{index + 1}'
    slug = f'{today}-{idea["slug"]}'
    app_directory = ROOT / "daily-apps" / "sites" / slug
    app_directory.mkdir(parents=True, exist_ok=True)
    page_path = app_directory / "index.html"
    write_atomic(page_path, render_page(idea))

    homepage_path = ROOT / "home.html"
    homepage = homepage_path.read_text(encoding="utf-8")
    if homepage.count(START_MARKER) != 1 or homepage.count(END_MARKER) != 1:
        raise RuntimeError("The daily app markers are missing or duplicated in home.html.")
    if f'href="daily-apps/sites/{slug}/"' not in homepage:
        card = render_card(idea, f"daily-apps/sites/{slug}/")
        homepage = homepage.replace(END_MARKER, card + "\n            " + END_MARKER)
        write_atomic(homepage_path, homepage)

    list_path = ROOT / "websbase.txt"
    list_content = list_path.read_text(encoding="utf-8")
    idea_line = f'-<{idea["title"].lower()}>'
    if idea_line not in list_content.lower().splitlines():
        list_path.write_text(list_content.rstrip() + "\n" + idea_line + "\n", encoding="utf-8", newline="\n")

    state["last_date"] = today
    state["count"] = index + 1
    write_atomic(STATE_FILE, json.dumps(state, indent=2) + "\n")
    print(f"Published {idea['title']} at {page_path}")


if __name__ == "__main__":
    main()
