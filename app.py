"""
Mitraya Farmers Producer Company - Streamlit website
Pages (same menu names as the reference site): Home, Our Projects, Gallery, About us, Donate Now

Run:   streamlit run app.py

Put your images in an "images" folder next to this file (all optional - a
green placeholder is shown for anything missing):

    images/logo.png
    images/hero.jpg
    images/about_1.jpg
    images/about_2.jpg
    images/projects/<name>.jpg      (names are set in PROJECTS below)
    images/gallery/*.jpg|png|jpeg   (every picture in this folder appears in Gallery)

Edit the CONFIG / CONTENT sections just below to put in your own data.
"""

import base64
import csv
import mimetypes
from datetime import datetime
from pathlib import Path

import streamlit as st

# =====================================================================
# CONFIG  - replace with your own details
# =====================================================================
ORG_NAME = "Mitraya Farmers Producer Company"
SHORT_NAME = "Mitraya FPC"
TAGLINE = "Making World Farmers Friendly"
EMAIL = "mitrayafarmerspc@gmail.com"
PHONES = ["+91 9423648979"]
WHATSAPP = "+91 9423648979"  # country code + number, digits only
ADDRESS = "Plot No 5, Near D mart, Wathoda layout ,Nagpur 440024, Maharashtra, India"

# Bank / UPI details shown on the Donate Now page
BANK = {
    "Contact": "mitrayafarmerspc@gmail.com" ,
   
}

BASE = Path(__file__).parent
IMG = BASE / "images"
DATA = BASE / "data"

# =====================================================================
# CONTENT  - replace with your own text
# =====================================================================
WHO_WE_ARE = (
    "Mitraya Farmers Producer Company is a farmer-owned organisation that brings "
    "small and marginal farmers together so they can buy better, grow better and "
    "sell better. By pooling land, knowledge and produce, our members gain the "
  
)
VISION = (
    "To raise the income and security of farming families by combining traditional "
    "farming wisdom with modern, resource-efficient practices and fair market access."
)
MISSION = [
    "Reduce the cost of seeds, fertiliser and equipment through group purchasing.",
    "Help members sell collectively to get fairer prices for their produce.",
    "Train farmers in soil-friendly, low-input and climate-smart methods.",
    "Create livelihood opportunities for women and youth in farming households.",
]
VALUES = [
    ("Farmer first", "Every decision starts with the member who grows the crop."),
    ("Transparency", "Prices, accounts and decisions are open to all members."),
    ("Sustainability", "We protect the soil and water that the next generation will farm."),
    ("Inclusion", "Women, youth and small landholders have a real voice."),
]
# Shown on the About page only when a value is filled in
STATS = [
    ("", "Member farmers"),
    ("", "Villages covered"),
    ("", "Acres under cultivation"),
    ("", "Women members"),
]
TEAM = [
    # ("Name", "Role", "images/team/name.jpg")
    ("Praful Bandbuche", "Chief Executive Officer and Director", "D:/Dashboard/images/Praful.jpg"),
    #("Praful Bandbuche", "Director", "team/director.jpg"),
]
FOCUS_AREAS = [
    ("Sustainable Agriculture",
     "Regenerative, low-input farming that improves soil health and long-term productivity.", 
     "projects/sustainable.jpg"),
    ("Women Empowerment",
     "Building leadership, participation and economic independence among women in farming households.",
     "projects/women.jpg"),
    ("Market Linkage",
     "Collective selling, aggregation and direct buyer connections for better prices.",
     "projects/market.jpg"),
    ("Training & Education",
     "Field schools and workshops that bring new skills and knowledge to farmers and youth.",
     "projects/education.jpg"),
]
PROJECTS = [
    {
        "title": "Sustainable Agriculture",
        "image": "D:/Dashboard/images/AWD@.jpeg",
        "text": "Promoting regenerative and low-input practices such as soil testing, "
                "organic inputs, crop rotation and efficient irrigation.",
        "points": ["Soil health programmes", "Water-saving irrigation", "Seed and input support"],
    },
    {
        "title": "Climate Finance",
        "image": "D:/Dashboard/images/climate_finance.jpg",
        "text": "Climate finance is money used to fund projects that stop climate change or help communities deal with its effects"
                "farmers can earn and decide for themselves.",
        "points": ["Self-help groups", "Skill and enterprise training", "Leadership workshops"],
    },
    {
        "title": "Market Linkage",
        "image": "D:/Dashboard/images/container.jpeg",
        "text": "Collection centres, grading, storage and direct sales so that members "
                "get a fair share of the final price.",
        "points": ["Aggregation centres", "Buyer partnerships", "Value addition"],
    },
    {
        "title": "Training & Education",
        "image": "D:/Dashboard/images/Training.jpeg",
        "text": "Practical learning for farmers and better access to quality education "
                "for rural children and youth.",
        "points": ["Farmer field schools", "Digital literacy", "Scholarship support"],

    },
]

# =====================================================================
# PAGES  (menu name -> url slug)
# =====================================================================
PAGES = {
    "Home": "home",
    "Our Projects": "our-projects",
    "Gallery": "gallery",
    "About us": "about-us",
    "Donate Now": "donate-now",
}
SLUG_TO_PAGE = {v: k for k, v in PAGES.items()}

st.set_page_config(page_title=ORG_NAME, page_icon="D:/Dashboard/images/mitraya_logo.jpeg", layout="wide",
                   initial_sidebar_state="collapsed")

# =====================================================================
# HELPERS
# =====================================================================
def clean(s: str) -> str:
    """Strip leading spaces so Markdown never treats HTML as a code block."""
    return "\n".join(line.strip() for line in s.splitlines() if line.strip())


def show(html: str):
    st.markdown(clean(html), unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def data_uri(path_str: str) -> str:
    p = Path(path_str)
    if not p.exists():
        return ""
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def img(rel: str, alt: str = "", cls: str = "") -> str:
    """Return an <img> tag, or a green placeholder when the file is missing."""
    uri = data_uri(str(IMG / rel))
    if uri:
        return f'<img class="{cls}" src="{uri}" alt="{alt}">'
    return f'<div class="ph {cls}"><span>{alt or "Add image"}<br><small>images/{rel}</small></span></div>'


def link(label: str, page: str, kind: str = "btn") -> str:
    return f'<a class="{kind}" href="?page={PAGES[page]}" target="_self">{label}</a>'


def gallery_files():
    folder = IMG / "gallery"
    if not folder.exists():
        return []
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in exts)


def current_page() -> str:
    slug = st.query_params.get("page", "home")
    if isinstance(slug, list):
        slug = slug[0]
    return SLUG_TO_PAGE.get(slug, "Home")


# =====================================================================
# THEME
# =====================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bitter:wght@500;700;800&family=Nunito+Sans:wght@400;600;700&display=swap');

:root{
  --field:#2E5B34;      /* hunter green */
  --leaf:#6E9A3B;       /* young leaf */
  --grain:#E0A526;      /* ripe millet gold */
  --soil:#5A3A26;       /* dark soil */
  --paddy:#EEF3DF;      /* pale paddy */
  --sky:#FAFBF4;        /* page background */
  --ink:#24301F;
}
html, body, [class*="css"], .stApp{font-family:'Nunito Sans',sans-serif;color:var(--ink);}
.stApp{background:var(--sky);}
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"]{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
h1,h2,h3,h4{font-family:'Bitter',serif !important;color:var(--field);letter-spacing:-.01em;}
a{text-decoration:none;}

.wrap{max-width:1160px;margin:0 auto;padding:0 24px;}
.section{padding:64px 0;}
.section.alt{background:var(--paddy);}
.section h2{font-size:2.1rem;margin:0 0 8px 0;}
.lead{font-size:1.1rem;line-height:1.75;max-width:68ch;}
.rule{width:64px;height:5px;background:var(--grain);border-radius:3px;margin:10px 0 24px 0;}

/* top bar + menu */
.topbar{background:var(--field);color:#E7EFD8;font-size:.85rem;padding:8px 0;}
.topbar .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;}
.topbar a{color:#F5E3A8;}
.nav{background:#fff;border-bottom:4px solid var(--grain);}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px;}
.brand{display:flex;align-items:center;gap:12px;}
.brand img{height:54px;width:auto;border-radius:6px;}
.brand .logo-ph{width:54px;height:54px;border-radius:50%;background:var(--field);color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.6rem;}
.brand b{font-family:'Bitter',serif;font-size:1.15rem;color:var(--field);line-height:1.1;display:block;}
.brand small{color:var(--soil);}
.menu{display:flex;gap:4px;flex-wrap:wrap;}
.menu a{padding:9px 16px;border-radius:999px;color:var(--ink);font-weight:700;}
.menu a:hover{background:var(--paddy);}
.menu a.active{background:var(--field);color:#fff;}
.menu a.donate{background:var(--grain);color:#2b1d00;}
.menu a.donate.active{background:var(--soil);color:#fff;}

/* hero */
.hero{position:relative;min-height:540px;display:flex;align-items:center;color:#fff;
  background-size:cover;background-position:center;}
.hero::before{content:"";position:absolute;inset:0;
  background:linear-gradient(100deg,rgba(26,52,30,.88) 15%,rgba(26,52,30,.35) 80%);}
.hero .wrap{position:relative;}
.hero h1{color:#fff;font-size:3.3rem;line-height:1.08;margin:0 0 16px 0;max-width:15ch;}
.hero p{font-size:1.2rem;max-width:52ch;line-height:1.6;color:#F2F6E6;}
.hero.small{min-height:250px;}
.hero.small h1{font-size:2.6rem;margin:0;max-width:none;}
.rows{position:absolute;left:0;right:0;bottom:0;height:46px;opacity:.9;
  background:repeating-linear-gradient(90deg,var(--leaf) 0 10px,var(--field) 10px 20px);
  clip-path:polygon(0 60%,5% 25%,10% 60%,15% 25%,20% 60%,25% 25%,30% 60%,35% 25%,40% 60%,45% 25%,50% 60%,55% 25%,60% 60%,65% 25%,70% 60%,75% 25%,80% 60%,85% 25%,90% 60%,95% 25%,100% 60%,100% 100%,0 100%);}

/* buttons */
.btn{display:inline-block;background:var(--grain);color:#2b1d00 !important;font-weight:800;padding:13px 28px;border-radius:999px;margin:8px 10px 0 0;transition:transform .15s;}
.btn:hover{transform:translateY(-2px);}
.btn.ghost{background:transparent;border:2px solid #fff;color:#fff !important;}
.btn.green{background:var(--field);color:#fff !important;}
.more{font-weight:800;color:var(--field);}

/* images */
.round{width:100%;height:100%;object-fit:cover;border-radius:18px 18px 18px 4px;display:block;}
.ph{background:repeating-linear-gradient(45deg,#DCE8C3 0 14px,#CFDFB0 14px 28px);color:var(--field);
  display:flex;align-items:center;justify-content:center;text-align:center;border-radius:18px 18px 18px 4px;
  min-height:220px;width:100%;height:100%;font-weight:700;padding:12px;}
.ph small{font-weight:400;opacity:.7;}

/* layout blocks */
.grid2{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:center;}
.pics{display:grid;grid-template-columns:1fr 1fr;gap:16px;height:360px;}
.pics > :nth-child(2){margin-top:40px;}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;}
.card{background:#fff;border-radius:16px;overflow:hidden;border-bottom:5px solid var(--leaf);
  box-shadow:0 2px 10px rgba(46,91,52,.1);}
.card .thumb{height:170px;}
.card .thumb .ph,.card .thumb img{border-radius:0;height:170px;min-height:0;object-fit:cover;width:100%;display:block;}
.card .body{padding:18px 20px 22px 20px;}
.card h3{font-size:1.15rem;margin:0 0 8px 0;}
.card p{margin:0;line-height:1.6;font-size:.97rem;}

.vision{background:var(--field);color:#fff;border-radius:20px;padding:40px 44px;
  background-image:radial-gradient(circle at 92% 20%,rgba(224,165,38,.35) 0,transparent 40%);}
.vision h2{color:#fff;margin:0 0 8px 0;}
.vision p{font-size:1.15rem;line-height:1.7;max-width:70ch;margin:0;}

.cta{background:var(--soil);color:#fff;text-align:center;padding:64px 24px;}
.cta h2{color:#fff;font-size:2.2rem;margin:0 0 12px 0;}
.cta p{max-width:56ch;margin:0 auto 12px auto;}

/* project rows */
.proj{display:grid;grid-template-columns:1fr 1.2fr;gap:36px;align-items:center;margin-bottom:44px;}
.proj.flip{grid-template-columns:1.2fr 1fr;}
.proj.flip .pimg{order:2;}
.pimg{height:300px;}
.proj ul{padding-left:20px;line-height:1.9;}
.proj li::marker{color:var(--grain);}

/* gallery */
.masonry{column-count:3;column-gap:16px;}
.masonry .item{break-inside:avoid;margin-bottom:16px;}
.masonry img{width:100%;border-radius:14px;display:block;}
.masonry .ph{min-height:200px;}

/* gallery page - separate cards, 2 per row (2 left + 2 right) */
.gallery-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:28px;}
.gcard{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(46,91,52,.15);
  border-bottom:5px solid var(--grain);transition:transform .25s,box-shadow .25s;}
.gcard:hover{transform:translateY(-5px);box-shadow:0 10px 26px rgba(46,91,52,.25);}
.gcard .gimg{aspect-ratio:4/3;overflow:hidden;background:#e8eedc;}
.gcard .gimg img,.gcard .gimg .ph{width:100%;height:100%;object-fit:cover;display:block;border-radius:0;min-height:0;}
.gcard .gcap{padding:14px 18px;font-family:'Bitter',serif;font-weight:700;color:var(--field);text-align:center;}

/* about */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;}
.stat{background:#fff;border-radius:16px;padding:24px;text-align:center;border-top:5px solid var(--grain);}
.stat b{font-family:'Bitter',serif;font-size:2.4rem;color:var(--field);display:block;}
.value{background:#fff;border-left:6px solid var(--leaf);border-radius:10px;padding:18px 22px;}
.value h4{margin:0 0 6px 0;}
.value p{margin:0;line-height:1.6;}
.team{text-align:center;}
.team .avatar{width:150px;height:150px;border-radius:50%;margin:0 auto 12px auto;overflow:hidden;border:5px solid var(--grain);}
.team .avatar img,.team .avatar .ph{width:150px;height:150px;border-radius:50%;object-fit:cover;min-height:0;font-size:.7rem;}
.team b{font-family:'Bitter',serif;color:var(--field);display:block;}
.mission li{margin-bottom:10px;line-height:1.6;}
.mission li::marker{color:var(--grain);}

/* donate */
.bank{background:#fff;border-radius:16px;padding:26px 30px;border-left:6px solid var(--grain);}
.bank table{width:100%;border-collapse:collapse;}
.bank td{padding:9px 0;border-bottom:1px dashed #cfd8bd;}
.bank td:first-child{color:var(--soil);font-weight:700;width:42%;}

/* footer */
.footer{background:#1D3A22;color:#D6E2C3;padding:48px 0 20px 0;margin-top:0;}
.footer .cols{display:grid;grid-template-columns:1.4fr 1fr 1.2fr;gap:36px;}
.footer h4{color:var(--grain) !important;margin:0 0 12px 0;}
.footer a{color:#D6E2C3;display:block;padding:3px 0;}
.footer a:hover{color:#fff;}
.footer .copy{border-top:1px solid rgba(255,255,255,.15);margin-top:30px;padding-top:16px;font-size:.85rem;text-align:center;}
.wa{position:fixed;right:20px;bottom:20px;z-index:99;background:#25D366;color:#fff !important;font-weight:800;
  padding:12px 18px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.25);}

/* streamlit form inside the donate page */
div[data-testid="stForm"]{background:#fff;border:none;border-radius:16px;padding:26px 30px;box-shadow:0 2px 10px rgba(46,91,52,.1);}
.stButton>button,.stFormSubmitButton>button{background:var(--field);color:#fff;border:none;border-radius:999px;font-weight:800;padding:.6rem 1.8rem;}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:var(--leaf);color:#fff;}

@media (max-width:900px){
  .grid2,.proj,.proj.flip,.footer .cols{grid-template-columns:1fr;}
  .proj.flip .pimg{order:0;}
  .grid4,.stats{grid-template-columns:1fr 1fr;}
  .masonry{column-count:2;}
  .hero h1{font-size:2.3rem;}
  .pics{height:260px;}
}
@media (max-width:560px){
  .grid4,.stats{grid-template-columns:1fr;}
  .masonry{column-count:1;}
  .gallery-grid{grid-template-columns:1fr;}
}
</style>
"""


# =====================================================================
# SHARED PIECES
# =====================================================================
def header(active: str):
    logo_uri = data_uri(str(IMG / "D:/Dashboard/images/mitraya_logo.jpeg"))
    logo = (f'<img src="{logo_uri}" alt="{SHORT_NAME} logo">' if logo_uri
            else '<div class="logo-ph">🌾</div>')
    items = ""
    for name, slug in PAGES.items():
        classes = []
        if name == active:
            classes.append("active")
        if name == "Donate Now":
            classes.append("donate")
        items += f'<a class="{" ".join(classes)}" href="?page={slug}" target="_self">{name}</a>'
    show(f"""
    <div class="topbar"><div class="wrap">
      <span>📍 {ADDRESS}</span>
      <span>✉ <a href="mailto:{EMAIL}">{EMAIL}</a> &nbsp;|&nbsp; ☎ {" / ".join(PHONES)}</span>
    </div></div>
    <div class="nav"><div class="wrap">
      <a class="brand" href="?page=home" target="_self">{logo}<span><b>{ORG_NAME}</b><small>{TAGLINE}</small></span></a>
      <div class="menu">{items}</div>
    </div></div>
    """)


def page_banner(title: str, subtitle: str = ""):
    uri = data_uri(str(IMG / "hero.jpg"))
    bg = (f"background-image:url('{uri}');" if uri else
          "background-image:linear-gradient(120deg,#2E5B34,#6E9A3B);")
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    show(f"""
    <div class="hero small" style="{bg}"><div class="wrap">
      <h1>{title}</h1>{sub}
    </div><div class="rows"></div></div>
    """)


def footer():
    menu = "".join(f'<a href="?page={s}" target="_self">{n}</a>' for n, s in PAGES.items())
    phones = "<br>".join(PHONES)
    show(f"""
    <div class="footer"><div class="wrap">
      <div class="cols">
        <div><h4>{ORG_NAME}</h4><p>{TAGLINE}<br>A farmer-owned company working for stronger,
        more resilient farming communities.</p></div>
        <div><h4>Menu</h4>{menu}</div>
        <div><h4>Contact</h4>
          <p>{ADDRESS}<br><a href="mailto:{EMAIL}">{EMAIL}</a>{phones}</p></div>
      </div>
      <div class="copy">© {datetime.now().year} {ORG_NAME}. All rights reserved.</div>
    </div></div>
    <a class="wa" href="https://wa.me/{WHATSAPP}" target="_blank">💬 Chat on WhatsApp</a>
    """)


# =====================================================================
# PAGES
# =====================================================================
def page_home():
    uri = data_uri(str(IMG / "hero.jpg"))
    bg = (f"background-image:url('{uri}');" if uri else
          "background-image:linear-gradient(120deg,#2E5B34,#6E9A3B 70%,#E0A526);")
    show(f"""
    <div class="hero" style="{bg}"><div class="wrap">
      <h1>Rooted in the soil. Owned by farmers.</h1>
      <p>{SHORT_NAME} brings small farmers together so they can cut costs, earn fair prices and
      farm in ways that protect the land for generations.</p>
      {link("Our Projects", "Our Projects")}
      {link("Donate Now", "Donate Now", "btn ghost")}
    </div><div class="rows"></div></div>
    """)

    show(f"""
    <div class="section"><div class="wrap"><div class="grid2">
      <div><h2>Who we are</h2><div class="rule"></div><p class="lead">{WHO_WE_ARE}</p>
        {link("Read more about us", "About us", "btn green")}</div>
      <div class="pics">{img("about_1.jpg", "About image 1", "round")}{img("about_2.jpg", "About image 2", "round")}</div>
    </div></div></div>
    """)

    show(f"""
    <div class="wrap" style="padding-bottom:64px;"><div class="vision">
      <h2>Vision</h2><p>{VISION}</p></div></div>
    """)

    cards = "".join(
        f'<div class="card"><div class="thumb">{img(i, t)}</div>'
        f'<div class="body"><h3>{t}</h3><p>{d}</p></div></div>'
        for t, d, i in FOCUS_AREAS)
    show(f"""
    <div class="section alt"><div class="wrap">
      <h2>Our Focus Areas</h2><div class="rule"></div>
      <div class="grid4">{cards}</div>
    </div></div>
    """)

    files = gallery_files()[:3]
    if files:
        tiles = "".join(f'<div class="item"><img src="{data_uri(str(f))}" alt="Gallery"></div>' for f in files)
    else:
        tiles = "".join(f'<div class="item">{img("gallery/x", "Gallery photo")}</div>' for _ in range(3))
    show(f"""
    <div class="section"><div class="wrap">
      <h2>Gallery</h2><div class="rule"></div>
      <div class="masonry" style="column-count:3;">{tiles}</div>
      <p style="margin-top:18px;"><a class="more" href="?page=gallery" target="_self">More &gt;</a></p>
    </div></div>
    """)

    show(f"""
    <div class="cta">
      <h2>Join Our Mission: Make a Difference Today!</h2>
      <p>Your support helps small farmers grow better crops, earn more and build a secure future.</p>
      {link("Click here", "Donate Now")}
    </div>
    """)


def page_projects():
    page_banner("Our Projects", "How we work with farming families, season after season.")
    rows = ""
    for n, p in enumerate(PROJECTS):
        flip = " flip" if n % 2 else ""
        points = "".join(f"<li>{x}</li>" for x in p["points"])
        rows += f"""
        <div class="proj{flip}">
          <div class="pimg">{img(p["image"], p["title"], "round")}</div>
          <div><h2>{p["title"]}</h2><div class="rule"></div>
          <p class="lead">{p["text"]}</p><ul>{points}</ul></div>
        </div>"""
    show(f'<div class="section"><div class="wrap">{rows}</div></div>')
    show(f"""
    <div class="cta"><h2>Help us reach more farmers</h2>
    <p>Every contribution goes into seeds, training and market access for farming families.</p>
    {link("Donate Now", "Donate Now")}</div>
    """)


def page_gallery():
    page_banner("Gallery", "Moments from the fields, the training sessions and our farming community.")
    files = gallery_files()
    if files:
        cards = "".join(
            f'<div class="gcard"><div class="gimg"><img loading="lazy" src="{data_uri(str(f))}" alt="{f.stem}"></div>'
            f'<div class="gcap">{f.stem.replace("_", " ").replace("-", " ").title()}</div></div>'
            for f in files)
    else:
        cards = "".join(
            f'<div class="gcard"><div class="gimg">{img("gallery/x", f"Photo {i}")}</div>'
            f'<div class="gcap">Photo {i}</div></div>'
            for i in range(1, 5))
    show(f'<div class="section"><div class="wrap"><div class="gallery-grid">{cards}</div></div></div>')
    if not files:
        st.info("Add pictures to the images/gallery folder and they will appear here automatically.")


def page_about():
    page_banner("About us", ORG_NAME)
    show(f"""
    <div class="section"><div class="wrap"><div class="grid2">
      <div><h2>Who we are</h2><div class="rule"></div><p class="lead">{WHO_WE_ARE}</p></div>
      <div class="pics">{img("about_1.jpg", "About image 1", "round")}{img("about_2.jpg", "About image 2", "round")}</div>
    </div></div></div>
    """)

    stats = [(v, l) for v, l in STATS if v]
    if stats:
        tiles = "".join(f'<div class="stat"><b>{v}</b>{l}</div>' for v, l in stats)
        show(f'<div class="section alt"><div class="wrap"><div class="stats">{tiles}</div></div></div>')

    mission = "".join(f"<li>{m}</li>" for m in MISSION)
    show(f"""
    <div class="section"><div class="wrap"><div class="grid2" style="align-items:start;">
      <div class="vision"><h2>Vision</h2><p>{VISION}</p></div>
      <div><h2>Our Mission</h2><div class="rule"></div><ul class="mission lead">{mission}</ul></div>
    </div></div></div>
    """)

    vals = "".join(f'<div class="value"><h4>{t}</h4><p>{d}</p></div>' for t, d in VALUES)
    show(f"""
    <div class="section alt"><div class="wrap"><h2>Our Values</h2><div class="rule"></div>
      <div class="grid4" style="grid-template-columns:repeat(2,1fr);">{vals}</div>
    </div></div>
    """)

    people = "".join(
        f'<div class="team"><div class="avatar">{img(i, n)}</div><b>{n}</b>{r}</div>'
        for n, r, i in TEAM)
    show(f"""
    <div class="section"><div class="wrap"><h2>Our Team</h2><div class="rule"></div>
      <div class="grid4" style="grid-template-columns:repeat({max(len(TEAM), 1)},1fr);">{people}</div>
    </div></div>
    """)


def page_donate():
    page_banner("Donate Now", "Join our mission and help farming families grow.")
    
  


# =====================================================================
# APP
# =====================================================================
st.markdown(CSS, unsafe_allow_html=True)
active = current_page()
header(active)

{
    "Home": page_home,
    "Our Projects": page_projects,
    "Gallery": page_gallery,
    "About us": page_about,
    "Donate Now": page_donate,
}[active]()

footer()
