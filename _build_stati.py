# -*- coding: utf-8 -*-
import html
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent
src = root / "статьи"
out = root / "stati"
out.mkdir(exist_ok=True)

articles = [
    {
        "file": "Статья номер 1.txt",
        "slug": "gotovyy-biznes-bez-medlicenzii.html",
        "desc": "Как открыть готовый бьюти-бизнес без больших вложений и медицинской лицензии: формат одной капсулы ухода за лицом.",
    },
    {
        "file": "Статья номер 2.txt",
        "slug": "beauty-kapsula-face-wash-bear.html",
        "desc": "Как работает готовый бизнес на одной бьюти-капсуле FACE WASH BEAR с рейтингом 5.0 без уколов и медлицензии.",
    },
    {
        "file": "Статья номер 3.txt",
        "slug": "franshiza-spa-kapsula-pod-klyuch.html",
        "desc": "Запуск студии FACE WASH BEAR в своём городе: пакет под ключ, рассрочка и формат одной SPA-капсулы.",
    },
    {
        "file": "Статья номер 4.txt",
        "slug": "uhod-bez-ukolov-dlya-masterov.html",
        "desc": "Почему мастера выбирают уход за лицом без инъекций и как на этом спросе зарабатывать с бьюти-капсулой.",
    },
    {
        "file": "Статья номер 5.txt",
        "slug": "salon-klinika-ili-kapsula.html",
        "desc": "Сравнение путей в бьюти-бизнес: классический салон, медкосметология или одна готовая бьюти-капсула.",
    },
]

SECTION_STARTERS = (
    "Почему",
    "Что ",
    "Вариант",
    "Путь",
    "Как ",
    "Кому",
    "Проверенный",
    "Эксклюзивная",
    "Комфортный",
    "Два ",
    "5 причин",
)


def is_heading(line: str) -> bool:
    if not line or line.startswith(("—", "- ")):
        return False
    if re.match(r"^\d+\.\s+", line) and len(line) < 120:
        return True
    if line.endswith(":") and len(line) < 80:
        return True
    if any(line.startswith(s) for s in SECTION_STARTERS) and len(line) < 100:
        return True
    if len(line) < 90 and not line.endswith(".") and not line.endswith(","):
        return True
    return False


def body_to_html(text: str):
    text = text.replace("\r\n", "\n").strip()
    if text.startswith("-"):
        text = text[1:].lstrip()
    lines = text.split("\n")
    title = lines[0].strip().lstrip("-").strip()
    rest = lines[1:]
    blocks = []
    i = 0
    while i < len(rest):
        line = rest[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith("—") or line.startswith("- "):
            items = []
            while i < len(rest) and rest[i].strip().startswith(("—", "- ")):
                items.append(rest[i].strip().lstrip("—").lstrip("-").strip())
                i += 1
            lis = "".join(f"<li>{html.escape(it)}</li>" for it in items)
            blocks.append(
                f'<ul class="mt-4 space-y-2 text-base leading-relaxed text-[#5C534E]">{lis}</ul>'
            )
            continue

        if re.match(r"^\d\)\s", line):
            items = []
            while i < len(rest) and re.match(r"^\d\)\s", rest[i].strip()):
                items.append(re.sub(r"^\d\)\s", "", rest[i].strip()))
                i += 1
            lis = "".join(
                f'<li class="pl-1">{html.escape(it)}</li>' for it in items
            )
            blocks.append(
                f'<ol class="mt-4 list-decimal space-y-2 pl-5 text-base leading-relaxed text-[#5C534E]">{lis}</ol>'
            )
            continue

        numbered = re.match(r"^(\d+)\.\s+(.+)$", line)
        if numbered and len(line) < 120:
            heading = f"{numbered.group(1)}. {numbered.group(2)}"
            blocks.append(
                f'<h2 class="mt-10 text-xl font-extrabold tracking-tight text-[#2a1c14] sm:text-2xl">{html.escape(heading)}</h2>'
            )
            i += 1
            continue

        if is_heading(line) and not line.endswith("."):
            blocks.append(
                f'<h2 class="mt-10 text-xl font-extrabold tracking-tight text-[#2a1c14] sm:text-2xl">{html.escape(line.rstrip(":"))}</h2>'
            )
            i += 1
            continue

        para = [line]
        i += 1
        while i < len(rest):
            nxt = rest[i].strip()
            if not nxt:
                break
            if nxt.startswith(("—", "- ")) or re.match(r"^\d+[.)]\s", nxt):
                break
            if is_heading(nxt) and not nxt.endswith("."):
                break
            para.append(nxt)
            i += 1
        blocks.append(
            f'<p class="mt-4 text-base leading-relaxed text-[#5C534E]">{html.escape(" ".join(para))}</p>'
        )

    return title, "\n".join(blocks)


SHELL_CSS = """
    html { scroll-behavior: smooth; }
    body { font-family: Manrope, sans-serif; background: #F6E4D6; color: #2a1c14; }
    .btn-orange { background: #C2410C; }
    .btn-orange:hover { background: #9A3412; }
    .brand-kicker { font-weight: 800; -webkit-text-stroke: 0.55px currentColor; paint-order: stroke fill; }
    .brand-orange { background: #C2410C; }
"""


def render_page(title, description, slug, body_html, all_articles):
    esc_title = html.escape(title)
    esc_desc = html.escape(description)
    canon = f"https://franchise.facewashbear.ru/stati/{slug}"
    others = "".join(
        f'<li><a class="underline-offset-4 hover:underline" href="{html.escape(a["slug"])}">{html.escape(a["title"])}</a></li>'
        for a in all_articles
        if a["slug"] != slug
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc_title} — FACE WASH BEAR</title>
  <meta name="description" content="{esc_desc}">
  <link rel="canonical" href="{canon}">
  <meta property="og:title" content="{esc_title}">
  <meta property="og:description" content="{esc_desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canon}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Manrope:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Manrope', 'sans-serif'],
            serif: ['"Cormorant Garamond"', 'serif']
          }},
          colors: {{ mute: '#5C534E' }}
        }}
      }}
    }}
  </script>
  <style>{SHELL_CSS}</style>
</head>
<body class="bg-[#F6E4D6] text-[#2a1c14] antialiased">
  <header class="sticky top-0 z-50 border-b border-[#EAD8C8] bg-[#FBF0E6]">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 lg:px-6">
      <a href="../" class="flex shrink-0 items-center gap-3">
        <img src="../images/logo.png" alt="Логотип Умывающийся Панда" width="1023" height="1280" class="h-[46px] w-auto rounded-[10px]">
        <span class="leading-tight">
          <span class="brand-kicker block text-[15px] font-extrabold uppercase leading-none tracking-[0.08em] text-[#C2410C]">Face Wash Bear</span>
          <span class="block font-serif text-lg font-semibold text-[#2a1c14]">Умывающийся Панда</span>
        </span>
      </a>
      <a href="../" class="btn-orange inline-flex items-center justify-center rounded-full px-5 py-2.5 text-sm font-bold text-white">На сайт франшизы</a>
    </div>
  </header>

  <main class="mx-auto max-w-3xl px-4 py-10 sm:py-14">
    <p class="text-xs font-bold uppercase tracking-wide text-[#C2410C]">Статья · FACE WASH BEAR</p>
    <h1 class="mt-3 font-serif text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">{esc_title}</h1>
    <article class="article-body mt-8">
{body_html}
    </article>

    <div class="mt-12 rounded-[28px] border border-[#EAD8C8] bg-[#FBF0E6] p-6 sm:p-8">
      <p class="text-lg font-extrabold leading-snug text-[#2a1c14]">Хотите увидеть формат целиком?</p>
      <p class="mt-2 text-sm leading-relaxed text-[#5C534E]">На сайте франшизы — капсула, преимущества, условия запуска и заявка на стоимость. Сначала посмотрите лендинг, затем свяжитесь с нами.</p>
      <a href="../" class="btn-orange mt-5 inline-flex items-center justify-center rounded-full px-6 py-3.5 text-sm font-bold text-white">Смотреть сайт франшизы</a>
    </div>

    <nav class="mt-12 border-t border-[#EAD8C8] pt-8" aria-label="Другие статьи">
      <p class="text-sm font-extrabold">Другие статьи</p>
      <ul class="mt-3 space-y-2 text-sm text-[#5C534E]">{others}</ul>
    </nav>
  </main>

  <footer class="brand-orange text-white">
    <div class="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 sm:flex-row sm:items-center sm:justify-between">
      <a href="../" class="font-serif text-lg font-semibold">FACE WASH BEAR · Умывающийся Панда</a>
      <a class="text-sm underline underline-offset-4" href="../">Вернуться на главную</a>
    </div>
  </footer>
</body>
</html>
"""


def main():
    built = []
    for meta in articles:
        raw = (src / meta["file"]).read_text(encoding="utf-8")
        title, body = body_to_html(raw)
        built.append({**meta, "title": title, "body": body})

    for a in built:
        page = render_page(a["title"], a["desc"], a["slug"], a["body"], built)
        (out / a["slug"]).write_text(page, encoding="utf-8")
        print("wrote", a["slug"])

    index_items = "".join(
        f'<li class="border-b border-[#EAD8C8] py-4"><a class="text-lg font-extrabold text-[#2a1c14] hover:text-[#C2410C]" href="{html.escape(a["slug"])}">{html.escape(a["title"])}</a><p class="mt-1 text-sm text-[#5C534E]">{html.escape(a["desc"])}</p></li>'
        for a in built
    )
    index_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Статьи — FACE WASH BEAR франшиза</title>
  <meta name="description" content="Статьи о готовом бьюти-бизнесе на одной капсуле FACE WASH BEAR: запуск без медлицензии, формат под ключ и рассрочка.">
  <link rel="canonical" href="https://franchise.facewashbear.ru/stati/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Manrope:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>{SHELL_CSS}</style>
</head>
<body class="bg-[#F6E4D6] text-[#2a1c14] antialiased">
  <header class="sticky top-0 z-50 border-b border-[#EAD8C8] bg-[#FBF0E6]">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
      <a href="../" class="flex items-center gap-3">
        <img src="../images/logo.png" alt="" class="h-[46px] w-auto rounded-[10px]">
        <span class="brand-kicker text-[15px] font-extrabold uppercase tracking-[0.08em] text-[#C2410C]">Face Wash Bear</span>
      </a>
      <a href="../" class="btn-orange rounded-full px-5 py-2.5 text-sm font-bold text-white">На сайт франшизы</a>
    </div>
  </header>
  <main class="mx-auto max-w-3xl px-4 py-12">
    <h1 class="font-serif text-3xl font-semibold sm:text-4xl">Статьи</h1>
    <p class="mt-3 text-[#5C534E]">Материалы о формате одной бьюти-капсулы и запуске готового бизнеса FACE WASH BEAR.</p>
    <ul class="mt-8">{index_items}</ul>
  </main>
  <footer class="brand-orange text-white">
    <div class="mx-auto max-w-6xl px-4 py-8"><a href="../" class="underline underline-offset-4">На главную</a></div>
  </footer>
</body>
</html>
"""
    (out / "index.html").write_text(index_html, encoding="utf-8")

    urls = [
        "https://franchise.facewashbear.ru/",
        "https://franchise.facewashbear.ru/stati/",
    ] + [f"https://franchise.facewashbear.ru/stati/{a['slug']}" for a in built]
    today = "2026-11-27"
    sitemap_body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>" for u in urls
    )
    (root / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_body}\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    robots = root / "robots.txt"
    if not robots.exists():
        robots.write_text(
            "User-agent: *\nAllow: /\nSitemap: https://franchise.facewashbear.ru/sitemap.xml\n",
            encoding="utf-8",
        )
    else:
        text = robots.read_text(encoding="utf-8")
        if "sitemap.xml" not in text.lower():
            robots.write_text(
                text.rstrip() + "\nSitemap: https://franchise.facewashbear.ru/sitemap.xml\n",
                encoding="utf-8",
            )
    print("done", len(built))


if __name__ == "__main__":
    main()
