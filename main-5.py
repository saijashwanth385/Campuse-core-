"""
Campus Connect Pro — Python/Kivy Mobile App
Optimised for Pydroid 3 (Android) — Python 3.x / Kivy 2.x

Install on Pydroid 3:
    pip install kivy
Build APK (desktop):
    pip install buildozer && buildozer android debug
"""

# ─── Config — edit these without touching anything else ──────────────────────
APP_CONFIG = {
    "name":         "Campus Connect Pro",
    "student_name": "M V Sai Jashwanth",
    "dept":         "CSE",
    "year":         "2nd Year",
    "roll":         "VV25CSE0619",
    "avatar":       "🧑‍💻",
    # Paste your Anthropic key here (or leave as-is for demo mode)
    "api_key":      "YOUR_API_KEY_HERE",
    # Window size — ignored on real device
    "win_w": 430,
    "win_h": 860,
}

# ─── Imports ──────────────────────────────────────────────────────────────────
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

import time
import hashlib
import threading
import urllib.request
import urllib.error
import json

# ─── Colour Palette ───────────────────────────────────────────────────────────
C = {
    "navy":        get_color_from_hex("#1A237E"),
    "navyDark":    get_color_from_hex("#0D1757"),
    "navyLight":   get_color_from_hex("#283593"),
    "mint":        get_color_from_hex("#e4f5ea"),
    "mintAccent":  get_color_from_hex("#4CAF82"),
    "gold":        get_color_from_hex("#FFD54F"),
    "coral":       get_color_from_hex("#FF6B6B"),
    "purple":      get_color_from_hex("#7C3AED"),
    "white":       get_color_from_hex("#FFFFFF"),
    "glass":       (1, 1, 1, 0.08),
    "glassBorder": (1, 1, 1, 0.15),
    "bg":          get_color_from_hex("#0D1757"),
}

# ─── Static Data ──────────────────────────────────────────────────────────────
EVENTS = [
    {"id": 1, "title": "HackSphere 2026",    "type": "Hackathon", "date": "May 10",
     "time": "9:00 AM",  "venue": "CSE Block",      "dept": "CSE",     "seats": 12,
     "prize": "₹50,000", "color": "#7C3AED", "emoji": "💻"},
    {"id": 2, "title": "IdeaStorm 3.0",      "type": "Ideathon",  "date": "May 15",
     "time": "10:00 AM", "venue": "Main Auditorium", "dept": "All",     "seats": 30,
     "prize": "₹25,000", "color": "#FF6B6B", "emoji": "💡"},
    {"id": 3, "title": "Campus Fest",         "type": "Cultural",  "date": "May 20",
     "time": "5:00 PM",  "venue": "Open Ground",     "dept": "All",     "seats": 200,
     "prize": "Trophies","color": "#FF9800", "emoji": "🎭"},
    {"id": 4, "title": "ML Workshop",         "type": "Workshop",  "date": "May 12",
     "time": "2:00 PM",  "venue": "Lab 3",            "dept": "CSE/AI",  "seats": 5,
     "prize": "Certificate", "color": "#4CAF82", "emoji": "🤖"},
    {"id": 5, "title": "TCS Placement Drive", "type": "Placement", "date": "May 18",
     "time": "8:00 AM",  "venue": "Placement Cell",  "dept": "CSE/ECE", "seats": 50,
     "prize": "Job Offer","color": "#FFD54F", "emoji": "🏢"},
]

BOOKS = [
    {"id": 1, "title": "Data Structures & Algorithms", "author": "Thomas Cormen",
     "isbn": "978-0262033848", "dept": "CSE", "rack": "A-12", "status": "Available",    "copies": 3},
    {"id": 2, "title": "Operating Systems",             "author": "Andrew Tanenbaum",
     "isbn": "978-0137458981", "dept": "CSE", "rack": "A-15", "status": "Fully Issued", "copies": 0},
    {"id": 3, "title": "Database Systems",              "author": "Ramez Elmasri",
     "isbn": "978-0133970777", "dept": "CSE", "rack": "B-04", "status": "Reserved",     "copies": 1},
    {"id": 4, "title": "Digital Electronics",           "author": "M. Morris Mano",
     "isbn": "978-0132103718", "dept": "ECE", "rack": "C-09", "status": "Available",    "copies": 5},
    {"id": 5, "title": "Engineering Maths",             "author": "B.S. Grewal",
     "isbn": "978-8174091792", "dept": "All", "rack": "D-01", "status": "In Repair",    "copies": 0},
]

NOTIFICATIONS_DATA = [
    {"id": 1, "title": "HackSphere registration closes in 2 days!", "time": "2h ago",  "icon": "🔥", "unread": True},
    {"id": 2, "title": "ML Workshop — Only 5 seats left!",          "time": "5h ago",  "icon": "⚡", "unread": True},
    {"id": 3, "title": "Library fine of ₹15 due by Friday",         "time": "1d ago",  "icon": "📚", "unread": False},
    {"id": 4, "title": "TCS Placement Drive confirmed for May 18",   "time": "2d ago",  "icon": "🏢", "unread": False},
]

LEADERBOARD = [
    {"rank": 1, "name": "Priya Sharma",                         "dept": "CSE",   "points": 2840, "badges": 12, "medal": "🥇"},
    {"rank": 2, "name": "Rahul Kumar",                          "dept": "ECE",   "points": 2610, "badges": 10, "medal": "🥈"},
    {"rank": 3, "name": APP_CONFIG["student_name"].split()[-1], "dept": "CSE",   "points": 2480, "badges": 7,  "medal": "🥉", "isMe": True},
    {"rank": 4, "name": "Ananya Reddy",                         "dept": "ME",    "points": 2290, "badges": 9,  "medal": "4"},
    {"rank": 5, "name": "Kiran Patel",                          "dept": "CIVIL", "points": 2100, "badges": 8,  "medal": "5"},
    {"rank": 6, "name": "Siddharth V",                          "dept": "CSE",   "points": 1980, "badges": 6,  "medal": "6"},
]

CAMPUS_SYSTEM_PROMPT = (
    "You are CampusBot, a helpful AI assistant for Campus Connect Pro — "
    "a college campus app. You help students with:\n"
    "- Campus events (hackathons, workshops, placements, cultural fests)\n"
    "- Library books, availability, reservations, fines\n"
    "- Attendance and QR system\n"
    "- Leaderboard and badges\n"
    "- College life advice, study tips, career guidance\n"
    "Keep answers short, friendly, and relevant to college students."
)

# ─── Shared App State ─────────────────────────────────────────────────────────
class AppState:
    role = "student"
    registered_events: set = set()
    notifications = [dict(n) for n in NOTIFICATIONS_DATA]


# ═══════════════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def hex_color(h: str, alpha: float = 1.0):
    """Convert hex string to (r, g, b, alpha) tuple."""
    c = get_color_from_hex(h)
    return (c[0], c[1], c[2], alpha)


def _bind_rect(widget, rect, radius=None):
    """Keep a RoundedRectangle / Rectangle in sync with its widget."""
    if radius is not None:
        def _upd(inst, _):
            rect.pos  = inst.pos
            rect.size = inst.size
            rect.rounded_rectangle = (inst.x, inst.y, inst.width, inst.height, radius)
    else:
        def _upd(inst, _):
            rect.pos  = inst.pos
            rect.size = inst.size
    widget.bind(pos=_upd, size=_upd)


def make_glass_bg(widget, radius=dp(16),
                  color=(1, 1, 1, 0.08),
                  border=(1, 1, 1, 0.15)):
    """Frosted-glass rounded card on widget.canvas.before."""
    with widget.canvas.before:
        Color(*color)
        r = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[radius])
        Color(*border)
        ln = Line(
            rounded_rectangle=(widget.x, widget.y, widget.width, widget.height, radius),
            width=1,
        )

    def _upd(inst, _):
        r.pos  = inst.pos
        r.size = inst.size
        ln.rounded_rectangle = (inst.x, inst.y, inst.width, inst.height, radius)

    widget.bind(pos=_upd, size=_upd)


def nav_bg(screen_widget):
    """Solid navy background for a screen."""
    with screen_widget.canvas.before:
        Color(*C["navyDark"])
        bg = Rectangle(pos=screen_widget.pos, size=screen_widget.size)
    screen_widget.bind(
        pos=lambda i, v: setattr(bg, "pos",  v),
        size=lambda i, v: setattr(bg, "size", v),
    )


def pill_button(text, bg_color=None, text_color=(1, 1, 1, 1),
                on_press=None, font_size=None):
    """Rounded pill-shaped button."""
    fs   = font_size or sp(15)
    bg   = bg_color or C["mintAccent"]
    btn  = Button(
        text=text, font_size=fs, color=text_color, bold=True,
        background_normal="", background_color=(0, 0, 0, 0),
        size_hint_y=None, height=dp(48),
    )
    with btn.canvas.before:
        Color(*bg)
        r = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(24)])
    btn.bind(
        pos =lambda i, _: setattr(r, "pos",  i.pos),
        size=lambda i, _: setattr(r, "size", i.size),
    )
    if on_press:
        btn.bind(on_press=on_press)
    return btn


def tab_button(text, active=False):
    """Small rounded tab / filter button."""
    btn = Button(
        text=text, font_size=sp(11), bold=True,
        background_normal="", background_color=(0, 0, 0, 0),
        color=C["white"], size_hint_x=None, width=dp(88),
    )
    with btn.canvas.before:
        btn._tab_col = Color(*(C["mintAccent"] if active else (1, 1, 1, 0.08)))
        btn._tab_rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(14)])
    btn.bind(
        pos =lambda i, _: setattr(i._tab_rect, "pos",  i.pos),
        size=lambda i, _: setattr(i._tab_rect, "size", i.size),
    )
    return btn


def back_button(on_press=None):
    """Standard ← back button."""
    btn = Button(
        text="←", font_size=sp(22),
        size_hint_x=None, width=dp(40),
        background_normal="", background_color=(0, 0, 0, 0),
        color=C["white"],
    )
    if on_press:
        btn.bind(on_press=on_press)
    return btn


def screen_header(title: str, on_back=None, right_widget=None):
    """Reusable top header bar (← Title  [right_widget])."""
    hdr = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
    hdr.add_widget(back_button(on_press=on_back))
    hdr.add_widget(Label(text=title, font_size=sp(20), bold=True,
                         color=C["white"], halign="left"))
    if right_widget:
        hdr.add_widget(right_widget)
    return hdr


def stat_card(value: str, label: str, val_color=None):
    """Small vertical stat card (number + label)."""
    col  = val_color or C["mintAccent"]
    card = BoxLayout(orientation="vertical", spacing=dp(2), padding=dp(10))
    make_glass_bg(card)
    card.add_widget(Label(text=value, font_size=sp(20), bold=True, color=col,
                          size_hint_y=None, height=dp(28), halign="center"))
    card.add_widget(Label(text=label,  font_size=sp(9),  color=(1, 1, 1, 0.6),
                          size_hint_y=None, height=dp(18), halign="center"))
    return card


# ═══════════════════════════════════════════════════════════════════════════════
#  WELCOME / LOGIN SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class WelcomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)
        self._build_welcome()

    # ── helpers ──────────────────────────────────────────────────────────────
    def _clear(self):
        self.clear_widgets()
        nav_bg(self)

    def _go_dashboard(self, *_):
        AppState.role = getattr(self, "_selected_role", "student")
        sm = self.manager
        sm.transition = SlideTransition(direction="left")
        sm.current = "dashboard"

    # ── welcome page ─────────────────────────────────────────────────────────
    def _build_welcome(self):
        root = BoxLayout(orientation="vertical", padding=dp(28), spacing=dp(16))

        logo_box = BoxLayout(orientation="vertical", spacing=dp(10),
                             size_hint_y=None, height=dp(260))
        logo_box.add_widget(Label(text="🎓", font_size=sp(72),
                                  size_hint_y=None, height=dp(90), halign="center"))
        logo_box.add_widget(Label(text="Campus Connect", font_size=sp(30), bold=True,
                                  color=C["white"], size_hint_y=None, height=dp(40), halign="center"))
        logo_box.add_widget(Label(text="Pro", font_size=sp(22), bold=True,
                                  color=C["mintAccent"], size_hint_y=None, height=dp(30), halign="center"))
        logo_box.add_widget(Label(text="All Campus Events. One Place.",
                                  font_size=sp(14), color=(1, 1, 1, 0.7),
                                  size_hint_y=None, height=dp(30), halign="center"))
        root.add_widget(logo_box)

        pills = BoxLayout(orientation="horizontal", spacing=dp(8),
                          size_hint_y=None, height=dp(36))
        for txt in ["🏆 Events", "📚 Library", "📡 QR Attend"]:
            lbl = Label(text=txt, font_size=sp(11), bold=True,
                        color=C["white"], size_hint_y=None, height=dp(30))
            make_glass_bg(lbl, radius=dp(14))
            pills.add_widget(lbl)
        root.add_widget(pills)

        root.add_widget(Widget())

        root.add_widget(pill_button("Get Started →",
                                    on_press=lambda *_: self._build_login()))
        root.add_widget(pill_button("I already have an account",
                                    bg_color=(0, 0, 0, 0),
                                    text_color=hex_color("#e4f5ea"),
                                    on_press=lambda *_: self._build_login()))
        self.add_widget(root)

    # ── login page ────────────────────────────────────────────────────────────
    def _build_login(self):
        self._clear()
        root = BoxLayout(orientation="vertical", padding=dp(28), spacing=dp(20))

        root.add_widget(Label(text="🎓", font_size=sp(56),
                              size_hint_y=None, height=dp(70), halign="center"))
        root.add_widget(Label(text=APP_CONFIG["name"], font_size=sp(24), bold=True,
                              color=hex_color("#e4f5ea"), size_hint_y=None, height=dp(36), halign="center"))
        root.add_widget(Label(text="Sign in to your account", font_size=sp(13),
                              color=(1, 1, 1, 0.6), size_hint_y=None, height=dp(24), halign="center"))

        # Role selector
        role_box = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        self._role_btns: dict = {}
        self._selected_role = "student"
        for r in ["student", "teacher", "admin"]:
            btn = Button(
                text=r.capitalize(), font_size=sp(12), bold=True,
                background_normal="", background_color=(0, 0, 0, 0), color=C["white"],
            )
            with btn.canvas.before:
                btn._col = Color(*(C["mintAccent"] if r == "student" else (1, 1, 1, 0.08)))
                btn._rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(12)])
            btn.bind(
                pos =lambda i, _: setattr(i._rect, "pos",  i.pos),
                size=lambda i, _: setattr(i._rect, "size", i.size),
            )
            btn.bind(on_press=lambda inst, role=r: self._select_role(role))
            self._role_btns[r] = btn
            role_box.add_widget(btn)
        root.add_widget(role_box)

        self._email = TextInput(
            hint_text="Email / Roll No", multiline=False,
            background_color=(1, 1, 1, 0.1), foreground_color=C["white"],
            hint_text_color=(1, 1, 1, 0.4), cursor_color=C["white"],
            size_hint_y=None, height=dp(48), font_size=sp(15), padding=[dp(16), dp(12)],
        )
        self._pass = TextInput(
            hint_text="Password", password=True, multiline=False,
            background_color=(1, 1, 1, 0.1), foreground_color=C["white"],
            hint_text_color=(1, 1, 1, 0.4), cursor_color=C["white"],
            size_hint_y=None, height=dp(48), font_size=sp(15), padding=[dp(16), dp(12)],
        )
        root.add_widget(self._email)
        root.add_widget(self._pass)

        root.add_widget(pill_button("Sign In →", on_press=self._do_login))
        root.add_widget(pill_button("← Back",
                                    bg_color=(0, 0, 0, 0),
                                    text_color=hex_color("#e4f5ea"),
                                    on_press=lambda *_: (self._clear(), self._build_welcome())))
        self.add_widget(root)

    def _select_role(self, role):
        self._selected_role = role
        for r, btn in self._role_btns.items():
            btn._col.rgba = C["mintAccent"] if r == role else (1, 1, 1, 0.08)

    def _do_login(self, *_):
        self._go_dashboard()


# ═══════════════════════════════════════════════════════════════════════════════
#  BOTTOM NAVIGATION BAR
# ═══════════════════════════════════════════════════════════════════════════════
class NavBar(BoxLayout):
    NAV_ITEMS = [
        ("🏠", "Home",    "dashboard"),
        ("🎯", "Events",  "events"),
        ("📚", "Library", "library"),
        ("📡", "QR",      "qr"),
        ("👤", "Profile", "profile"),
    ]

    def __init__(self, screen_manager, **kw):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None, height=dp(64), **kw,
        )
        self.sm = screen_manager
        self._items: dict = {}

        with self.canvas.before:
            Color(0.05, 0.09, 0.34, 0.97)
            bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos =lambda i, v: setattr(bg, "pos",  v),
            size=lambda i, v: setattr(bg, "size", v),
        )

        for icon, label, scr in self.NAV_ITEMS:
            item = BoxLayout(orientation="vertical", spacing=dp(2))
            ico = Label(text=icon,  font_size=sp(22), size_hint_y=None, height=dp(28), halign="center")
            lbl = Label(text=label, font_size=sp(9),  bold=True,
                        color=(1, 1, 1, 0.4), size_hint_y=None, height=dp(14), halign="center")
            item.add_widget(ico)
            item.add_widget(lbl)
            item.bind(on_touch_down=lambda inst, t, s=scr: self._nav(s, t, inst))
            self._items[scr] = lbl
            self.add_widget(item)

    def _nav(self, scr, touch, widget):
        if not widget.collide_point(*touch.pos):
            return
        self.sm.transition = SlideTransition(direction="left")
        self.sm.current = scr
        self.set_active(scr)

    def set_active(self, scr):
        for s, lbl in self._items.items():
            lbl.color = C["mintAccent"] if s == scr else (1, 1, 1, 0.4)


# ═══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class DashboardScreen(Screen):
    _ev_idx = 0

    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        Clock.unschedule(self._rotate_event)
        self.clear_widgets()
        nav_bg(self)
        self._build()

    def on_leave(self):
        Clock.unschedule(self._rotate_event)

    def _build(self):
        root   = BoxLayout(orientation="vertical")
        scroll = ScrollView(size_hint=(1, 1))
        inner  = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(18),
                           size_hint_y=None)
        inner.bind(minimum_height=inner.setter("height"))

        # ── Greeting header ──────────────────────────────────────────────────
        hdr  = BoxLayout(size_hint_y=None, height=dp(72))
        left = BoxLayout(orientation="vertical", spacing=dp(2))
        h    = int(time.strftime("%H"))
        greet = "Good Morning 👋" if h < 12 else ("Good Afternoon 👋" if h < 17 else "Good Evening 👋")
        left.add_widget(Label(text=greet, font_size=sp(12), color=(1, 1, 1, 0.6),
                              halign="left", valign="middle", size_hint_y=None, height=dp(20)))
        first = APP_CONFIG["student_name"].split()[0]
        left.add_widget(Label(text=first, font_size=sp(21), bold=True, color=C["white"],
                              halign="left", valign="middle", size_hint_y=None, height=dp(28)))
        left.add_widget(Label(
            text=f"{APP_CONFIG['dept']} • {APP_CONFIG['year']} • VVCE",
            font_size=sp(11), color=(1, 1, 1, 0.5),
            halign="left", valign="middle", size_hint_y=None, height=dp(18),
        ))
        hdr.add_widget(left)
        hdr.add_widget(Label(text=APP_CONFIG["avatar"], font_size=sp(34),
                             size_hint_x=None, width=dp(56), halign="center"))
        inner.add_widget(hdr)

        # ── Stats row ────────────────────────────────────────────────────────
        stats = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, height=dp(72))
        for val, lbl in [("12", "Events Joined"), ("3", "Books Borrowed"), ("7", "Badges")]:
            stats.add_widget(stat_card(val, lbl))
        inner.add_widget(stats)

        # ── Trending event card ───────────────────────────────────────────────
        ev_hdr = BoxLayout(size_hint_y=None, height=dp(30))
        ev_hdr.add_widget(Label(text="🔥 Trending Events", font_size=sp(15), bold=True,
                                color=C["white"], halign="left"))
        ev_hdr.add_widget(Label(text="See all →", font_size=sp(12),
                                color=C["mintAccent"], halign="right"))
        inner.add_widget(ev_hdr)

        self._ev_card = BoxLayout(orientation="vertical", spacing=dp(6),
                                  size_hint_y=None, height=dp(130), padding=dp(16))
        make_glass_bg(self._ev_card)
        inner.add_widget(self._ev_card)
        self._refresh_event()
        Clock.schedule_interval(self._rotate_event, 3)

        # ── Quick access grid ─────────────────────────────────────────────────
        inner.add_widget(Label(text="⚡ Quick Access", font_size=sp(15), bold=True,
                               color=C["white"], size_hint_y=None, height=dp(30), halign="left"))

        features = [
            ("🎯", "Events",        "events"),
            ("📚", "Library",       "library"),
            ("📡", "QR Attend",     "qr"),
            ("👤", "Profile",       "profile"),
            ("🏆", "Leaderboard",   "leaderboard"),
            ("🔔", "Notifications", "notifications"),
            ("🤖", "CampusBot",     "chatbot"),
        ]
        if AppState.role == "admin":
            features.append(("⚙️", "Admin Panel", "admin"))

        cols  = 3
        rows  = (len(features) + cols - 1) // cols
        grid  = GridLayout(cols=cols, spacing=dp(10),
                           size_hint_y=None, height=dp(120) * rows)
        for icon, label, scr in features:
            btn = BoxLayout(orientation="vertical", spacing=dp(4), padding=dp(10))
            make_glass_bg(btn)
            btn.add_widget(Label(text=icon,  font_size=sp(30), size_hint_y=None,
                                 height=dp(40), halign="center"))
            btn.add_widget(Label(text=label, font_size=sp(11), bold=True, color=C["white"],
                                 size_hint_y=None, height=dp(20), halign="center"))
            btn.bind(on_touch_down=lambda inst, t, s=scr: self._go(s, t, inst))
            grid.add_widget(btn)
        inner.add_widget(grid)

        scroll.add_widget(inner)
        root.add_widget(scroll)
        self.add_widget(root)

    def _refresh_event(self):
        ev = EVENTS[self._ev_idx % len(EVENTS)]
        self._ev_card.clear_widgets()
        self._ev_card.add_widget(Label(
            text=f"{ev['emoji']} {ev['title']}",
            font_size=sp(17), bold=True, color=C["white"],
            size_hint_y=None, height=dp(30), halign="left",
        ))
        self._ev_card.add_widget(Label(
            text=f"📅 {ev['date']}  •  ⏰ {ev['time']}  •  📍 {ev['venue']}",
            font_size=sp(12), color=(1, 1, 1, 0.7),
            size_hint_y=None, height=dp(22), halign="left",
        ))
        self._ev_card.add_widget(Label(
            text=f"🏆 {ev['prize']}   |   {ev['seats']} seats left",
            font_size=sp(13), bold=True, color=C["gold"],
            size_hint_y=None, height=dp(22), halign="left",
        ))

    def _rotate_event(self, dt):
        self._ev_idx += 1
        self._refresh_event()

    def _go(self, scr, touch, widget):
        if widget.collide_point(*touch.pos):
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = scr


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENTS SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class EventsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._filter = "All"
        self._build()

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        root.add_widget(screen_header("🎯 Campus Events",
                                      on_back=lambda *_: self._go_back()))

        # Filter bar (scrollable horizontally)
        filters = ["All", "Hackathon", "Ideathon", "Workshop", "Placement", "Cultural"]
        fbar = ScrollView(size_hint_y=None, height=dp(42), do_scroll_y=False)
        fbar_inner = BoxLayout(spacing=dp(8), size_hint_x=None,
                               width=dp(96) * len(filters))
        self._f_btns: dict = {}
        for f in filters:
            btn = tab_button(f, active=(f == "All"))
            btn.bind(on_press=lambda inst, filt=f: self._set_filter(filt))
            self._f_btns[f] = btn
            fbar_inner.add_widget(btn)
        fbar.add_widget(fbar_inner)
        root.add_widget(fbar)

        self._scroll_box = BoxLayout(orientation="vertical", spacing=dp(10),
                                     size_hint_y=None)
        self._scroll_box.bind(minimum_height=self._scroll_box.setter("height"))
        sv = ScrollView()
        sv.add_widget(self._scroll_box)
        root.add_widget(sv)
        self._render_events()
        self.add_widget(root)

    def _set_filter(self, filt):
        self._filter = filt
        for f, btn in self._f_btns.items():
            btn._tab_col.rgba = C["mintAccent"] if f == filt else (1, 1, 1, 0.08)
        self._render_events()

    def _render_events(self):
        self._scroll_box.clear_widgets()
        for ev in EVENTS:
            if self._filter != "All" and ev["type"] != self._filter:
                continue
            card = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(6),
                             size_hint_y=None, height=dp(130))
            make_glass_bg(card)

            row = BoxLayout(size_hint_y=None, height=dp(30))
            row.add_widget(Label(text=f"{ev['emoji']} {ev['title']}", font_size=sp(15),
                                 bold=True, color=C["white"], halign="left"))
            sc = C["coral"] if ev["seats"] < 15 else C["mintAccent"]
            row.add_widget(Label(text=f"{ev['seats']} left", font_size=sp(11), bold=True,
                                 color=sc, halign="right", size_hint_x=None, width=dp(60)))
            card.add_widget(row)
            card.add_widget(Label(
                text=f"📅 {ev['date']}  •  📍 {ev['venue']}  •  {ev['dept']}",
                font_size=sp(11), color=(1, 1, 1, 0.6),
                size_hint_y=None, height=dp(20), halign="left",
            ))
            card.add_widget(Label(text=f"🏆 {ev['prize']}", font_size=sp(12), bold=True,
                                  color=C["gold"], size_hint_y=None, height=dp(20), halign="left"))

            btn_txt = "✅ Registered!" if ev["id"] in AppState.registered_events else "Register Now →"
            reg_btn = pill_button(btn_txt, font_size=sp(13))
            reg_btn.size_hint_y = None
            reg_btn.height = dp(36)
            reg_btn.bind(on_press=lambda inst, eid=ev["id"]: self._register(eid))
            card.add_widget(reg_btn)
            self._scroll_box.add_widget(card)

    def _register(self, eid):
        AppState.registered_events.add(eid)
        self._render_events()

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  LIBRARY SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class LibraryScreen(Screen):
    _STATUS_COLORS = {
        "Available":    C["mintAccent"],
        "Reserved":     C["gold"],
        "Fully Issued": C["coral"],
        "In Repair":    get_color_from_hex("#9E9E9E"),
    }

    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._filter = "All"
        self._build()

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        root.add_widget(screen_header("📚 Smart Library",
                                      on_back=lambda *_: self._go_back()))

        # Stats
        stat_row = GridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(62))
        avail  = sum(1 for b in BOOKS if b["status"] == "Available")
        issued = sum(1 for b in BOOKS if b["status"] == "Fully Issued")
        for val, lbl, col in [(str(len(BOOKS)), "Total",     C["mintAccent"]),
                               (str(avail),       "Available", C["mintAccent"]),
                               (str(issued),       "Issued",    C["coral"])]:
            stat_row.add_widget(stat_card(val, lbl, col))
        root.add_widget(stat_row)

        # Search
        self._search = TextInput(
            hint_text="🔍 Search by title, author, ISBN...",
            multiline=False, size_hint_y=None, height=dp(44),
            font_size=sp(13), background_color=(1, 1, 1, 0.1),
            foreground_color=C["white"], hint_text_color=(1, 1, 1, 0.4),
            cursor_color=C["white"], padding=[dp(14), dp(12)],
        )
        self._search.bind(text=lambda *_: self._render_books())
        root.add_widget(self._search)

        # Filter bar
        fbar = ScrollView(size_hint_y=None, height=dp(40), do_scroll_y=False)
        fbar_inner = BoxLayout(spacing=dp(8), size_hint_x=None)
        statuses = ["All", "Available", "Reserved", "Fully Issued", "In Repair"]
        fbar_inner.width = dp(96) * len(statuses)
        self._f_btns: dict = {}
        for f in statuses:
            btn = tab_button(f, active=(f == "All"))
            btn.bind(on_press=lambda inst, filt=f: self._set_filter(filt))
            self._f_btns[f] = btn
            fbar_inner.add_widget(btn)
        fbar.add_widget(fbar_inner)
        root.add_widget(fbar)

        self._book_box = BoxLayout(orientation="vertical", spacing=dp(10),
                                   size_hint_y=None)
        self._book_box.bind(minimum_height=self._book_box.setter("height"))
        sv = ScrollView()
        sv.add_widget(self._book_box)
        root.add_widget(sv)
        self._render_books()
        self.add_widget(root)

    def _set_filter(self, filt):
        self._filter = filt
        for f, btn in self._f_btns.items():
            btn._tab_col.rgba = C["mintAccent"] if f == filt else (1, 1, 1, 0.08)
        self._render_books()

    def _render_books(self):
        self._book_box.clear_widgets()
        q = self._search.text.lower() if hasattr(self, "_search") else ""
        for b in BOOKS:
            if self._filter != "All" and b["status"] != self._filter:
                continue
            if q and q not in b["title"].lower() \
                 and q not in b["author"].lower() \
                 and q not in b["isbn"]:
                continue
            h = dp(114) if b["status"] == "Available" else dp(84)
            card = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(4),
                             size_hint_y=None, height=h)
            make_glass_bg(card)
            card.add_widget(Label(text=b["title"], font_size=sp(14), bold=True,
                                  color=C["white"], size_hint_y=None, height=dp(22), halign="left"))
            card.add_widget(Label(
                text=f"by {b['author']}  •  Rack {b['rack']}  •  {b['copies']} copies",
                font_size=sp(11), color=(1, 1, 1, 0.6),
                size_hint_y=None, height=dp(18), halign="left",
            ))
            sc = self._STATUS_COLORS.get(b["status"], C["white"])
            card.add_widget(Label(text=f"[Status] {b['status']}", font_size=sp(11), bold=True,
                                  color=sc, size_hint_y=None, height=dp(18), halign="left"))
            if b["status"] == "Available":
                rb = pill_button("Reserve Book", font_size=sp(13))
                rb.size_hint_y = None
                rb.height = dp(34)
                card.add_widget(rb)
            self._book_box.add_widget(card)

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  QR ATTENDANCE SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class QRScreen(Screen):
    _QR_INTERVAL = 7   # seconds between hash refresh

    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._mode     = "generate" if AppState.role == "teacher" else "scan"
        self._scanned  = False
        self._time_left = self._QR_INTERVAL
        self._qr_hash  = self._gen_hash()
        self._build()
        Clock.unschedule(self._tick)
        Clock.schedule_interval(self._tick, 1)

    def on_leave(self):
        Clock.unschedule(self._tick)

    # ── helpers ──────────────────────────────────────────────────────────────
    def _gen_hash(self):
        ts  = int(time.time() / self._QR_INTERVAL)
        raw = f"TEACHER001_SECRET_{ts}"
        return hashlib.sha256(raw.encode()).hexdigest()[:8].upper()

    def _tick(self, dt):
        self._time_left -= 1
        if self._time_left <= 0:
            self._time_left = self._QR_INTERVAL
            self._qr_hash   = self._gen_hash()
        if hasattr(self, "_timer_lbl"):
            self._timer_lbl.text  = f"{self._time_left}s"
            self._timer_lbl.color = C["coral"] if self._time_left <= 3 else C["mintAccent"]
        if hasattr(self, "_hash_lbl"):
            self._hash_lbl.text = f"HASH: {self._qr_hash}"

    # ── build ─────────────────────────────────────────────────────────────────
    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(14))
        root.add_widget(screen_header("📡 QR Attendance",
                                      on_back=lambda *_: self._go_back()))

        # Mode tabs
        tabs = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        self._mode_btns: dict = {}
        for m, lbl in [("generate", "🎓 Teacher"), ("scan", "👤 Student")]:
            btn = Button(text=lbl, font_size=sp(14), bold=True,
                         background_normal="", background_color=(0, 0, 0, 0), color=C["white"])
            with btn.canvas.before:
                btn._c = Color(*(C["mintAccent"] if m == self._mode else (1, 1, 1, 0.08)))
                btn._r = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(12)])
            btn.bind(
                pos =lambda i, _: setattr(i._r, "pos",  i.pos),
                size=lambda i, _: setattr(i._r, "size", i.size),
            )
            btn.bind(on_press=lambda inst, mode=m: self._set_mode(mode))
            self._mode_btns[m] = btn
            tabs.add_widget(btn)
        root.add_widget(tabs)

        self._content = BoxLayout(orientation="vertical", spacing=dp(14))
        root.add_widget(self._content)
        self._render_mode()
        self.add_widget(root)

    def _set_mode(self, mode):
        self._mode = mode
        for m, btn in self._mode_btns.items():
            btn._c.rgba = C["mintAccent"] if m == mode else (1, 1, 1, 0.08)
        self._render_mode()

    def _render_mode(self):
        self._content.clear_widgets()

        if self._mode == "generate":
            timer_card = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(8),
                                   size_hint_y=None, height=dp(90))
            make_glass_bg(timer_card)
            timer_card.add_widget(Label(text="Dynamic QR — Expires in", font_size=sp(12),
                                        color=(1, 1, 1, 0.6), size_hint_y=None, height=dp(22),
                                        halign="center"))
            self._timer_lbl = Label(text=f"{self._time_left}s", font_size=sp(42), bold=True,
                                    color=C["mintAccent"], size_hint_y=None, height=dp(52),
                                    halign="center")
            timer_card.add_widget(self._timer_lbl)
            self._content.add_widget(timer_card)

            qr_card = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(8),
                                size_hint_y=None, height=dp(200))
            make_glass_bg(qr_card)
            qr_card.add_widget(Label(text="[QR Code Placeholder]", font_size=sp(28),
                                     size_hint_y=None, height=dp(80), halign="center"))
            self._hash_lbl = Label(text=f"HASH: {self._qr_hash}", font_size=sp(13),
                                   color=(1, 1, 1, 0.7), size_hint_y=None, height=dp(24),
                                   halign="center")
            qr_card.add_widget(self._hash_lbl)
            qr_card.add_widget(Label(
                text="📍 GPS: 12.9716°N, 77.5946°E\n🔐 TOTP Signed • Auto-refresh every 7s",
                font_size=sp(11), color=(1, 1, 1, 0.5),
                size_hint_y=None, height=dp(48), halign="center",
            ))
            self._content.add_widget(qr_card)

            sec = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(4),
                            size_hint_y=None, height=dp(120))
            make_glass_bg(sec)
            sec.add_widget(Label(text="🛡️ Security Features", font_size=sp(13), bold=True,
                                 color=C["white"], size_hint_y=None, height=dp(26), halign="left"))
            for feat in ["✅ TOTP 7-second refresh", "✅ GPS payload embedded",
                         "✅ SHA256 signed hash", "✅ Anti-screenshot protection"]:
                sec.add_widget(Label(text=feat, font_size=sp(12), color=(1, 1, 1, 0.8),
                                     size_hint_y=None, height=dp(20), halign="left"))
            self._content.add_widget(sec)

        else:
            if self._scanned:
                succ = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(10),
                                 size_hint_y=None, height=dp(280))
                make_glass_bg(succ)
                succ.add_widget(Label(text="✅", font_size=sp(60),
                                      size_hint_y=None, height=dp(80), halign="center"))
                succ.add_widget(Label(text="Attendance Marked!", font_size=sp(20), bold=True,
                                      color=C["mintAccent"], size_hint_y=None, height=dp(36),
                                      halign="center"))
                for info in ["Distance verified: 23m ≤ 50m ✓", "Timestamp valid ✓", "GPS authentic ✓"]:
                    succ.add_widget(Label(text=info, font_size=sp(12), color=(1, 1, 1, 0.6),
                                          size_hint_y=None, height=dp(22), halign="center"))
                rb = pill_button("Scan Again")
                rb.bind(on_press=lambda *_: self._reset_scan())
                succ.add_widget(rb)
                self._content.add_widget(succ)
            else:
                frame = BoxLayout(orientation="vertical", padding=dp(40), spacing=dp(8),
                                  size_hint_y=None, height=dp(240))
                with frame.canvas.before:
                    Color(*C["mintAccent"])
                    ln = Line(
                        rounded_rectangle=(frame.x, frame.y, frame.width, frame.height, dp(20)),
                        width=2,
                    )
                frame.bind(
                    pos =lambda i, _: setattr(ln, "rounded_rectangle",
                                               (i.x, i.y, i.width, i.height, dp(20))),
                    size=lambda i, _: setattr(ln, "rounded_rectangle",
                                               (i.x, i.y, i.width, i.height, dp(20))),
                )
                frame.add_widget(Label(text="📷", font_size=sp(52),
                                       size_hint_y=None, height=dp(70), halign="center"))
                frame.add_widget(Label(text="Camera Preview\n(tap Scan to simulate)",
                                       font_size=sp(13), color=(1, 1, 1, 0.5),
                                       size_hint_y=None, height=dp(44), halign="center"))
                self._content.add_widget(frame)
                self._content.add_widget(
                    pill_button("📡 Scan QR Code", on_press=lambda *_: self._do_scan()))

    def _do_scan(self):
        self._scanned = True
        self._render_mode()

    def _reset_scan(self):
        self._scanned = False
        self._render_mode()

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  PROFILE SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class ProfileScreen(Screen):
    BADGES   = ["🏆 Winner", "💻 Coder", "📚 Reader", "⚡ Fast", "🎯 Pro"]
    CERTS    = ["ML Workshop 2025", "HackSphere 2025 - Runner Up", "Python Bootcamp"]

    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._build()

    def _build(self):
        root   = BoxLayout(orientation="vertical")
        scroll = ScrollView()
        inner  = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(16),
                           size_hint_y=None)
        inner.bind(minimum_height=inner.setter("height"))

        # Header
        hdr = BoxLayout(size_hint_y=None, height=dp(44))
        hdr.add_widget(back_button(on_press=lambda *_: self._go_back()))
        hdr.add_widget(Widget())
        inner.add_widget(hdr)

        # Avatar / name
        inner.add_widget(Label(text=APP_CONFIG["avatar"], font_size=sp(56),
                               size_hint_y=None, height=dp(70), halign="center"))
        inner.add_widget(Label(text=APP_CONFIG["student_name"], font_size=sp(20), bold=True,
                               color=C["white"], size_hint_y=None, height=dp(30), halign="center"))
        inner.add_widget(Label(
            text=f"{APP_CONFIG['dept']} • {APP_CONFIG['year']} • Roll: {APP_CONFIG['roll']}",
            font_size=sp(12), color=(1, 1, 1, 0.6),
            size_hint_y=None, height=dp(22), halign="center",
        ))

        # Mini stats
        mini = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(20))
        for val, lbl in [("12", "Events"), ("7", "Badges"), ("3", "Books")]:
            col = BoxLayout(orientation="vertical")
            col.add_widget(Label(text=val, font_size=sp(20), bold=True, color=C["mintAccent"],
                                 halign="center", size_hint_y=None, height=dp(28)))
            col.add_widget(Label(text=lbl, font_size=sp(11), color=(1, 1, 1, 0.6),
                                 halign="center", size_hint_y=None, height=dp(18)))
            mini.add_widget(col)
        inner.add_widget(mini)

        # Badges card
        bc = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(8),
                       size_hint_y=None, height=dp(110))
        make_glass_bg(bc)
        bc.add_widget(Label(text="🏅 My Badges", font_size=sp(14), bold=True,
                            color=C["white"], size_hint_y=None, height=dp(26), halign="left"))
        brow = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(34))
        for b in self.BADGES:
            brow.add_widget(Label(text=b, font_size=sp(11), bold=True, color=C["white"],
                                  size_hint_x=None, width=dp(72)))
        bc.add_widget(brow)
        inner.add_widget(bc)

        # Library status
        lc = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(6),
                       size_hint_y=None, height=dp(110))
        make_glass_bg(lc)
        lc.add_widget(Label(text="📚 Library Status", font_size=sp(14), bold=True,
                            color=C["white"], size_hint_y=None, height=dp(26), halign="left"))
        for left_txt, right_txt, col in [
            ("Books Borrowed", "3 / 5",        C["mintAccent"]),
            ("Pending Fine",   "₹15",           C["coral"]),
            ("Due Date",       "May 5, 2026",   C["white"]),
        ]:
            row = BoxLayout(size_hint_y=None, height=dp(22))
            row.add_widget(Label(text=left_txt,  font_size=sp(12), color=(1, 1, 1, 0.7), halign="left"))
            row.add_widget(Label(text=right_txt, font_size=sp(12), bold=True, color=col, halign="right"))
            lc.add_widget(row)
        inner.add_widget(lc)

        # Certificates
        cert = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(6),
                         size_hint_y=None, height=dp(20 + 26 + 28 * len(self.CERTS)))
        make_glass_bg(cert)
        cert.add_widget(Label(text="📜 Certificates Earned", font_size=sp(14), bold=True,
                              color=C["white"], size_hint_y=None, height=dp(26), halign="left"))
        for c in self.CERTS:
            row = BoxLayout(size_hint_y=None, height=dp(26))
            row.add_widget(Label(text=f"🎓 {c}", font_size=sp(12), color=C["white"], halign="left"))
            row.add_widget(Label(text="Download", font_size=sp(12), color=C["mintAccent"],
                                 halign="right", size_hint_x=None, width=dp(70)))
            cert.add_widget(row)
        inner.add_widget(cert)

        # Sign out
        so = pill_button("🚪 Sign Out", bg_color=(0, 0, 0, 0), text_color=C["coral"])
        so.bind(on_press=lambda *_: self._sign_out())
        inner.add_widget(so)

        scroll.add_widget(inner)
        root.add_widget(scroll)
        self.add_widget(root)

    def _sign_out(self):
        AppState.role = "student"
        AppState.registered_events = set()
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "welcome"

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  LEADERBOARD SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class LeaderboardScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._build()

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        root.add_widget(screen_header("🏆 Leaderboard",
                                      on_back=lambda *_: self._go_back()))

        # Podium (2nd / 1st / 3rd)
        podium = BoxLayout(size_hint_y=None, height=dp(140), spacing=dp(10))
        for s, bar_h in zip(
            [LEADERBOARD[1], LEADERBOARD[0], LEADERBOARD[2]],
            [100, 130, 80],
        ):
            col = BoxLayout(orientation="vertical")
            col.add_widget(Label(text=s["medal"], font_size=sp(22),
                                 size_hint_y=None, height=dp(30), halign="center"))
            col.add_widget(Label(text=s["name"].split()[0], font_size=sp(11), bold=True,
                                 color=C["white"], size_hint_y=None, height=dp(20), halign="center"))
            bar = BoxLayout(size_hint_y=None, height=dp(bar_h))
            is_first = s["rank"] == 1
            with bar.canvas.before:
                Color(*hex_color("#FFD54F", 0.3)) if is_first else Color(1, 1, 1, 0.08)
                r = RoundedRectangle(pos=bar.pos, size=bar.size, radius=[dp(8), dp(8), 0, 0])
            bar.bind(
                pos =lambda i, _: setattr(r, "pos",  i.pos),
                size=lambda i, _: setattr(r, "size", i.size),
            )
            bar.add_widget(Label(text=str(s["points"]), font_size=sp(13), bold=True,
                                 color=C["gold"] if is_first else C["white"], halign="center"))
            col.add_widget(bar)
            podium.add_widget(col)
        root.add_widget(podium)

        # Full list
        sv = ScrollView()
        lb = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        lb.bind(minimum_height=lb.setter("height"))
        for s in LEADERBOARD:
            is_me = s.get("isMe", False)
            card  = BoxLayout(size_hint_y=None, height=dp(64), padding=dp(14), spacing=dp(12))
            if is_me:
                make_glass_bg(card, color=hex_color("#4CAF82", 0.08),
                              border=hex_color("#4CAF82", 0.3))
            else:
                make_glass_bg(card, color=(1, 1, 1, 0.05))
            medal_txt = s["medal"] if s["medal"] in ("🥇", "🥈", "🥉") else f"#{s['rank']}"
            card.add_widget(Label(text=medal_txt, font_size=sp(20),
                                  size_hint_x=None, width=dp(36), halign="center"))
            name_col = BoxLayout(orientation="vertical", spacing=dp(2))
            me_tag   = " (You)" if is_me else ""
            name_col.add_widget(Label(
                text=f"{s['name']}{me_tag}", font_size=sp(14), bold=True,
                color=C["mintAccent"] if is_me else C["white"],
                halign="left", size_hint_y=None, height=dp(24),
            ))
            name_col.add_widget(Label(
                text=f"{s['dept']} • {s['badges']} badges",
                font_size=sp(11), color=(1, 1, 1, 0.6),
                halign="left", size_hint_y=None, height=dp(18),
            ))
            card.add_widget(name_col)
            card.add_widget(Label(text=str(s["points"]), font_size=sp(17), bold=True,
                                  color=C["gold"], size_hint_x=None, width=dp(56), halign="right"))
            lb.add_widget(card)
        sv.add_widget(lb)
        root.add_widget(sv)
        self.add_widget(root)

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  NOTIFICATIONS SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class NotificationsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._build()

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))

        mark_all_btn = Button(
            text="Mark all read", font_size=sp(12), bold=True,
            background_normal="", background_color=(0, 0, 0, 0),
            color=C["mintAccent"], size_hint_x=None, width=dp(100),
        )
        mark_all_btn.bind(on_press=lambda *_: self._mark_all())
        root.add_widget(screen_header("🔔 Notifications",
                                      on_back=lambda *_: self._go_back(),
                                      right_widget=mark_all_btn))

        self._notif_box = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        self._notif_box.bind(minimum_height=self._notif_box.setter("height"))
        sv = ScrollView()
        sv.add_widget(self._notif_box)
        root.add_widget(sv)
        self._render_notifs()
        self.add_widget(root)

    def _render_notifs(self):
        self._notif_box.clear_widgets()
        for n in AppState.notifications:
            card = BoxLayout(size_hint_y=None, height=dp(72), padding=dp(14), spacing=dp(12))
            if n["unread"]:
                make_glass_bg(card, color=hex_color("#4CAF82", 0.05),
                              border=hex_color("#4CAF82", 0.2))
            else:
                make_glass_bg(card, color=(1, 1, 1, 0.04))
            card.add_widget(Label(text=n["icon"], font_size=sp(26),
                                  size_hint_x=None, width=dp(36), halign="center"))
            info = BoxLayout(orientation="vertical", spacing=dp(2))
            info.add_widget(Label(text=n["title"], font_size=sp(13), bold=n["unread"],
                                  color=C["white"], halign="left",
                                  size_hint_y=None, height=dp(24)))
            info.add_widget(Label(text=n["time"], font_size=sp(11), color=(1, 1, 1, 0.5),
                                  halign="left", size_hint_y=None, height=dp(18)))
            card.add_widget(info)
            if n["unread"]:
                card.add_widget(Label(text="●", font_size=sp(10), color=C["mintAccent"],
                                      size_hint_x=None, width=dp(12)))
            nid = n["id"]
            card.bind(on_touch_down=lambda inst, t, i=nid: self._mark_one(i, t, inst))
            self._notif_box.add_widget(card)

    def _mark_one(self, nid, touch, widget):
        if not widget.collide_point(*touch.pos):
            return
        for n in AppState.notifications:
            if n["id"] == nid:
                n["unread"] = False
        self._render_notifs()

    def _mark_all(self):
        for n in AppState.notifications:
            n["unread"] = False
        self._render_notifs()

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  ADMIN SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class AdminScreen(Screen):
    _STATS = [
        ("📊", "Total Events",  "24"),
        ("👥", "Registrations", "847"),
        ("📚", "Books",         "1200"),
        ("💰", "Revenue",       "₹48K"),
    ]

    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._tab = "events"
        self._build()

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        root.add_widget(screen_header("⚙️ Admin Panel",
                                      on_back=lambda *_: self._go_back()))

        # Stats grid
        sg = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(110))
        for icon, lbl, val in self._STATS:
            c = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(4))
            make_glass_bg(c)
            c.add_widget(Label(text=icon, font_size=sp(22), size_hint_y=None, height=dp(28), halign="center"))
            c.add_widget(Label(text=val,  font_size=sp(18), bold=True, color=C["mintAccent"],
                               size_hint_y=None, height=dp(24), halign="center"))
            c.add_widget(Label(text=lbl,  font_size=sp(10), color=(1, 1, 1, 0.6),
                               size_hint_y=None, height=dp(16), halign="center"))
            sg.add_widget(c)
        root.add_widget(sg)

        # Tabs
        tabs = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        self._tab_btns: dict = {}
        for t in ["events", "library", "notifications"]:
            btn = tab_button(t.capitalize(), active=(t == self._tab))
            btn.width = None
            btn.size_hint_x = 1
            btn.bind(on_press=lambda inst, tab=t: self._set_tab(tab))
            self._tab_btns[t] = btn
            tabs.add_widget(btn)
        root.add_widget(tabs)

        self._tab_content = BoxLayout(orientation="vertical", spacing=dp(10),
                                      size_hint_y=None)
        self._tab_content.bind(minimum_height=self._tab_content.setter("height"))
        sv = ScrollView()
        sv.add_widget(self._tab_content)
        root.add_widget(sv)
        self._render_tab()
        self.add_widget(root)

    def _set_tab(self, tab):
        self._tab = tab
        for t, btn in self._tab_btns.items():
            btn._tab_col.rgba = C["mintAccent"] if t == tab else (1, 1, 1, 0.08)
        self._render_tab()

    def _render_tab(self):
        self._tab_content.clear_widgets()
        if self._tab == "events":
            self._tab_content.add_widget(pill_button("+ Add New Event", font_size=sp(13)))
            for ev in EVENTS:
                card = BoxLayout(size_hint_y=None, height=dp(62), padding=dp(12), spacing=dp(8))
                make_glass_bg(card)
                info = BoxLayout(orientation="vertical", spacing=dp(2))
                info.add_widget(Label(text=f"{ev['emoji']} {ev['title']}", font_size=sp(13),
                                      bold=True, color=C["white"], halign="left",
                                      size_hint_y=None, height=dp(24)))
                info.add_widget(Label(text=f"{ev['type']} • {ev['seats']} seats left",
                                      font_size=sp(11), color=(1, 1, 1, 0.6),
                                      halign="left", size_hint_y=None, height=dp(18)))
                card.add_widget(info)
                for txt, col in [("✏️", (1, 1, 1, 0.1)), ("🗑", hex_color("#FF6B6B", 0.15))]:
                    btn = Button(text=txt, font_size=sp(16), size_hint_x=None, width=dp(36),
                                 background_normal="", background_color=col, color=C["white"])
                    card.add_widget(btn)
                self._tab_content.add_widget(card)

        elif self._tab == "library":
            self._tab_content.add_widget(pill_button("+ Add New Book", font_size=sp(13)))
            for b in BOOKS:
                card = BoxLayout(size_hint_y=None, height=dp(56), padding=dp(12), spacing=dp(8))
                make_glass_bg(card)
                info = BoxLayout(orientation="vertical", spacing=dp(2))
                info.add_widget(Label(text=b["title"], font_size=sp(13), bold=True,
                                      color=C["white"], halign="left", size_hint_y=None, height=dp(22)))
                info.add_widget(Label(text=f"Rack {b['rack']} • {b['copies']} copies",
                                      font_size=sp(11), color=(1, 1, 1, 0.6),
                                      halign="left", size_hint_y=None, height=dp(18)))
                card.add_widget(info)
                card.add_widget(Button(text="✏️", font_size=sp(16),
                                       size_hint_x=None, width=dp(36),
                                       background_normal="", background_color=(1, 1, 1, 0.1),
                                       color=C["white"]))
                self._tab_content.add_widget(card)

        else:  # notifications
            notif_card = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10),
                                   size_hint_y=None, height=dp(220))
            make_glass_bg(notif_card)
            notif_card.add_widget(Label(text="📤 Send Notification", font_size=sp(14), bold=True,
                                        color=C["white"], size_hint_y=None, height=dp(26), halign="left"))
            for hint, h, multi in [("Notification title...", dp(44), False),
                                    ("Message body...",       dp(80), True)]:
                ti = TextInput(
                    hint_text=hint, multiline=multi,
                    size_hint_y=None, height=h, font_size=sp(13),
                    background_color=(1, 1, 1, 0.1), foreground_color=C["white"],
                    hint_text_color=(1, 1, 1, 0.4), cursor_color=C["white"],
                    padding=[dp(12), dp(10)],
                )
                notif_card.add_widget(ti)
            notif_card.add_widget(pill_button("Send to All Students", font_size=sp(13)))
            self._tab_content.add_widget(notif_card)

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  CHATBOT SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class ChatBotScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        nav_bg(self)
        self._history: list = []

    def on_pre_enter(self):
        self.clear_widgets()
        nav_bg(self)
        self._build()

    def _build(self):
        root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))

        # Header
        online = Label(text="● Online", font_size=sp(11), bold=True,
                       color=C["mintAccent"], size_hint_x=None, width=dp(70), halign="right")
        root.add_widget(screen_header("🤖 CampusBot AI",
                                      on_back=lambda *_: self._go_back(),
                                      right_widget=online))

        # Chat scroll area
        self._chat_scroll = ScrollView(size_hint=(1, 1))
        self._chat_box    = BoxLayout(
            orientation="vertical", spacing=dp(10),
            size_hint_y=None, padding=[0, dp(6), 0, dp(6)],
        )
        self._chat_box.bind(minimum_height=self._chat_box.setter("height"))
        self._chat_scroll.add_widget(self._chat_box)
        root.add_widget(self._chat_scroll)

        # Typing indicator
        self._typing_lbl = Label(
            text="CampusBot is typing...",
            font_size=sp(12), color=(1, 1, 1, 0.5),
            size_hint_y=None, height=dp(22),
            halign="left", opacity=0,
        )
        root.add_widget(self._typing_lbl)

        # Input row
        input_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        self._input = TextInput(
            hint_text="Ask me anything about campus...",
            multiline=False,
            background_color=(1, 1, 1, 0.1), foreground_color=C["white"],
            hint_text_color=(1, 1, 1, 0.4), cursor_color=C["white"],
            font_size=sp(14), padding=[dp(14), dp(14)],
        )
        self._input.bind(on_text_validate=lambda *_: self._send())
        input_row.add_widget(self._input)

        send_btn = Button(
            text="➤", font_size=sp(20), bold=True,
            size_hint_x=None, width=dp(52),
            background_normal="", background_color=(0, 0, 0, 0),
        )
        with send_btn.canvas.before:
            Color(*C["mintAccent"])
            sb_r = RoundedRectangle(pos=send_btn.pos, size=send_btn.size, radius=[dp(14)])
        send_btn.bind(
            pos =lambda i, _: setattr(sb_r, "pos",  i.pos),
            size=lambda i, _: setattr(sb_r, "size", i.size),
        )
        send_btn.color = C["white"]
        send_btn.bind(on_press=lambda *_: self._send())
        input_row.add_widget(send_btn)
        root.add_widget(input_row)
        self.add_widget(root)

        if not self._history:
            self._add_bubble(
                "Hi! I'm CampusBot 👋\n"
                "Ask me about events, library books, attendance, or anything campus-related!",
                sender="bot",
            )

    # ── Chat bubble ───────────────────────────────────────────────────────────
    def _add_bubble(self, text: str, sender: str = "user"):
        is_user = sender == "user"
        outer   = BoxLayout(size_hint_y=None, orientation="horizontal", padding=[dp(6), 0])

        if is_user:
            outer.add_widget(Widget())

        bubble = BoxLayout(orientation="vertical", size_hint_x=0.78,
                           size_hint_y=None, padding=dp(12))
        if is_user:
            make_glass_bg(bubble, color=hex_color("#4CAF82", 0.25),
                          border=hex_color("#4CAF82", 0.4))
        else:
            make_glass_bg(bubble, color=(1, 1, 1, 0.08), border=(1, 1, 1, 0.15))

        lbl = Label(
            text=text, font_size=sp(13), color=C["white"],
            halign="right" if is_user else "left", valign="top",
            text_size=(Window.width * 0.68, None),
        )
        lbl.bind(texture_size=lbl.setter("size"))
        bubble.add_widget(lbl)
        bubble.bind(minimum_height=bubble.setter("height"))

        outer.height = lbl.texture_size[1] + dp(32)
        lbl.bind(texture_size=lambda inst, val: setattr(outer, "height", val[1] + dp(32)))

        if is_user:
            outer.add_widget(bubble)
        else:
            outer.insert(0, bubble)
            outer.add_widget(Widget())

        self._chat_box.add_widget(outer)
        Clock.schedule_once(lambda dt: setattr(self._chat_scroll, "scroll_y", 0), 0.1)

    # ── Send / API ────────────────────────────────────────────────────────────
    def _send(self):
        text = self._input.text.strip()
        if not text:
            return
        self._input.text = ""
        self._add_bubble(text, sender="user")
        self._history.append({"role": "user", "content": text})
        self._typing_lbl.opacity = 1
        threading.Thread(target=self._call_api, daemon=True).start()

    def _call_api(self):
        api_key = APP_CONFIG["api_key"]
        if api_key == "YOUR_API_KEY_HERE":
            reply = (
                "⚠️ Demo mode — no API key set.\n"
                "Open main.py and replace YOUR_API_KEY_HERE in APP_CONFIG with your real Anthropic key!"
            )
            Clock.schedule_once(lambda dt: self._on_reply(reply), 0)
            return

        try:
            payload = json.dumps({
                "model":      "claude-haiku-4-5-20251001",
                "max_tokens": 512,
                "system":     CAMPUS_SYSTEM_PROMPT,
                "messages":   self._history[-10:],
            }).encode("utf-8")

            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=payload,
                headers={
                    "Content-Type":      "application/json",
                    "x-api-key":         api_key,
                    "anthropic-version": "2023-06-01",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data  = json.loads(resp.read().decode("utf-8"))
                reply = data["content"][0]["text"]

        except urllib.error.HTTPError as e:
            if e.code == 401:
                reply = "❌ Invalid API key. Check APP_CONFIG['api_key'] in main.py."
            elif e.code == 429:
                reply = "⚠️ Too many requests. Please wait a moment and try again."
            else:
                reply = f"❌ API error {e.code}. Check your internet connection."
        except Exception as ex:
            reply = f"❌ Could not connect: {str(ex)[:80]}"

        Clock.schedule_once(lambda dt: self._on_reply(reply), 0)

    def _on_reply(self, reply: str):
        self._typing_lbl.opacity = 0
        self._history.append({"role": "assistant", "content": reply})
        self._add_bubble(reply, sender="bot")

    def _go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
#  ROOT APP
# ═══════════════════════════════════════════════════════════════════════════════
class CampusConnectApp(App):
    def build(self):
        Window.clearcolor = C["navyDark"]
        # On Pydroid 3 this is ignored — device uses real screen size
        Window.size = (APP_CONFIG["win_w"], APP_CONFIG["win_h"])

        sm = ScreenManager()
        for s in [
            WelcomeScreen(name="welcome"),
            DashboardScreen(name="dashboard"),
            EventsScreen(name="events"),
            LibraryScreen(name="library"),
            QRScreen(name="qr"),
            ProfileScreen(name="profile"),
            LeaderboardScreen(name="leaderboard"),
            NotificationsScreen(name="notifications"),
            AdminScreen(name="admin"),
            ChatBotScreen(name="chatbot"),
        ]:
            sm.add_widget(s)
        sm.current = "welcome"

        root = FloatLayout()
        root.add_widget(sm)

        self.navbar = NavBar(sm, size_hint=(1, None), pos_hint={"x": 0, "y": 0})
        root.add_widget(self.navbar)

        def _on_screen(mgr, screen_name):
            hidden = screen_name == "welcome"
            self.navbar.opacity  = 0 if hidden else 1
            self.navbar.disabled = hidden
            self.navbar.set_active(screen_name)

        sm.bind(current=_on_screen)
        return root

    def get_application_name(self):
        return APP_CONFIG["name"]


if __name__ == "__main__":
    CampusConnectApp().run()
