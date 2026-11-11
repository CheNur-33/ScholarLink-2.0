"""ScholarLink 2.4.2 — Competition-Ready, single-file Streamlit prototype.
All scholarship listings are fictional SAMPLE data, not real offers.
Run locally (PowerShell):
    python -m pip install streamlit==1.67.0
    python -m streamlit run ScholarLink_2_4_2_ALL_IN_ONE.py --theme.base light --theme.primaryColor "#159669" --theme.backgroundColor "#F8FAF9" --theme.secondaryBackgroundColor "#FFFFFF" --theme.textColor "#183429"
For cloud deployment use Streamlit Community Cloud + this file as entrypoint.
"""
from datetime import date, datetime
from html import escape
import streamlit as st

def evaluate(profile, scholarship):
    """Return three-valued preliminary eligibility with explainable criteria."""
    checks = []
    for name, field, accepted in [
        ("Study level", "study_level", scholarship["levels"]),
        ("Field of study", "field", scholarship["fields"]),
        ("Study location", "location", [scholarship["location"]]),
    ]:
        value = profile.get(field)
        result = None if not value else (value in accepted or "All fields" in accepted)
        checks.append({"criterion": name, "result": result,
                       "detail": f"Your value: {value or 'Not provided'}; accepted: {', '.join(accepted)}"})
    cgpa = profile.get("cgpa")
    result = None if cgpa is None else cgpa >= scholarship["min_cgpa"]
    checks.append({"criterion": "Minimum CGPA", "result": result,
                   "detail": f"Your CGPA: {cgpa if cgpa is not None else 'Not provided'}; minimum: {scholarship['min_cgpa']:.2f}"})
    if any(x["result"] is False for x in checks):
        status = "Does not meet listed criteria"
    elif any(x["result"] is None for x in checks):
        status = "Needs verification"
    else:
        status = "Meets listed criteria (preliminary)"
    return {"status": status, "checks": checks, "verified": False}


def match_score(profile, scholarship):
    """Ranking score is relevance only, NOT chance of winning a scholarship."""
    checks = evaluate(profile, scholarship)["checks"]
    weights = [25, 25, 20, 30]  # level, field, location, CGPA; total 100
    scored = sum(weight for check, weight in zip(checks, weights) if check["result"] is True)
    return scored


def ranked_scholarships(profile, scholarships):
    return sorted(scholarships, key=lambda s: (-match_score(profile, s), s["name"]))


def readiness(requirements, statuses):
    if not requirements:
        return 0, 0, 0
    done = sum(statuses.get(name) == "Prepared" for name in requirements)
    return round(100 * done / len(requirements)), done, len(requirements)


def days_remaining(deadline, today=None):
    try:
        return (date.fromisoformat(deadline) - (today or date.today())).days
    except (ValueError, TypeError):
        return None


DEMO_SCHOLARSHIPS = [{'id': 'SCH001', 'name': 'Future Tech Scholars (Demo)', 'provider': 'Technology Fund', 'levels': ['Diploma'], 'fields': ['Computer Science', 'Engineering'], 'min_cgpa': 3.2, 'funding': 'Full', 'location': 'Malaysia', 'deadline': '2027-02-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH002', 'name': 'Community Education Award (Demo)', 'provider': 'Education Trust', 'levels': ['Diploma'], 'fields': ['All fields'], 'min_cgpa': 2.8, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-03-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH003', 'name': 'Women in Digital Innovation (Demo)', 'provider': 'Digital Education Fund', 'levels': ['Degree'], 'fields': ['Computer Science', 'Engineering'], 'min_cgpa': 3.5, 'funding': 'Full', 'location': 'Malaysia', 'deadline': '2027-04-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH004', 'name': 'Green Future Grant (Demo)', 'provider': 'Sustainability Fund', 'levels': ['Degree'], 'fields': ['Engineering', 'Business'], 'min_cgpa': 3.0, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-05-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH005', 'name': 'Young Creators Award (Demo)', 'provider': 'Creative Learning Trust', 'levels': ['Diploma'], 'fields': ['Design', 'Business'], 'min_cgpa': 2.5, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-06-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH006', 'name': 'Academic Excellence Fund (Demo)', 'provider': 'Student Advancement Fund', 'levels': ['Degree'], 'fields': ['All fields'], 'min_cgpa': 3.75, 'funding': 'Full', 'location': 'Malaysia', 'deadline': '2027-01-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH007', 'name': 'STEM Starter Scholarship (Demo)', 'provider': 'Future STEM Trust', 'levels': ['Diploma'], 'fields': ['Computer Science', 'Engineering'], 'min_cgpa': 3.0, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-02-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH008', 'name': 'Business Leadership Award (Demo)', 'provider': 'Entrepreneurship Fund', 'levels': ['Degree'], 'fields': ['Business'], 'min_cgpa': 3.25, 'funding': 'Full', 'location': 'Malaysia', 'deadline': '2027-03-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH009', 'name': 'Creative Media Grant (Demo)', 'provider': 'Media Innovation Fund', 'levels': ['Degree'], 'fields': ['Design', 'Computer Science'], 'min_cgpa': 3.0, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-04-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH010', 'name': 'Rural Education Support (Demo)', 'provider': 'Education Access Foundation', 'levels': ['Diploma'], 'fields': ['All fields'], 'min_cgpa': 2.5, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-05-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH011', 'name': 'Emerging Engineers Award (Demo)', 'provider': 'Engineering Foundation', 'levels': ['Degree'], 'fields': ['Engineering'], 'min_cgpa': 3.4, 'funding': 'Full', 'location': 'Malaysia', 'deadline': '2027-06-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH012', 'name': 'Digital Opportunity Grant (Demo)', 'provider': 'Connected Futures Trust', 'levels': ['Diploma'], 'fields': ['Computer Science', 'Design'], 'min_cgpa': 2.75, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-01-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH013', 'name': 'Future Educators Programme (Demo)', 'provider': 'Learning Futures Trust', 'levels': ['Degree'], 'fields': ['Education'], 'min_cgpa': 3.0, 'funding': 'Full', 'location': 'Malaysia', 'deadline': '2027-02-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH014', 'name': 'Youth Research Grant (Demo)', 'provider': 'Academic Discovery Fund', 'levels': ['Degree'], 'fields': ['Computer Science', 'Education'], 'min_cgpa': 3.3, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-03-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}, {'id': 'SCH015', 'name': 'Career Pathways Scholarship (Demo)', 'provider': 'Student Pathways Trust', 'levels': ['Diploma'], 'fields': ['All fields'], 'min_cgpa': 3.0, 'funding': 'Partial', 'location': 'Malaysia', 'deadline': '2027-04-15', 'requirements': ['Academic transcript status', 'Personal statement', 'Reference letter', 'Eligibility review'], 'description': 'Fictional opportunity created exclusively to demonstrate ScholarLink features. This is NOT an active scholarship.', 'source_url': None, 'is_demo': True}]


# ===============================================================
# SCHOLARLINK 2.4.2 — ONBOARDING UPDATE: one-file Streamlit application
# ===============================================================
# All data, logic, navigation, and styling are in this single file.
# Only dependency: streamlit. Install: python -m pip install streamlit
# Run: python -m streamlit run ScholarLink_2_4_1_ALL_IN_ONE.py --theme.base light


# Additional fictitious opportunities make Foundation and Overseas choices meaningful.
DEMO_SCHOLARSHIPS.extend([
    {"id":"SCH016","name":"Foundation Pathways Grant (Demo)","provider":"Illustrative Foundation Trust","levels":["Foundation"],"fields":["All fields"],"min_cgpa":2.5,"funding":"Partial","location":"Malaysia","deadline":"2027-03-20","requirements":["Academic transcript status","Personal statement","Eligibility review"],"description":"Fictional Foundation-level sample. Not an active scholarship.","source_url":None,"is_demo":True},
    {"id":"SCH017","name":"Global Foundation Starter Award (Demo)","provider":"Illustrative Global Learning Fund","levels":["Foundation"],"fields":["Computer Science","Engineering","Business"],"min_cgpa":3.0,"funding":"Full","location":"Overseas","deadline":"2027-05-20","requirements":["Academic transcript status","Personal statement","Language requirements review","Eligibility review"],"description":"Fictional overseas Foundation sample. Not an active scholarship.","source_url":None,"is_demo":True},
    {"id":"SCH018","name":"International Computing Futures (Demo)","provider":"Illustrative Global Technology Fund","levels":["Degree"],"fields":["Computer Science","Engineering"],"min_cgpa":3.4,"funding":"Full","location":"Overseas","deadline":"2027-04-10","requirements":["Academic transcript status","Personal statement","Language requirements review","Eligibility review"],"description":"Fictional overseas Degree scholarship sample. Not an active scholarship.","source_url":None,"is_demo":True},
    {"id":"SCH019","name":"Overseas Creative Pathways (Demo)","provider":"Illustrative International Arts Trust","levels":["Diploma","Degree"],"fields":["Design","Business"],"min_cgpa":2.9,"funding":"Partial","location":"Overseas","deadline":"2027-06-10","requirements":["Academic transcript status","Portfolio preparation","Language requirements review","Eligibility review"],"description":"Fictional overseas creative studies sample. Not an active scholarship.","source_url":None,"is_demo":True},
    {"id":"SCH020","name":"Foundation Science Opportunity (Demo)","provider":"Illustrative STEM Education Trust","levels":["Foundation"],"fields":["Computer Science","Engineering"],"min_cgpa":2.8,"funding":"Partial","location":"Malaysia","deadline":"2027-02-12","requirements":["Academic transcript status","Personal statement","Eligibility review"],"description":"Fictional local Foundation scholarship sample. Not an active scholarship.","source_url":None,"is_demo":True}
])
SCHOLARSHIPS = DEMO_SCHOLARSHIPS
LOOKUP = {s["id"]: s for s in SCHOLARSHIPS}


# -----------------------------------------------------------------------------
# ScholarLink V2.3: Visual layer and app navigation
# THEME NOTE: A native Streamlit theme must be selected when the SERVER starts.
# Recommended Windows PowerShell command (still just one Python source file):
# python -m streamlit run ScholarLink_2_4_1_ALL_IN_ONE.py --theme.base light --theme.primaryColor "#159669" --theme.backgroundColor "#F8FAF9" --theme.secondaryBackgroundColor "#FFFFFF" --theme.textColor "#183429"
# -----------------------------------------------------------------------------

# ────────────────────── Design system & session state ──────────────────────
st.set_page_config(page_title="ScholarLink 2.4.1 | Your Scholarship Compass", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
st.markdown(r"""<style>
:root{color-scheme:light!important;--sl-green:#159669;--sl-dark:#075C43;--sl-text:#183429;--sl-muted:#4E6B5D;--sl-line:#D4E6DC;--sl-bg:#F8FAF9}
html,body,[data-testid="stApp"],[data-testid="stAppViewContainer"],.stApp{background:#F8FAF9!important;color:#183429!important;color-scheme:light!important}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div{background:#FFFFFF!important;color:#183429!important}
[data-testid="stSidebar"] *{color:#234737}
[data-testid="stHeader"]{background:rgba(248,250,249,.92)!important}
.block-container{padding-top:2.1rem;max-width:1060px}
h1,h2,h3,h4,p,label,span{overflow-wrap:anywhere}
[data-testid="stMarkdownContainer"] p,[data-testid="stCaptionContainer"] p,[data-testid="stWidgetLabel"] p{color:#315542}
[data-testid="stMetric"]{background:#FFFFFF!important;border:1px solid #D6E8DD;border-radius:16px;padding:15px 19px}
[data-testid="stMetricLabel"] *,[data-testid="stMetricValue"] *{color:#0B503A!important}
[data-testid="stButton"] button,[data-testid="stFormSubmitButton"] button,[data-testid="stLinkButton"] a{background:#FFFFFF!important;color:#075C43!important;border:1px solid #B5D9C5!important;border-radius:11px!important;font-weight:650!important;min-height:42px}
[data-testid="stButton"] button:hover,[data-testid="stFormSubmitButton"] button:hover{background:#E8F6F0!important;border-color:#159669!important}
[data-testid="stButton"] button[kind="primary"],[data-testid="stFormSubmitButton"] button[kind="primary"]{background:#159669!important;border-color:#159669!important;color:#FFFFFF!important}
[data-testid="stButton"] button[kind="primary"] p,[data-testid="stFormSubmitButton"] button[kind="primary"] p{color:#FFFFFF!important}
[data-testid="stButton"] button p,[data-testid="stFormSubmitButton"] button p{color:inherit!important}
[data-testid="stButton"] button:focus-visible,input:focus-visible,[role="combobox"]:focus-visible{outline:3px solid #087354!important;outline-offset:2px}
[data-testid="stSelectbox"] [data-baseweb="select"], [data-testid="stSelectbox"] [data-baseweb="select"] > div, [data-testid="stSelectbox"] [role="combobox"], [data-testid="stMultiSelect"] [data-baseweb="select"], [data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stTextArea"] textarea{background:#FFFFFF!important;color:#183429!important;-webkit-text-fill-color:#183429!important;border-color:#BDD8C9!important;color-scheme:light!important}
[data-testid="stSelectbox"] [data-baseweb="select"] svg,[data-testid="stNumberInput"] svg{color:#087354!important;fill:currentColor!important}
[data-testid="stSelectbox"] span,[data-testid="stSelectbox"] input,[data-testid="stNumberInput"] input,[data-testid="stTextInput"] input,[data-testid="stMultiSelect"] span{color:#183429!important;-webkit-text-fill-color:#183429!important}
[data-testid="stNumberInput"] button{background:#E8F6F0!important;color:#075C43!important}
[data-baseweb="popover"],[data-baseweb="popover"] *,[role="listbox"],[role="listbox"] *{background-color:#FFFFFF!important;color:#183429!important;-webkit-text-fill-color:#183429!important;color-scheme:light!important}
[role="option"]:hover,[role="option"][aria-selected="true"]{background-color:#E8F6F0!important}
[data-testid="stTabs"] button{color:#476C57!important}[data-testid="stTabs"] button[aria-selected="true"]{color:#087354!important}
[data-testid="stProgress"] > div > div{background:#E4EFE8!important}
[data-testid="stProgress"] > div > div > div{background:#159669!important}
.sl-logo{font-size:1.77rem;font-weight:850;color:#087354;letter-spacing:-.055em;line-height:1.2}
.sl-tag{font-size:.79rem;color:#607E6C;margin:6px 0 22px}
.sl-over{font-size:.75rem;font-weight:780;color:#087354;letter-spacing:.1em;text-transform:uppercase;margin:0 0 8px}
.sl-h{font-weight:810;color:#153F2C;font-size:1.95rem;letter-spacing:-.045em;line-height:1.18;margin:0 0 9px}
.sl-sub{color:#4E705E;font-size:.94rem;line-height:1.6;margin:0 0 19px}
.sl-hero{background:linear-gradient(117deg,#E1F4E8,#C9ECDD);border:1px solid #B1DDC5;padding:32px 34px;border-radius:22px;margin:0 0 18px}
.sl-hero h1{font-size:2.2rem;line-height:1.17;letter-spacing:-.045em;margin:0 0 12px;color:#075C43!important}
.sl-hero p{color:#2D6048;font-size:1rem;max-width:680px;line-height:1.6;margin:0}
.sl-section{color:#174B32;font-size:1.3rem;font-weight:800;margin:22px 0 10px;letter-spacing:-.025em}
.sl-title{color:#13472F;font-size:1.12rem;font-weight:780;margin:0 0 5px;line-height:1.4}
.sl-meta{color:#55745F;font-size:.84rem;line-height:1.65;margin:0 0 10px}
.sl-pill{display:inline-block;background:#E7F6ED;border:1px solid #BBDFCB;color:#075C43!important;font-size:.76rem;font-weight:750;border-radius:50px;padding:5px 10px;margin:0 6px 6px 0}
.sl-pill-alt{background:#F4F7F5;color:#526D5C!important;border-color:#DDE9E1}
.sl-card-copy{color:#486957;font-size:.87rem;line-height:1.6}
.sl-eyebrow{font-size:.74rem;color:#51816B;text-transform:uppercase;letter-spacing:.07em;font-weight:750}
.sl-banner{background:#E8F6F0;color:#234F3A!important;border:1px solid #B8E1C9;padding:15px 19px;border-radius:14px;line-height:1.6;margin:11px 0 18px}
.sl-banner b{color:#075C43!important}.sl-banner.warning{background:#FFF5DF;border-color:#EAD59D;color:#785419!important}.sl-banner.warning b{color:#785419!important}
.sl-banner.good{background:#E5F6EA;border-color:#B5E1C3}
.sl-banner.bad{background:#FDEFEF;border-color:#F2C5C5;color:#943232!important}
.sl-sample{background:#FFF6E7;border:1px solid #F2DEB8;border-radius:12px;padding:11px 14px;color:#765614!important;font-size:.83rem;margin:8px 0 18px;line-height:1.55}
.sl-empty{background:#E8F6F0;border:1px solid #B7E3D1;border-radius:19px;padding:29px 26px;text-align:center;margin:8px 0 14px}
.sl-empty h3{color:#075C43!important;margin:7px 0 8px;font-size:1.32rem}.sl-empty p{color:#295740!important;margin:0 auto;max-width:520px;line-height:1.65}
.sl-micro{color:#547160;font-size:.81rem;line-height:1.55;margin:3px 0}
.sl-step{border:1px solid #D0E6D8;border-radius:14px;background:#FFFFFF;padding:17px 13px;min-height:96px;text-align:center}
.sl-step strong{color:#075C43;display:block;margin-bottom:5px;font-size:.86rem}.sl-step span{color:#567463;font-size:.77rem}
.sl-stat{color:#20513C;font-weight:780}.sl-divider{border-top:1px solid #D6E8DD;margin:17px 0}
@media(max-width:768px){.block-container{padding:.95rem .85rem 2rem!important}.sl-hero{padding:23px 18px;border-radius:17px}.sl-hero h1{font-size:1.55rem}.sl-h{font-size:1.53rem}.sl-step{min-height:78px;padding:11px 8px}[data-testid="stMetric"]{padding:9px!important}[data-testid="stMetricValue"]{font-size:1.25rem!important}}

/* V2.4.2: semantic criteria-match and readiness indicators. Explicit text labels remain visible. */
.sl-pill.sl-match-high{background:#E5F6EA!important;border-color:#A4D8B5!important;color:#17623C!important}
.sl-pill.sl-match-mid{background:#FFF4D8!important;border-color:#E9CE8D!important;color:#785000!important}
.sl-pill.sl-match-low{background:#FFF0E2!important;border-color:#ECC19E!important;color:#954B15!important}
.sl-pill.sl-match-poor{background:#FDEBEC!important;border-color:#EDB8BE!important;color:#992D38!important}
.sl-action-alert{background:#FDEBEC!important;color:#8C2433!important;border:1px solid #EAB5BC!important;border-left:5px solid #C63C4C!important;border-radius:14px;padding:16px 18px;margin:12px 0 18px;line-height:1.6}
.sl-action-alert b,.sl-action-alert strong{color:#8C2433!important}
.sl-action-done{background:#E5F6EA!important;color:#17623C!important;border:1px solid #A4D8B5!important;border-left:5px solid #159669!important;border-radius:14px;padding:16px 18px;margin:12px 0 18px;line-height:1.6}
.sl-action-done b,.sl-action-done strong{color:#17623C!important}
.sl-readiness-label{color:#174532!important;font-weight:700;font-size:.92rem;margin:9px 0 7px}
.sl-readiness-track{height:10px;width:100%;border-radius:999px;background:#F0E6E6;overflow:hidden;margin:0 0 13px}
.sl-readiness-fill{height:100%;border-radius:999px;transition:width .2s ease}
</style>""", unsafe_allow_html=True)

DEFAULT_PROFILE = {"study_level":"Diploma","field":"Computer Science","cgpa":3.50,"location":"Malaysia"}
STATE_DEFAULTS={"page":"Welcome","profile":DEFAULT_PROFILE.copy(),"profile_saved":False,"onboarded":False,"selected":"SCH001","saved":[],"checklists":{},"statuses":{},"view_category":"All","last_message":"","account_created":False,"demo_display_name":"","demo_email":""}
if not st.session_state.get("v241_initialized",False):
    st.session_state["page"]="Welcome"
    st.session_state["account_created"]=False
    st.session_state["profile_saved"]=False
    st.session_state["onboarded"]=False
    st.session_state["v241_initialized"]=True
for key,value in STATE_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key]=value.copy() if isinstance(value,(dict,list)) else value

CATEGORIES={"All":"All opportunities","Government":"Government","Private":"Private","International":"International"}
# These classifications are explicitly illustrative; the providers above are fictional.
CATEGORY_ASSIGN={"SCH001":"Private","SCH002":"Government","SCH003":"Private","SCH004":"Government","SCH005":"Private","SCH006":"Government","SCH007":"Private","SCH008":"Private","SCH009":"International","SCH010":"Government","SCH011":"Private","SCH012":"International","SCH013":"Government","SCH014":"International","SCH015":"Government","SCH016":"Government","SCH017":"International","SCH018":"International","SCH019":"International","SCH020":"Government"}


def navigate(page,sid=None):
    if sid is not None:
        st.session_state.selected=sid
    st.session_state.page=page
    st.rerun()


def selected_scholarship():
    return LOOKUP.get(st.session_state.selected,SCHOLARSHIPS[0])


def section(title,subtitle="",label="SCHOLARLINK 2.4.2"):
    st.markdown(f'<div class="sl-over">{escape(label)}</div><div class="sl-h">{escape(title)}</div><div class="sl-sub">{escape(subtitle)}</div>',unsafe_allow_html=True)


def banner(title,description,kind="info"):
    style=kind if kind in {"warning","good","bad"} else ""
    st.markdown(f'<div role="status" class="sl-banner {style}"><b>{escape(title)}</b> — {escape(description)}</div>',unsafe_allow_html=True)


def sample_disclosure():
    st.markdown('<div class="sl-sample">ⓘ <b>Sample dataset:</b> All 20 scholarship listings, providers and deadlines are fictional educational examples. None are open for real applications.</div>',unsafe_allow_html=True)


def profile_completeness(profile):
    fields=("study_level","field","cgpa","location")
    return round(100*sum(profile.get(k) not in (None,"") for k in fields)/len(fields))


def deadline_label(s):
    n=days_remaining(s["deadline"])
    if n is None: return "Date unavailable"
    if n<0: return "Sample deadline passed"
    if n==0: return "Sample deadline today"
    return f"{n} days until sample deadline"


def save_opportunity(sid):
    if sid not in st.session_state.saved:
        st.session_state.saved.append(sid)
        return True
    return False


def match_indicator(score):
    """Traffic-light cue for criteria fit, never award probability."""
    if score >= 80:
        return "sl-match-high", "Strong criteria match"
    if score >= 60:
        return "sl-match-mid", "Moderate criteria match"
    if score >= 40:
        return "sl-match-low", "Limited criteria match"
    return "sl-match-poor", "Low criteria match"


def match_badge(score):
    css, meaning = match_indicator(score)
    return f'<span class="sl-pill {css}" aria-label="{score} out of 100; {meaning}">{score}/100 · {meaning}</span>'


def readiness_notice(progress, prepared, count, unfinished):
    """Render accessible state-driven readiness progress and next action."""
    incomplete = progress < 100
    fill = "#C63C4C" if incomplete else "#159669"
    label = f"Application readiness: {progress}% · {prepared}/{count} prepared"
    st.markdown(
        f'<div class="sl-readiness-label">{escape(label)}</div>'
        f'<div class="sl-readiness-track" role="progressbar" '
        f'aria-label="Application readiness" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{progress}">'
        f'<div class="sl-readiness-fill" style="width:{progress}%;background:{fill}"></div></div>',
        unsafe_allow_html=True,
    )
    if incomplete:
        message = f"Prepare or verify: {unfinished[0]}" if unfinished else "Review your outstanding preparation items."
        st.markdown(
            '<div class="sl-action-alert" role="status">'
            '<b>⚠ Action needed — application not yet ready</b> — '
            f'{escape(message)} <span>({count-prepared} item(s) remaining)</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="sl-action-done" role="status">'
            '<b>✓ Preparation complete</b> — All checklist items are marked Prepared. '
            'Please verify official scholarship requirements before applying.</div>',
            unsafe_allow_html=True,
        )


def opportunity_card(s,scope):
    score=match_score(st.session_state.profile,s)
    outcome=evaluate(st.session_state.profile,s)["status"]
    with st.container(border=True):
        l,r=st.columns([4,1.35],gap="medium",vertical_alignment="center")
        with l:
            st.markdown(f'<div class="sl-title">🎓 {escape(s["name"])}</div>'
                        f'<div class="sl-meta">{escape(s["provider"])} · {escape(", ".join(s["levels"]))} · {escape(s["funding"])} funding</div>'
                        + match_badge(score)
                        +                         f'<span class="sl-pill sl-pill-alt">{escape(CATEGORY_ASSIGN.get(s["id"],"Sample"))}</span>'
                        f'<div class="sl-card-copy">📅 {escape(s["deadline"])} · {escape(deadline_label(s))}</div>'
                        f'<div class="sl-micro">{escape(outcome)}. Score reflects listed criteria, not selection chances.</div>',unsafe_allow_html=True)
        with r:
            if st.button("View details",key=f"details_{scope}_{s['id']}",type="primary",use_container_width=True):
                navigate("Scholarship Details",s["id"])
            saved=s["id"] in st.session_state.saved
            if st.button("✓ Saved" if saved else "+ Save",key=f"save_{scope}_{s['id']}",disabled=saved,use_container_width=True):
                save_opportunity(s["id"])
                st.rerun()


def profile_form(key):
    p=st.session_state.profile
    levels=["Foundation","Diploma","Degree"]
    fields=["Computer Science","Engineering","Business","Design","Education"]
    with st.form(f"profile_form_{key}"):
        c1,c2=st.columns(2)
        with c1:
            level=st.selectbox("Study level",levels,index=levels.index(p["study_level"]) if p.get("study_level") in levels else 0)
            cgpa=st.number_input("Academic CGPA (example)",min_value=0.0,max_value=4.0,step=0.05,value=float(p["cgpa"]))
        with c2:
            field=st.selectbox("Field of study",fields,index=fields.index(p["field"]))
            location_options=["Malaysia","Overseas"]
            location=st.selectbox("Study location",location_options,index=location_options.index(p.get("location","Malaysia")) if p.get("location") in location_options else 0)
        submitted=st.form_submit_button("Save academic profile",type="primary",use_container_width=True)
    if submitted:
        st.session_state.profile={"study_level":level,"field":field,"cgpa":float(cgpa),"location":location}
        st.session_state.profile_saved=True
        st.session_state.onboarded=True
        banner("Profile saved","ScholarMatch recommendations now use your updated profile.","good")
    return submitted


def welcome_page():
    st.markdown('<div class="sl-hero"><div class="sl-over">YOUR SCHOLARSHIP COMPASS</div><h1>Find opportunities that fit your future.</h1><p>Explore sample scholarships, understand academic criteria and prepare your journey in one place.</p></div>',unsafe_allow_html=True)
    sample_disclosure()
    section("Discover. Evaluate. Prepare.","Your ScholarLink journey begins here.","WELCOME")
    a,b,c=st.columns(3,gap="small")
    with a: st.markdown('<div class="sl-step"><strong>01 · ScholarMatch</strong><span>Find relevant opportunities</span></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="sl-step"><strong>02 · ScholarCheck</strong><span>Understand requirements</span></div>',unsafe_allow_html=True)
    with c: st.markdown('<div class="sl-step"><strong>03 · ScholarReady</strong><span>Prepare your application</span></div>',unsafe_allow_html=True)
    if st.button("Get Started →",type="primary",use_container_width=True):
        navigate("Create Account")


def create_account_page():
    section("Create Account","Set up a temporary ScholarLink practice identity.","STEP 1 OF 3 · ACCOUNT SETUP")
    banner("Prototype account only","This is a simulated account for testing, not real registration or authentication. Use a nickname and example details; no password is needed.")
    with st.form("create_demo_account"):
        nickname=st.text_input("Display name / nickname",value=st.session_state.demo_display_name,placeholder="e.g. Student A",max_chars=40)
        example_email=st.text_input("Example email (optional)",value=st.session_state.demo_email,placeholder="e.g. student@example.com")
        submitted=st.form_submit_button("Continue to Academic Profile →",type="primary",use_container_width=True)
    if submitted:
        if not nickname.strip():
            banner("Name required","Please enter a nickname to continue.","warning")
        else:
            st.session_state.demo_display_name=nickname.strip()
            st.session_state.demo_email=example_email.strip()
            st.session_state.account_created=True
            navigate("Academic Setup")
    if st.button("← Back to Welcome",use_container_width=True):navigate("Welcome")


def academic_setup_page():
    if not st.session_state.account_created:
        navigate("Create Account")
    section("Academic Profile","Complete your sample study profile to receive personalised recommendations.","STEP 2 OF 3 · ACADEMIC SETUP")
    banner("Practice safely","Use example academic information. Do not enter sensitive personal details.")
    submitted=profile_form("onboarding")
    if submitted:
        navigate("Recommended Scholarships")
    if st.button("← Back to Account Setup",use_container_width=True):navigate("Create Account")


def recommendations_page():
    if not st.session_state.profile_saved:
        navigate("Academic Setup")
    section("Recommended Scholarships",f'Here are the sample opportunities matched to {st.session_state.demo_display_name or "your"} academic profile.',"STEP 3 OF 3 · SCHOLARMATCH")
    sample_disclosure()
    p=st.session_state.profile
    st.caption(f'Based on {p["study_level"]} · {p["field"]} · CGPA {p["cgpa"]:.2f} · {p["location"]}. Scores compare only the illustrated criteria, not award probabilities.')
    matches=ranked_scholarships(p,SCHOLARSHIPS)
    for item in matches[:6]:
        opportunity_card(item,"onboarding_recommendations")
    a,b=st.columns(2)
    with a:
        if st.button("Explore all opportunities →",type="primary",use_container_width=True):navigate("Explore")
    with b:
        if st.button("Go to Home Dashboard →",use_container_width=True):navigate("Home")


def home_page():
    if not st.session_state.profile_saved:
        navigate("Academic Setup" if st.session_state.account_created else "Welcome")
    st.markdown('<div class="sl-hero"><div class="sl-over">WELCOME TO SCHOLARLINK</div><h1>Welcome back to ScholarLink!</h1><p>One academic profile. Relevant matches. Clear eligibility explanations. Organised application preparation.</p></div>',unsafe_allow_html=True)
    sample_disclosure()
    profile=st.session_state.profile
    ranked=ranked_scholarships(profile,SCHOLARSHIPS)
    passing=sum(evaluate(profile,s)["status"].startswith("Meets") for s in SCHOLARSHIPS)
    upcoming=sorted((s for s in SCHOLARSHIPS if days_remaining(s["deadline"]) is not None and days_remaining(s["deadline"])>=0),key=lambda s:s["deadline"])
    nearest=upcoming[0] if upcoming else min(SCHOLARSHIPS,key=lambda s:s["deadline"])
    a,b,c,d=st.columns(4,gap="small")
    a.metric("Sample opportunities",len(SCHOLARSHIPS))
    b.metric("Listed criteria met",passing)
    c.metric("Saved plans",len(st.session_state.saved))
    d.metric("Profile completeness",f"{profile_completeness(profile)}%")
    l,r=st.columns([1.7,1],gap="large")
    with l:
        st.markdown('<div class="sl-section">ScholarMatch · Recommended for you</div>',unsafe_allow_html=True)
        st.caption("Ranked by matching academic criteria; not a guarantee of eligibility or award.")
        for s in ranked[:3]: opportunity_card(s,"home")
        if st.button("Explore all scholarships →",type="primary",use_container_width=True):navigate("Explore")
    with r:
        st.markdown('<div class="sl-section">Your next steps</div>',unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="sl-title">📌 Academic profile</div>',unsafe_allow_html=True)
            st.write(f'**{escape(profile["study_level"])} · {escape(profile["field"])}**')
            st.caption(f'CGPA {profile["cgpa"]:.2f} · {profile["location"]}')
            if st.button("Edit my profile",use_container_width=True):navigate("Profile")
        with st.container(border=True):
            st.markdown('<div class="sl-title">🗓️ Upcoming sample deadline</div>',unsafe_allow_html=True)
            st.write(nearest["name"])
            st.caption(f'{nearest["deadline"]} · {deadline_label(nearest)}')
            if st.button("Open Deadline Centre",use_container_width=True):navigate("Deadline Centre")
        with st.container(border=True):
            st.markdown('<div class="sl-title">📋 Application preparation</div>',unsafe_allow_html=True)
            st.write(f'{len(st.session_state.saved)} saved scholarship plan(s)')
            if st.button("View application journey",use_container_width=True):navigate("My Applications")


def explore_page():
    section("Explore Scholarships","Discover opportunities and review how each sample listing matches your academic profile.","DISCOVERY · SCHOLARMATCH")
    sample_disclosure()
    query=st.text_input("Search by scholarship or provider",placeholder="Try Future Tech, Community or Education...")
    selected_category=st.radio("Scholarship category",["All","Government","Private","International"],horizontal=True,key="view_category")
    c1,c2,c3=st.columns(3,gap="small")
    with c1:level=st.selectbox("Study level",["Any","Foundation","Diploma","Degree"])
    with c2:field=st.selectbox("Field of study",["Any","Computer Science","Engineering","Business","Design","Education"])
    with c3:funding=st.selectbox("Funding",["Any","Full","Partial"])
    location_filter=st.selectbox("Study location",["Any","Malaysia","Overseas"],index=0)
    filtered=[s for s in SCHOLARSHIPS if
        (not query or query.lower() in (s["name"]+" "+s["provider"]).lower())
        and (selected_category=="All" or CATEGORY_ASSIGN.get(s["id"])==selected_category)
        and (level=="Any" or level in s["levels"])
        and (field=="Any" or field in s["fields"] or "All fields" in s["fields"])
        and (funding=="Any" or funding==s["funding"])
        and (location_filter=="Any" or location_filter==s["location"])]
    banner("Search results",f"{len(filtered)} sample listing(s) found · ranked by criteria match.")
    if not filtered:
        st.markdown('<div class="sl-empty"><h3>No matching scholarships</h3><p>Try a broader search term or reset your filters.</p></div>',unsafe_allow_html=True)
        st.caption("To reset the search, clear the search field and choose 'Any' for each filter.")
    else:
        for s in ranked_scholarships(st.session_state.profile,filtered):opportunity_card(s,"explore")


def details_page():
    s=selected_scholarship()
    if st.button("← Back to Explore"):navigate("Explore")
    section(s["name"],f'{s["provider"]} · {s["funding"]} funding · {CATEGORY_ASSIGN.get(s["id"],"Sample")} category',"SCHOLARSHIP INFORMATION")
    sample_disclosure()
    st.markdown(match_badge(match_score(st.session_state.profile,s)) + f'<span class="sl-pill sl-pill-alt">{escape(deadline_label(s))}</span>',unsafe_allow_html=True)
    t1,t2,t3,t4=st.tabs(["Overview","Eligibility","Benefits","Apply / Prepare"])
    with t1:
        st.write(s["description"])
        st.write("**Study levels:** "+", ".join(s["levels"]))
        st.write("**Illustrative location:** "+s["location"])
        st.write("**Sample deadline:** "+s["deadline"])
    with t2:
        st.write(f'**Minimum CGPA:** {s["min_cgpa"]:.2f}')
        st.write("**Eligible fields in sample criteria:** "+", ".join(s["fields"]))
        result=evaluate(st.session_state.profile,s)
        banner("Preliminary result",result["status"],"good" if result["status"].startswith("Meets") else "warning")
    with t3:
        st.write("**Illustrative funding type:** "+s["funding"])
        banner("Sample information","No real sponsorship benefit or monetary value is being advertised.")
    with t4:
        st.write("**Suggested preparation checklist:**")
        for x in s["requirements"]:st.write("• "+x)
        banner("Application planning only","ScholarLink does not submit applications to any real scholarship provider.")
    c1,c2=st.columns(2)
    with c1:
        if st.button("Check with ScholarCheck",type="primary",use_container_width=True):navigate("ScholarCheck")
    with c2:
        saved=s["id"] in st.session_state.saved
        if st.button("✓ Saved" if saved else "Save application plan",disabled=saved,use_container_width=True):
            save_opportunity(s["id"])
            navigate("My Applications")


def eligibility_page():
    s=selected_scholarship()
    section("ScholarCheck","Understand which listed academic criteria are met, unmet or need verification.","INNOVATION 02")
    st.markdown(f'<div class="sl-banner"><b>Selected:</b> {escape(s["name"])}</div>',unsafe_allow_html=True)
    result=evaluate(st.session_state.profile,s)
    status=result["status"]
    banner("Preliminary assessment",status,"good" if status.startswith("Meets") else "bad" if status.startswith("Does not") else "warning")
    with st.container(border=True):
        for item in result["checks"]:
            mark="✅" if item["result"] is True else "❌" if item["result"] is False else "❔"
            st.write(f'{mark} **{item["criterion"]}** — {item["detail"]}')
    banner("Important","This is NOT an official eligibility decision. Verify the full requirements through an authorised provider.")
    a,b=st.columns(2)
    with a:
        if st.button("Start my application journey →",type="primary",use_container_width=True):
            save_opportunity(s["id"])
            navigate("My Applications")
    with b:
        if st.button("Edit academic profile",use_container_width=True):navigate("Profile")


def application_stepper():
    a,b,c,d=st.columns(4,gap="small")
    for target,label,sub in [(a,"01 · Discover","Save an opportunity"),(b,"02 · Evaluate","Check requirements"),(c,"03 · Prepare","Mark checklist items"),(d,"04 · Review","Track next steps")]:
        with target:st.markdown(f'<div class="sl-step"><strong>{escape(label)}</strong><span>{escape(sub)}</span></div>',unsafe_allow_html=True)


def applications_page():
    section("My Applications","ScholarReady · Prepare and track saved scholarship plans in one place.","APPLICATION JOURNEY")
    application_stepper()
    if not st.session_state.saved:
        st.markdown('<div class="sl-empty" role="status"><div style="font-size:1.85rem">🔖</div><h3>No saved scholarships yet</h3><p>Explore scholarship opportunities and save the ones that match your academic goals. Your saved plans will appear here.</p></div>',unsafe_allow_html=True)
        if st.button("Explore Scholarships →",type="primary",use_container_width=True):navigate("Explore")
        return
    for sid in list(st.session_state.saved):
        s=LOOKUP[sid]
        with st.container(border=True):
            st.markdown(f'<div class="sl-title">📋 {escape(s["name"])}</div>',unsafe_allow_html=True)
            st.caption(f'Sample deadline {s["deadline"]} · {deadline_label(s)}')
            states=st.session_state.checklists.setdefault(sid,{})
            for item in s["requirements"]:
                allowed=["Pending","Prepared","Needs review"]
                state=states.get(item,"Pending")
                if state not in allowed:state="Pending"
                states[item]=st.selectbox(item,allowed,index=allowed.index(state),key=f'item_{sid}_{item}')
            progress,prepared,count=readiness(s["requirements"],states)
            unfinished=[item for item in s["requirements"] if states[item]!="Prepared"]
            readiness_notice(progress,prepared,count,unfinished)
            options=["Planning","Preparing","Submitted externally (user-reported)","Closed"]
            current=st.session_state.statuses.get(sid,"Planning")
            st.session_state.statuses[sid]=st.selectbox("Application status (manually reported)",options,index=options.index(current) if current in options else 0,key=f"status_{sid}")
            a,b,c=st.columns(3,gap="small")
            if a.button("ScholarCheck",key=f"check_{sid}",use_container_width=True):navigate("ScholarCheck",sid)
            if b.button("See deadline",key=f"deadline_{sid}",use_container_width=True):navigate("Deadline Centre")
            if c.button("Remove plan",key=f"remove_{sid}",use_container_width=True):
                st.session_state.saved.remove(sid)
                st.rerun()
    st.caption("Checklist and statuses are session-only. They are not shared with providers or permanently stored.")


def deadline_page():
    section("Deadline Centre","An in-app overview of fictional closing dates, saved plans and suggested next actions.","PLAN AHEAD")
    sample_disclosure()
    saved_only=st.checkbox("Show saved plans only",value=False)
    items=[LOOKUP[sid] for sid in st.session_state.saved] if saved_only else SCHOLARSHIPS
    ordered=sorted(items,key=lambda s:s["deadline"])
    if not ordered:
        st.markdown('<div class="sl-empty"><h3>No deadlines in saved plans</h3><p>Save a scholarship in Explore to show its sample deadline here.</p></div>',unsafe_allow_html=True)
        if st.button("Explore opportunities →",type="primary"):navigate("Explore")
        return
    if ordered:
        next_s=next((s for s in ordered if days_remaining(s["deadline"]) is not None and days_remaining(s["deadline"])>=0),None)
        if next_s:banner("Upcoming sample deadline",f'{next_s["name"]} · {next_s["deadline"]} · {deadline_label(next_s)}')
    for s in ordered:
        with st.container(border=True):
            l,r=st.columns([4,1.2],gap="small",vertical_alignment="center")
            with l:
                st.markdown(f'<div class="sl-title">🗓️ {escape(s["name"])}</div><div class="sl-meta">{escape(s["deadline"])} · {escape(deadline_label(s))}</div>',unsafe_allow_html=True)
                if s["id"] in st.session_state.saved:
                    status=st.session_state.statuses.get(s["id"],"Planning")
                    st.caption("Saved plan · "+status)
                else:st.caption("Not saved")
            with r:
                if st.button("View details",key=f"dline_{s['id']}",use_container_width=True):navigate("Scholarship Details",s["id"])
    banner("How reminders work","Deadlines are displayed when you open ScholarLink. V2.4.2 does not send emails, SMS or push notifications.")


def profile_page():
    section("Academic Profile","Manage the shared student profile used by ScholarMatch and ScholarCheck.","STUDENT PROFILE")
    banner("Privacy first","Enter example academic information only. No real transcripts, identification numbers or financial documents are collected.")
    profile_form("profile")
    a,b=st.columns(2)
    if a.button("Reset example profile",use_container_width=True):
        st.session_state.profile=DEFAULT_PROFILE.copy()
        st.session_state.profile_saved=False
        st.rerun()
    if b.button("View my recommendations →",type="primary",use_container_width=True):navigate("Recommended Scholarships")


def about_page():
    section("About ScholarLink","A two-person student innovation project developed from an original UI/UX prototype.","ABOUT THE INNOVATION")
    st.write("**ScholarMatch:** Profile-based discovery and weighted relevance scoring.")
    st.write("**ScholarCheck:** Explainable preliminary assessment against listed academic criteria.")
    st.write("**ScholarReady:** Preparation checklist and user-reported application progress.")
    st.write("**Deadline Centre:** In-app reference for sample closing dates.")
    sample_disclosure()
    banner("Privacy and limitations","There are no real accounts, uploaded documents, scholarship applications or automatic reminders. All user changes stay in this temporary Streamlit session.")
    st.caption("This prototype does not use generative AI and does not predict scholarship award outcomes.")


# ───────────────────────── Onboarding gate & global navigation ─────────────────────────
ONBOARDING_PAGES={"Welcome","Create Account","Academic Setup","Recommended Scholarships"}
if st.session_state.page not in ONBOARDING_PAGES and not st.session_state.profile_saved:
    st.session_state.page="Academic Setup" if st.session_state.account_created else "Welcome"

if st.session_state.page not in {"Welcome","Create Account","Academic Setup"}:
    with st.sidebar:
        st.markdown('<div class="sl-logo">🎓 ScholarLink</div><div class="sl-tag">Your Scholarship Compass · V2.4.2</div>',unsafe_allow_html=True)
        if st.session_state.demo_display_name:
            st.caption("Welcome, " + st.session_state.demo_display_name)
        st.caption("MAIN MENU")
        pages=[("Home","⌂"),("Explore","⌕"),("Recommended Scholarships","★"),("My Applications","▤"),("Deadline Centre","▦"),("Profile","♙"),("About","ⓘ")]
        for page,icon in pages:
            active=st.session_state.page==page
            if st.button(f"{icon}  {page}",key=f"nav_{page}",use_container_width=True,type="primary" if active else "secondary"):
                navigate(page)
        st.divider()
        st.caption("🔒 Temporary practice account · Fictional scholarship listings")
        st.caption("ScholarMatch · ScholarCheck · ScholarReady")

PAGES={"Welcome":welcome_page,"Create Account":create_account_page,"Academic Setup":academic_setup_page,"Recommended Scholarships":recommendations_page,"Home":home_page,"Explore":explore_page,"Scholarship Details":details_page,"ScholarCheck":eligibility_page,"My Applications":applications_page,"Deadline Centre":deadline_page,"Profile":profile_page,"About":about_page}
PAGES.get(st.session_state.page,welcome_page)()
