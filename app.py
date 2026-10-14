import os, re, json



from pathlib import Path



from datetime import datetime, date



from io import BytesIO







import pandas as pd



import requests



import streamlit as st







st.set_page_config(page_title="Hunar | Advisor Recruitment", page_icon="📞", layout="wide", initial_sidebar_state="collapsed")







BASE_URL = "https://api.voice.hunar.ai/external/v1"



DEFAULT_SCREENING_ID = "46443ecf-4dac-44d2-9d66-bf68d6af4668"



DEFAULT_SCHEDULING_ID = "9816e513-5ba6-4b7e-9b3f-aec334ffea06"



UNIFIED_AGENT_NAME = "Mumbai Advisor Recruitment — Screening & Interview Scheduling"



DATA_DIR = Path(os.getenv("HUNAR_APP_DATA_DIR", "app_data"))



DATA_DIR.mkdir(parents=True, exist_ok=True)



CALL_LOG = DATA_DIR / "live_call_history.csv"







st.markdown("""



<style>



:root { color-scheme: light; }



[data-testid="stAppViewContainer"] { background: #f5f8fc !important; color: #23334d !important; }



[data-testid="stHeader"] { background: rgba(245,248,252,.94) !important; }



.block-container { padding: 1.35rem 2rem 2.5rem !important; max-width: 1500px !important; }



html, body, [class*="css"] { font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important; }



.hero { padding: 1.55rem 1.8rem; border-radius: 18px; background: linear-gradient(115deg,#eaf1ff 0%,#e8f6f8 58%,#e7f7f1 100%); border: 1px solid #d6e3f3; margin: .2rem 0 1.1rem; box-shadow: 0 8px 24px rgba(48,78,120,.07); }



.hero h1 { color:#203653 !important; margin:0 !important; font-size:clamp(2rem,3vw,2.7rem) !important; letter-spacing:-.025em; }



.hero p { color:#526780 !important; margin:.55rem 0 0 !important; font-size:1rem !important; }



[data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] p, label, .stCaption, [data-testid="stCaptionContainer"] { color: #34465f; }



h1,h2,h3,h4 { color:#203653 !important; letter-spacing:-.015em; }



p, li { color:#34465f; }



/* Premium navigation with high-contrast labels */

[data-testid="stTabs"] {

    margin-top: 10px !important;

}

[data-testid="stTabs"] [role="tablist"] {

    display: flex !important;

    gap: 10px !important;

    flex-wrap: wrap !important;

    padding: 10px !important;

    margin: 8px 0 22px !important;

    background: linear-gradient(135deg, #14243b 0%, #203b5c 100%) !important;

    border: 1px solid #2e496b !important;

    border-radius: 16px !important;

    box-shadow: 0 8px 22px rgba(20,36,59,.14) !important;

}

[data-testid="stTabs"] [role="tablist"] button[role="tab"] {

    flex: 0 0 auto !important;

    border: 1px solid rgba(255,255,255,.20) !important;

    border-radius: 11px !important;

    padding: 12px 18px !important;

    min-height: 48px !important;

    background: #263e5b !important;

    color: #f8fbff !important;

    font-family: "Inter", "Segoe UI", sans-serif !important;

    font-size: 16px !important;

    font-weight: 800 !important;

    letter-spacing: .15px !important;

    opacity: 1 !important;

    transition: background .18s ease, color .18s ease, transform .18s ease !important;

}

[data-testid="stTabs"] [role="tablist"] button[role="tab"] *,

[data-testid="stTabs"] [role="tablist"] button[role="tab"] p,

[data-testid="stTabs"] [role="tablist"] button[role="tab"] div,

[data-testid="stTabs"] [role="tablist"] button[role="tab"] span {

    color: #f8fbff !important;

    font-family: "Inter", "Segoe UI", sans-serif !important;

    font-size: 16px !important;

    font-weight: 800 !important;

    opacity: 1 !important;

}

[data-testid="stTabs"] [role="tablist"] button[role="tab"]:hover {

    background: #365575 !important;

    border-color: #80dce4 !important;

    color: #ffffff !important;

    transform: translateY(-1px) !important;

}

[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] {

    background: linear-gradient(135deg, #0e9aa7 0%, #2563eb 100%) !important;

    color: #ffffff !important;

    border: 1px solid #8be9f0 !important;

    box-shadow: 0 5px 14px rgba(14,154,167,.30) !important;

    font-weight: 900 !important;

}

[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] *,

[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] p,

[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] div,

[data-testid="stTabs"] [role="tablist"] button[role="tab"][aria-selected="true"] span {

    color: #ffffff !important;

    font-weight: 900 !important;

    opacity: 1 !important;

}

[data-testid="stTabs"] [data-baseweb="tab-highlight"],

[data-testid="stTabs"] [data-baseweb="tab-border"] {

    display: none !important;

}

/* Emphasize key upload/download controls and file-format cues */



[data-testid="stFileUploader"] label, [data-testid="stFileUploader"] label p { font-weight:800 !important; color:#203653 !important; font-size:1.02rem !important; }



[data-testid="stWidgetLabel"] p { font-weight:750 !important; color:#293f5a !important; }



[data-testid="stDownloadButton"] button p, [data-testid="stFileUploaderDropzone"] button p { font-weight:800 !important; }



[data-testid="stFileUploaderDropzone"] { background:#ffffff !important; border:2px dashed #8ca9c7 !important; border-radius:12px !important; }



[data-testid="stFileUploaderDropzoneInstructions"] { color:#294563 !important; font-weight:700 !important; }



[data-testid="stMetric"] { background:#ffffff !important; border:1px solid #dce5ef !important; border-radius:14px !important; padding:1rem 1.1rem !important; box-shadow:0 3px 12px rgba(32,54,83,.045) !important; }



[data-testid="stMetricLabel"] { color:#61738a !important; opacity:1 !important; font-weight:650 !important; }



[data-testid="stMetricValue"] { color:#203653 !important; font-weight:760 !important; }



input, textarea, [data-baseweb="select"] > div { border-radius:8px !important; background:#fff !important; color:#23334d !important; border-color:#cbd8e6 !important; }



input::placeholder, textarea::placeholder { color:#8190a5 !important; opacity:1 !important; }



.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button { border-radius:9px !important; min-height:2.65rem !important; padding:.5rem 1rem !important; font-weight:680 !important; transition:all .15s ease-in-out !important; }



.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] { background:#1769aa !important; border-color:#1769aa !important; color:#fff !important; }



.stButton > button[kind="primary"] p, [data-testid="stFormSubmitButton"] > button[kind="primary"] p { color:#fff !important; }



.stButton > button:not([kind="primary"]), .stDownloadButton > button { background:#fff !important; color:#294563 !important; border:1px solid #cbd8e6 !important; }



[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #dce5ef !important; border-radius:10px !important; overflow:hidden !important; }



[data-testid="stAlert"] { border-radius:10px !important; }



details[data-testid="stExpander"] { border:1px solid #dce5ef !important; border-radius:12px !important; background:#fff !important; }



hr { border-color:#dce5ef !important; }



/* Keep the app consistently readable in either OS appearance setting. */



@media (max-width:900px) { .block-container { padding:1rem .85rem 2rem !important; } .hero { padding:1.2rem; } }





/* FINAL TAB LABEL CONTRAST OVERRIDE — color-only fix */

[data-testid="stTabs"] [role="tablist"] [role="tab"],

[data-testid="stTabs"] [role="tablist"] [role="tab"] *,

[data-testid="stTabs"] [role="tablist"] [role="tab"] p,

[data-testid="stTabs"] [role="tablist"] [role="tab"] span,

[data-testid="stTabs"] [role="tablist"] [role="tab"] div,

[data-testid="stTabs"] [role="tablist"] [role="tab"] label {

    color: #FFFFFF !important;

    -webkit-text-fill-color: #FFFFFF !important;

    opacity: 1 !important;

}



</style>



""", unsafe_allow_html=True)











def get_secret(name, default=""):



    try:



        value = st.secrets.get(name, "")



        if value:



            return str(value)



    except Exception:



        pass



    return os.getenv(name, default)







api_key = get_secret("HUNAR_API_KEY")



screening_agent_id = get_secret("SCREENING_AGENT_ID", DEFAULT_SCREENING_ID)



scheduling_agent_id = get_secret("SCHEDULING_AGENT_ID", DEFAULT_SCHEDULING_ID)



headers = {"X-API-Key": api_key, "Content-Type": "application/json"} if api_key else {}







CALL_COLUMNS = ["created_at", "call_date", "candidate_name", "mobile_number", "agent_name", "agent_id", "call_id", "request_id", "status", "duration_seconds", "engagement_status", "approved_interview_venue", "approved_interview_slots", "candidate_intent", "interest_status", "intent_summary", "experience_type", "experience_years", "experience_employer", "experience_details", "mumbai_interview_willingness", "interview_status", "interview_date", "interview_time", "interview_venue", "candidate_preferred_time", "interview_confirmation", "remarks", "recording_url", "do_not_contact", "call_summary", "result_json", "source", "last_checked_at"]







def load_call_log():



    if CALL_LOG.exists():



        try:



            df = pd.read_csv(CALL_LOG, dtype=str).fillna("")



            for c in CALL_COLUMNS:



                if c not in df.columns: df[c] = ""



            return df[CALL_COLUMNS]



        except Exception:



            pass



    return pd.DataFrame(columns=CALL_COLUMNS)







def save_call_log(df):



    DATA_DIR.mkdir(parents=True, exist_ok=True)



    df.reindex(columns=CALL_COLUMNS).to_csv(CALL_LOG, index=False)







def api_request(method, path, payload=None, params=None):



    if not api_key:



        raise RuntimeError("HUNAR_API_KEY is missing. Set it as an environment variable or in .streamlit/secrets.toml.")



    response = requests.request(method, BASE_URL + path, headers=headers, json=payload, params=params, timeout=45)



    try: body = response.json()



    except Exception: body = {"raw": response.text[:1000]}



    if not response.ok:



        raise RuntimeError(f"Hunar API returned HTTP {response.status_code}: {body}")



    return body







def is_true(v):



    return str(v).strip().lower() in {"true", "yes", "y", "1"}







def normalise_columns(df):



    aliases = {"name":"candidate_name", "candidate":"candidate_name", "phone":"mobile_number", "phone_number":"mobile_number", "mobile":"mobile_number", "leadid":"lead_id", "lead id":"lead_id", "consent":"consent_to_call", "call_consent":"consent_to_call"}



    rename = {}



    for c in df.columns:



        key = str(c).strip().lower().replace("-", "_")



        rename[c] = aliases.get(key, key.replace(" ", "_"))



    df = df.rename(columns=rename)



    missing = [c for c in ["candidate_name", "mobile_number"] if c not in df.columns]



    if missing: raise ValueError("CSV is missing required columns: " + ", ".join(missing))



    if "lead_id" not in df.columns: df.insert(0, "lead_id", [f"LEAD-{i+1:04d}" for i in range(len(df))])



    if "consent_to_call" not in df.columns: df["consent_to_call"] = "No"



    if "contact_status" not in df.columns: df["contact_status"] = "Not Contacted"



    return df







def get_agent_list():



    try:



        data = api_request("GET", "/agents/")



        if isinstance(data, list): return data



        for key in ["results", "agents", "data", "items"]:



            if isinstance(data, dict) and isinstance(data.get(key), list): return data[key]



        return []



    except Exception as e:



        st.session_state.agent_fetch_error = str(e)



        return []







def add_call_record(person, agent_name, agent_id, request_id, call_response, source="manual_agent_test", campaign_context=None):

    call_id = call_response.get("id") or call_response.get("call_id") or ""

    now = datetime.now().astimezone().isoformat(timespec="seconds")

    context = campaign_context or {}

    record = {

        "created_at": now, "call_date": datetime.now().astimezone().date().isoformat(),

        "candidate_name": person.get("candidate_name", ""),

        "mobile_number": person.get("mobile_number", ""),

        "agent_name": agent_name, "agent_id": agent_id, "call_id": call_id,

        "request_id": request_id,

        "status": call_response.get("lifecycle_status") or call_response.get("status", "CREATED"),

        "duration_seconds": "", "engagement_status": "",

        "approved_interview_venue": context.get("interview_venue", ""),

        "approved_interview_slots": context.get("available_interview_slots", ""),

        "candidate_intent": "", "interest_status": "", "intent_summary": "",

        "experience_type": "", "experience_years": "", "experience_employer": "",

        "experience_details": "", "mumbai_interview_willingness": "",

        "interview_status": "", "interview_date": "", "interview_time": "",

        "interview_venue": "", "candidate_preferred_time": "",

        "interview_confirmation": "", "remarks": "", "recording_url": "",

        "do_not_contact": "", "call_summary": "", "result_json": "",

        "source": source, "last_checked_at": ""

    }

    log = load_call_log()

    log = pd.concat([log, pd.DataFrame([record])], ignore_index=True)

    save_call_log(log)

    return record





def _flatten_result_objects(value, collected=None):

    """Collect nested dictionaries and decode JSON strings from common Hunar result containers."""

    if collected is None:

        collected = []

    if isinstance(value, str):

        stripped = value.strip()

        if stripped.startswith("{") or stripped.startswith("["):

            try:

                _flatten_result_objects(json.loads(stripped), collected)

            except Exception:

                pass

        return collected

    if isinstance(value, dict):

        collected.append(value)

        for key in ("result", "call_result", "data", "output", "structured_output",

                    "extracted_data", "analysis", "variables", "custom_data", "response",

                    "evaluation", "results"):

            if key in value:

                _flatten_result_objects(value[key], collected)

        return collected

    if isinstance(value, list):

        for item in value:

            _flatten_result_objects(item, collected)

    return collected





def _first_result_value(objects, aliases):

    aliases_lower = {a.lower() for a in aliases}

    for obj in objects:

        for key, value in obj.items():

            if str(key).lower() in aliases_lower and value not in (None, ""):

                if isinstance(value, (dict, list)):

                    return json.dumps(value, ensure_ascii=False)

                return str(value)

    return None





def normalize_interview_date(value, approved_slots=""):
    """Normalize a date using explicit text or the call's approved interview slots."""
    if value is None or not str(value).strip():
        return ""

    text = str(value).strip()
    # Keep ISO dates as-is.
    try:
        return datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        pass

    # First match natural-language dates to a known approved slot, so the year
    # is derived from configured data rather than guessed.
    normalized_text = re.sub(r"(\d+)(st|nd|rd|th)\b", r"\1", text.lower())
    for slot in re.split(r"[;\n]+", str(approved_slots or "")):
        slot = slot.strip()
        try:
            approved_date = datetime.strptime(slot, "%Y-%m-%d %H:%M").date()
        except ValueError:
            continue

        month = approved_date.strftime("%B").lower()
        day = str(approved_date.day)
        padded_day = approved_date.strftime("%d")
        if month in normalized_text and re.search(rf"\b({day}|{padded_day})\b", normalized_text):
            return approved_date.isoformat()

    # Parse a complete date only when the year is explicitly present.
    for fmt in ("%d %B %Y", "%d %b %Y", "%B %d %Y", "%b %d %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return text


def normalize_interview_time(value):
    """Normalize numeric and common spoken times to 24-hour HH:MM."""
    if value is None or not str(value).strip():
        return ""

    text = re.sub(r"\s+", " ", str(value).strip().lower())
    for fmt in ("%H:%M", "%I:%M %p", "%I %p"):
        try:
            return datetime.strptime(text.upper(), fmt).strftime("%H:%M")
        except ValueError:
            pass

    hour_words = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    }
    match = re.search(
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b"
        r"(?:\s+(\d{1,2})\s*minutes?)?\s+"
        r"(in the morning|in the afternoon|in the evening|at night|am|pm)\b",
        text,
    )
    if match:
        hour = hour_words[match.group(1)]
        minute = int(match.group(2) or 0)
        period = match.group(3)
        if minute > 59:
            return text
        if period in ("in the afternoon", "in the evening", "at night", "pm"):
            if hour < 12:
                hour += 12
        elif period in ("in the morning", "am") and hour == 12:
            hour = 0
        return f"{hour:02d}:{minute:02d}"

    return text


def refresh_call_record(call_id):

    data = api_request("GET", f"/calls/{call_id}/")

    log = load_call_log()

    matches = log.index[log["call_id"].astype(str).eq(str(call_id))].tolist()

    result_objects = _flatten_result_objects(data)

    result = {}

    for obj in result_objects:

        # Prefer a structured result object where possible, but retain all nested outputs.

        for k, v in obj.items():

            if isinstance(k, str):

                result[k] = v



    status = data.get("lifecycle_status") or data.get("status") or "UNKNOWN"

    if isinstance(data.get("call"), dict):

        status = data["call"].get("lifecycle_status") or data["call"].get("status") or status

    duration = _first_result_value(result_objects, ["duration_seconds", "duration", "call_duration"])

    engagement = _first_result_value(result_objects, ["engagement_status", "engagement"])

    now = datetime.now().astimezone().isoformat(timespec="seconds")



    field_map = {

        "candidate_intent": ["candidate_intent", "intent", "intent_summary", "candidate_goal"],

        "interest_status": ["interest_status", "interest", "candidate_interest"],

        "intent_summary": ["intent_summary", "candidate_intent", "intent", "candidate_goal"],

        "experience_type": ["experience_type", "experience_domain", "work_experience_type", "experience_area"],

        "experience_years": ["experience_years", "years_experience", "work_experience_years", "experience_duration"],

        "experience_employer": ["experience_employer", "previous_employer", "company_name", "worked_at", "employer"],

        "experience_details": ["experience_details", "work_experience_details", "experience_summary"],

        "mumbai_interview_willingness": ["mumbai_interview_willingness", "interview_willingness", "willing_to_attend"],

        "interview_status": ["interview_status", "appointment_status", "booking_status"],

        "interview_date": ["interview_date", "scheduled_date", "appointment_date", "confirmed_date"],

        "interview_time": ["interview_time", "scheduled_time", "appointment_time", "confirmed_time"],

        "interview_venue": ["interview_venue", "venue", "location", "office_address"],

        "candidate_preferred_time": ["candidate_preferred_time", "alternative_request_time", "requested_alternative_time", "best_callback_time", "preferred_time"],

        "interview_confirmation": ["interview_confirmation", "confirmation_details", "explicit_confirmation"],

        "remarks": ["remarks", "recruiter_remarks", "candidate_questions", "notes"],

        "do_not_contact": ["do_not_contact", "dnc"],

        "call_summary": ["call_summary", "summary", "conversation_summary"],

        "recording_url": ["recording_url", "recording", "audio_url"]

    }



    for idx in matches:

        log.loc[idx, "status"] = status

        if duration:

            log.loc[idx, "duration_seconds"] = duration

        if engagement:

            log.loc[idx, "engagement_status"] = engagement
        for target, aliases in field_map.items():
            value = _first_result_value(result_objects, aliases)
            if value is not None and target in log.columns:
                if target == "interview_date":
                    approved_slots = log.loc[idx, "approved_interview_slots"]
                    value = normalize_interview_date(value, approved_slots)
                elif target == "interview_time":
                    value = normalize_interview_time(value)
                log.loc[idx, target] = value

        recording = _first_result_value(result_objects, ["recording_url", "recordingUrl", "audio_url", "recording"])

        if recording:

            log.loc[idx, "recording_url"] = recording

        log.loc[idx, "last_checked_at"] = now

        log.loc[idx, "result_json"] = json.dumps(result, ensure_ascii=False, default=str) if result else log.loc[idx, "result_json"]



    save_call_log(log)

    return data





def valid_phone(phone):



    return bool(re.fullmatch(r"\\+[1-9]\d{7,14}", str(phone).strip()))







st.markdown('<div class="hero"><h1 style="margin:0; color:#172b4d">Recruitment Console</h1><p style="margin:.45rem 0 0 0; color:#475467">Mumbai life-insurance advisor hiring · live calls · interview conversion</p></div>', unsafe_allow_html=True)



if not api_key:



    st.warning("Hunar API key is not configured. Set HUNAR_API_KEY before making live calls.")



else:



    st.caption("Hunar API key detected. Credentials are read from secrets/environment and are not displayed.")



with st.expander("Operational safeguards", expanded=False):



    st.caption("Calls reach real people. Obtain explicit consent before every test/recruitment call. Interview slots must be approved by the recruiter. Never expose API credentials or personal call recordings.")







# Tabs: no preloaded fake leads or placeholder appointments.



tabs = st.tabs(["◈  Overview", "⇧  Lead Import", "✦  Unified Agent", "▤  Call History & Export"])







with tabs[0]:



    log = load_call_log()



    st.subheader("Live operations overview")



    if log.empty:



        st.info("No calls are stored in this app yet. Upload a CSV or open All Agents · Test Call to place an authorized test call. The dashboard will populate from actual call records only.")



        total_calls = completed = engaged = interested = 0



    else:



        total_calls = len(log)



        completed = int(log["status"].astype(str).str.upper().eq("COMPLETED").sum())



        engaged = int(log["engagement_status"].astype(str).str.upper().eq("ENGAGED").sum())



        interested = int(log["interest_status"].astype(str).str.lower().eq("interested").sum())



    c1,c2,c3,c4 = st.columns(4)



    c1.metric("Live calls logged", total_calls)



    c2.metric("Completed calls", completed)



    c3.metric("Engaged calls", engaged)



    c4.metric("Interested results", interested)



    if not log.empty:



        st.markdown("#### Call activity by day")



        daily = log.copy()



        daily["call_date"] = pd.to_datetime(daily["call_date"], errors="coerce").dt.date



        daily_count = daily.groupby("call_date", dropna=True).size().rename("Calls").reset_index()



        if not daily_count.empty:



            daily_count["call_date"] = daily_count["call_date"].astype(str)



            st.bar_chart(daily_count.set_index("call_date")["Calls"], use_container_width=True)



        left,right = st.columns(2)



        with left:



            st.markdown("#### Agent usage")



            usage = log.groupby("agent_name").size().sort_values(ascending=False)



            st.bar_chart(usage)



        with right:



            st.markdown("#### Call outcomes")



            outcomes = log["interest_status"].replace("", "Not yet retrieved").value_counts()



            st.bar_chart(outcomes)



        st.markdown("#### Latest live activity")



        show_cols = [c for c in ["created_at","candidate_name","agent_name","status","duration_seconds","engagement_status","interest_status","interview_status","interview_date","interview_time","call_id"] if c in log.columns]



        st.dataframe(log[show_cols].sort_values("created_at", ascending=False).head(15), use_container_width=True, hide_index=True)



    st.caption(f"Call log location: {CALL_LOG}. The local file persists across app restarts on this machine. Some cloud hosts have ephemeral storage unless a persistent volume/database is configured.")







with tabs[1]:



    st.subheader("Upload lead list (CSV only)")



    st.write("Upload your own CSV. This app starts with **no dummy leads**. Required columns: \\`candidate_name\\`, \\`mobile_number\\`. Recommended: \\`lead_id\\`, \\`consent_to_call\\`, \\`preferred_language\\`, \\`city\\`.")



    template = pd.DataFrame(columns=["lead_id","candidate_name","mobile_number","consent_to_call","preferred_language","city"])



    st.download_button("Download blank CSV template", template.to_csv(index=False).encode("utf-8"), "advisor_leads_template.csv", "text/csv")



    upload = st.file_uploader("Choose input CSV", type=["csv"], key="csv_upload_only")



    if upload is not None:



        try:



            uploaded_df = normalise_columns(pd.read_csv(upload, dtype=str).fillna(""))



            st.success(f"CSV validated: {len(uploaded_df)} rows.")



            st.dataframe(uploaded_df.head(50), use_container_width=True, hide_index=True)



            if "uploaded_leads" not in st.session_state: st.session_state.uploaded_leads = pd.DataFrame()



            if st.button("Use this CSV in this session", type="primary"):



                st.session_state.uploaded_leads = uploaded_df.copy()



                st.success("CSV loaded for this session. Open All Agents · Test Call to trigger a call for a selected row.")



        except Exception as e:



            st.error(str(e))



    if "uploaded_leads" in st.session_state and not st.session_state.uploaded_leads.empty:



        st.markdown("#### Currently loaded leads")



        st.dataframe(st.session_state.uploaded_leads, use_container_width=True, hide_index=True)



        st.download_button("Export loaded CSV", st.session_state.uploaded_leads.to_csv(index=False).encode("utf-8"), "loaded_advisor_leads.csv", "text/csv")







with tabs[2]:



    st.subheader("One agent. One candidate journey.")



    st.markdown("The combined workflow screens the candidate first, captures intent, and only then offers approved Mumbai interview slots to suitable, interested candidates.")



    with st.expander("Recruitment conversation design", expanded=False):



        st.markdown("""



**Call sequence**



1. Introduce the recruiter and the advisor opportunity in Mumbai; ask if it is a convenient time to speak.



2. Check basic fit with one concise question about interest in an advisor role and comfort with a customer-facing/sales-oriented opportunity. Do not ask about licensing, training, or unrelated personal details.



3. If the person is not interested, politely close and respect any do-not-contact request.



4. If interested, capture only relevant experience (if volunteered or one brief question) and whether they can attend an in-person interview in Mumbai.



5. Offer up to two recruiter-approved slots between **09:00 and 18:00 IST inclusive**. Never offer an interview time before 09:00 or after 18:00. Calling hours are separate; do not apply interview-hour limits to placing the call. Calls may be placed at any time and any day, subject to Hunar/provider account policies and recipient consent. If neither works, ask for one alternative within that window and flag it for recruiter confirmation.



6. Repeat the selected date, time and venue; record a booking as confirmed only if the candidate explicitly accepts and the slot is still available.







**FAQ handling**



\\- Role: Explain that the opportunity is to become a life-insurance advisor; the interview will cover responsibilities and next steps.



\\- Location: Share only the approved Mumbai venue provided by the recruiter.



\\- Timing: Offer only the supplied slots, 09:00–18:00 IST.



\\- Compensation, commissions, licensing, training, documents: Do not invent details. Say the recruiter will clarify during the interview.



\\- Not interested / do not contact: Acknowledge and end politely; no scheduling.



""")



    st.markdown("#### Configure the single combined agent")



    st.caption("This updates the existing Screening Agent's server-side prompt and removes configured call-time/day restrictions (08:00–21:00, all days) through Hunar's agent-update endpoint. Interview slots remain restricted separately. It does not create another agent.")



    venue = st.text_input("Approved interview venue in Mumbai", value="Andheri West, Mumbai", placeholder="Enter the approved office address / landmark")



    slot_text = st.text_area("Recruiter-approved interview slots (one per line)", placeholder="2026-10-15 10:30\n2026-10-15 15:00\n2026-10-16 11:00", height=100)



    st.caption("Interview slots only: 09:00–18:00 IST inclusive. Calling time is separate from interview time. Slots are passed into each call; this prototype does not connect to a live calendar or reserve capacity automatically.")



    unified_prompt = """You are Neha, a friendly recruitment coordinator for a life-insurance company hiring advisors in Mumbai. Follow the conversation flow; NEVER read these instructions or headings aloud. The introduction field is the only opening line to speak first. After the candidate answers the name question, acknowledge their name naturally and continue with screening. Do not repeat the introduction or restart the call. Speak naturally, warmly, and concisely. The goal is to screen the candidate and, if suitable and interested, schedule an in-person interview using only recruiter-approved slots supplied in call metadata.







Before speaking, use candidate_provided_context and the recruiter-approved venue/slots supplied in call metadata. Do not ask the candidate to repeat information already present in the lead record; use it only when relevant and never assume unprovided facts. Call flow: (1) introduce yourself and the Mumbai life-insurance advisor opportunity; ask if now is a convenient time. (2) Ask only essential fit questions: whether the candidate is interested in an advisor/customer-facing role and whether they are comfortable exploring a sales-oriented opportunity. If work experience is missing from the lead record, ask one short question about relevant sales/customer/business-development experience; capture employer/company and duration only if the candidate states them. Ask if they can attend an in-person interview in Mumbai. Do not ask about licensing, training, document upload, or unrelated personal information unless the candidate asks. (3) If not interested, respect their answer, capture do_not_contact if requested, and end politely without scheduling. (4) If interested and willing to attend, offer up to two recruiter-approved interview slots supplied in metadata. Interviews must be between 09:00 and 18:00 Asia/Kolkata inclusive; never propose earlier than 09:00 or later than 18:00. Calling time is independent and is not restricted by interview hours. Never invent a date, slot, venue, compensation, commission, licensing rule, or job condition. If no supplied slot works, ask the candidate for a preferred time within 09:00–18:00 and mark it as requested, not confirmed. (5) Read back the venue, date and time. Mark interview_status confirmed only when the candidate explicitly accepts a supplied slot. If the candidate wants an alternative, record the requested alternative for recruiter review; do not claim it is booked.







Use a professional, human conversational tone. Ask one question at a time. Do not interrupt; allow the candidate to answer. If asked about compensation, commission, licensing, training, or documents and the details are not provided, say the recruiter will explain them at the interview. If the candidate asks not to be contacted again, acknowledge and end the call. Never pressure the candidate."""



    unified_objective = "Screen a Mumbai life-insurance advisor lead, capture clear intent and basic relevant fit, then schedule an in-person interview only when the candidate is interested and explicitly accepts an available recruiter-approved slot between 09:00 and 18:00 IST inclusive. Call placement hours are independent of interview hours; platform guardrails still apply to actual call placement."



    unified_intro = "Hello, I’m Neha from the recruitment team. I’m calling about a life-insurance advisor opportunity in Mumbai. May I know who I’m speaking with?"



    unified_result_prompt = "Never read or narrate this result prompt. Return every field in the configured schema. Preserve candidate_name, approved_interview_venue, and approved_interview_slots exactly as provided in call metadata; capture candidate_intent, interview date/time only when accepted, alternative requested time if not scheduled, explicit confirmation, and concise recruiter remarks. Extract only what the candidate explicitly says or what the system actually offered. Do not guess missing values; use an empty string for unknown text fields. Normalize interest_status to interested, not_interested, or undecided. do_not_contact must be a boolean. Capture candidate intent, relevant work experience including employer/company if stated, role/domain and duration in years/months, and concise recruiter remarks. Capture interview_status as not_offered, offered, requested_alternative, confirmed, or declined. Record interview date/time/venue only when offered or accepted in the conversation. A confirmed interview requires explicit candidate acceptance of one of the supplied valid slots and must not be inferred. If the candidate requests another time, record it as requested_alternative and never mark confirmed. Include recording_url only if returned by the call API; otherwise empty. Keep the summary factual and concise."



    unified_schema = {



        "candidate_name": {"type":"string"},

        "approved_interview_venue": {"type":"string"},

        "approved_interview_slots": {"type":"string"},

        "candidate_intent": {"type":"string"},

        "interest_status": {"type":"string","enum":["interested","not_interested","undecided"]},



        "candidate_intent": {"type":"string"},



        "intent_summary": {"type":"string"},



        "do_not_contact": {"type":"boolean"},



        "experience_type": {"type":"string"},



        "experience_years": {"type":"string"},



        "experience_employer": {"type":"string"},



        "experience_details": {"type":"string"},



        "mumbai_interview_willingness": {"type":"string","enum":["yes","no","unclear"]},



        "interview_status": {"type":"string","enum":["not_offered","offered","requested_alternative","confirmed","declined"]},



        "interview_date": {"type":"string"},



        "interview_time": {"type":"string"},



        "interview_venue": {"type":"string"},



        "candidate_preferred_time": {"type":"string"},



        "interview_confirmation": {"type":"string"},



        "remarks": {"type":"string"},



        "recording_url": {"type":"string"},



        "call_summary": {"type":"string"}



    }



    if st.button("Apply combined workflow to Screening Agent", type="primary", disabled=not bool(api_key)):



        if not venue.strip():



            st.error("Enter the approved Mumbai interview venue first.")



        else:



            slots = [x.strip() for x in slot_text.splitlines() if x.strip()]



            bad = []



            for slot in slots:



                try:



                    dt = datetime.strptime(slot, "%Y-%m-%d %H:%M")



                    if not (9 <= dt.hour <= 18) or (dt.hour == 18 and dt.minute > 0): bad.append(slot)



                    if dt.date() < date.today(): bad.append(slot)



                except ValueError:



                    bad.append(slot)



            if bad:



                st.error("Fix these slots. Use YYYY-MM-DD HH:MM, future dates, and 09:00–18:00 inclusive only: " + ", ".join(bad))



            else:



                # Embed the actual venue and approved slots into the server-side prompt. Do not rely on custom_data being visible to the agent.



                slots_for_prompt = "\n".join(f"- {slot}" for slot in slots) if slots else "NO INTERVIEW SLOTS CONFIGURED"



                prompt_with_real_constraints = unified_prompt + f"\n\nRECRUITER-CONFIGURED FACTS FOR THIS CAMPAIGN (authoritative; never override or invent):\nAPPROVED VENUE: {venue.strip()}\nAPPROVED INTERVIEW SLOTS (Asia/Kolkata):\n{slots_for_prompt}\nOnly offer the exact slots above. If no listed slot works, record the candidate's alternative as requested_alternative; do not say it is booked. Never mention June or any date not explicitly listed above. Never substitute another Mumbai address. The only venue you may state is the approved venue above."



                update_payload = {"name": UNIFIED_AGENT_NAME, "agent_prompt": prompt_with_real_constraints, "objective": unified_objective, "introduction": unified_intro, "result_prompt": unified_result_prompt, "result_schema": unified_schema, "guardrails": {"earliest_call_time": "08:00", "last_call_time": "23:59", "allowed_days": ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]}}



                try:



                    with st.spinner("Updating the existing agent configuration in Hunar.AI…"):



                        updated = api_request("PUT", f"/agents/{screening_agent_id}/", payload=update_payload)



                    st.session_state.unified_venue = venue.strip()



                    st.session_state.unified_slots = slots



                    st.success("Combined workflow applied to the existing Screening Agent. No second agent was created.")



                    st.json({k: updated.get(k) for k in ["id", "name", "status", "language"] if k in updated})



                except Exception as e:



                    st.error("Agent update failed. No prompt changes were confirmed. " + str(e))



    if "unified_venue" in st.session_state:



        st.success(f"Configured venue: {st.session_state.unified_venue}")



        st.write("Approved slots for this session:")



        st.write(st.session_state.get("unified_slots", []))



    st.divider()



    st.markdown("#### Trigger a combined screening + interview call")



    st.caption("This uses the single configured Screening Agent. Call only a person who has agreed to the call.")



    loaded_leads = st.session_state.get("uploaded_leads", pd.DataFrame())



    selected_lead = None



    default_name, default_phone = "", ""



    if isinstance(loaded_leads, pd.DataFrame) and not loaded_leads.empty:



        lead_labels = [f"{row.get('candidate_name','')} · {row.get('mobile_number','')} · {row.get('lead_id','')}" for _, row in loaded_leads.iterrows()]



        lead_choice = st.selectbox("Optional: choose a lead from the uploaded CSV", ["Manual entry"] + lead_labels)



        if lead_choice != "Manual entry":



            selected_idx = lead_labels.index(lead_choice)



            selected_lead = loaded_leads.iloc[selected_idx].to_dict()



            default_name = str(selected_lead.get("candidate_name", ""))



            default_phone = str(selected_lead.get("mobile_number", ""))



            st.caption("The CSV row only pre-fills contact details. You must still confirm consent before placing a call.")



    with st.form("combined_call_form"):



        candidate_name = st.text_input("Candidate name", value=default_name, placeholder="Full name")



        candidate_phone = st.text_input("Mobile number", value=default_phone, placeholder="+919876543210")



        call_consent = st.checkbox("I confirm this candidate explicitly consented to this call.")



        trigger_combined = st.form_submit_button("Start screening & interview call", type="primary", use_container_width=True)



    if trigger_combined:



        if not candidate_name.strip(): st.error("Enter candidate name.")



        elif not valid_phone(candidate_phone): st.error("Enter a valid international number, e.g. +919876543210.")



        elif not call_consent: st.error("Call blocked until explicit consent is confirmed.")



        elif not st.session_state.get("unified_venue"):



            st.error("First apply the combined workflow and enter the approved Mumbai venue above.")



        elif not st.session_state.get("unified_slots"):



            st.error("Add at least one recruiter-approved future interview slot before calling.")



        else:



            request_id = f"combined-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"



            custom_data = {"workflow":"combined_screening_interview", "interview_venue":st.session_state["unified_venue"], "available_interview_slots":"; ".join(st.session_state["unified_slots"]), "interview_timezone":"Asia/Kolkata", "interview_window":"09:00-18:00 IST", "source":"advisor_recruitment_ui", "candidate_name":candidate_name.strip(), "candidate_provided_context": json.dumps({k: str(v) for k, v in (selected_lead or {}).items() if k not in {"mobile_number", "consent_to_call"}}, ensure_ascii=False), "instruction":f"Use ONLY this venue: {st.session_state['unified_venue']}. Offer ONLY these approved interview slots: {'; '.join(st.session_state['unified_slots'])}. Never invent dates (especially June), times, or addresses. Interview hours are 09:00-18:00 IST inclusive only. Calling time is separate and is not restricted by these interview hours. Screen first; ask intent and relevant work experience; schedule only if interested and candidate explicitly accepts a listed slot. Do not ask about training or licensing unless asked. Do not claim confirmed unless a listed slot is accepted."}



            payload = {"callee_name":candidate_name.strip(), "mobile_number":candidate_phone.strip(), "agent_id":screening_agent_id, "timezone":"Asia/Kolkata", "request_id":request_id, "custom_data":custom_data, "guardrails":{"earliest_call_time":"08:00","last_call_time":"21:00","allowed_days":["MON","TUE","WED","THU","FRI","SAT","SUN"]}}



            try:



                with st.spinner("Submitting call request to Hunar.AI…"):



                    response = api_request("POST", "/calls/", payload=payload)



                record = add_call_record({"candidate_name":candidate_name.strip(),"mobile_number":candidate_phone.strip()}, UNIFIED_AGENT_NAME, screening_agent_id, request_id, response, source="combined_screening_interview", campaign_context={"interview_venue":st.session_state["unified_venue"], "available_interview_slots":"; ".join(st.session_state["unified_slots"])})



                st.success(f"Call request submitted · {record['status']} · Call ID: {record['call_id']}")



                st.json(response)



                st.info("Calling hours follow Hunar API guardrails (08:00–21:00 requested), independently of the interview time window. Interview offers remain limited to recruiter-approved slots from 09:00 to 18:00 IST. When the call finishes, use Refresh call history to fetch results.")



            except Exception as e: st.error(str(e))







with tabs[3]:



    st.subheader("Call history & results")



    st.caption("Call creation is asynchronous. Use refresh to pull the latest status and structured result from Hunar; NOT_STARTED may mean the request has not entered the calling lifecycle yet.")



    log = load_call_log()



    if log.empty:



        st.info("No live call records yet.")



    else:



        display_cols = [c for c in ["created_at","candidate_name","agent_name","status","duration_seconds","interest_status","candidate_intent","interview_status","interview_date","interview_time","candidate_preferred_time","remarks","call_id"] if c in log.columns]



        st.dataframe(log[display_cols].sort_values("created_at", ascending=False), use_container_width=True, hide_index=True)



        call_ids = log.loc[log["call_id"].astype(str).str.len() > 0, "call_id"].astype(str).tolist()



        if st.button("Refresh call history", type="primary", use_container_width=False, disabled=not bool(call_ids)):



            current_log = load_call_log()



            ids_to_refresh = list(dict.fromkeys(current_log.loc[current_log["call_id"].astype(str).str.len() > 0, "call_id"].astype(str).tolist()))



            ok, failed = 0, []



            progress = st.progress(0)



            for i, cid in enumerate(ids_to_refresh):



                try:



                    data = refresh_call_record(cid)



                    st.session_state.last_refreshed_call_detail = data



                    st.session_state.last_refreshed_call_id = cid



                    ok += 1



                except Exception as exc:



                    failed.append(f"{cid}: {exc}")



                progress.progress((i+1)/max(1,len(ids_to_refresh)))



            st.session_state.pending_refresh_summary = f"Refreshed {ok} of {len(ids_to_refresh)} call records."



            st.session_state.pending_refresh_failures = failed



            st.rerun()



        if st.session_state.get("last_refreshed_call_detail"):



            detail_id = st.session_state.get("last_refreshed_call_id", "")



            detail = st.session_state.last_refreshed_call_detail



            st.markdown("#### Latest fetched call detail")



            st.success(f"{detail_id} · {detail.get('lifecycle_status') or detail.get('status') or 'Unknown'}")



            st.json(detail)



        if st.session_state.get("pending_refresh_summary"):



            st.success(st.session_state.pending_refresh_summary)



            for item in st.session_state.get("pending_refresh_failures", []): st.warning(item[:400])



        if st.session_state.get("pending_refresh_summary"):



            st.success(st.session_state.pending_refresh_summary)



            for item in st.session_state.get("pending_refresh_failures", []): st.warning(item[:400])



        current = load_call_log()



        st.download_button("Download full live call history (CSV)", current.to_csv(index=False).encode("utf-8"), "hunar_live_call_history.csv", "text/csv", type="primary")



        excel_buffer = BytesIO()



        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:



            current.to_excel(writer, index=False, sheet_name="Live Call History")



        st.download_button("Download live call history (Excel)", data=excel_buffer.getvalue(), file_name="hunar_live_call_history.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



        st.caption("The history stores real calls created through this app. Historical calls made elsewhere are not automatically imported; add them through an authorized export/import process if needed.")







st.divider()



st.caption("Prototype notes: no dummy leads or fake appointments are preloaded. The primary journey uses one combined screening-and-interview agent. Call records are stored locally in app_data/live_call_history.csv; use a persistent database for multi-user or cloud production deployments.")
