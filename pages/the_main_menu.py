import streamlit as st
import plotly.express as px
import pandas as pd
import json
import os

from streamlit_option_menu import option_menu
from supabase import create_client


# ==============================================================
# SUPABASE
# ==============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)


# ==============================================================
# JSON FILE PATHS
# ==============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SUGGESTIONS_FILE = os.path.join(
    PROJECT_ROOT,
    "suggestions.json"
)

ANNOUNCEMENTS_FILE = os.path.join(
    PROJECT_ROOT,
    "announcements.json"
)


# ==============================================================
# JSON HELPERS
# ==============================================================

def load_json_file(file_path):

    if not os.path.exists(file_path):
        return []

    if os.path.getsize(file_path) == 0:
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):

        return []


def save_json_file(file_path, data):

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


# ==============================================================
# SIDEBAR
# ==============================================================

with st.sidebar:
    st.markdown("## ⚽ N.I.L.S LEAGUE")


    # ----------------------------------------------------------
    # MAIN MENU
    # ----------------------------------------------------------

    selected_main = option_menu(

        menu_title="MAIN MENU",

        options=[
            "Main",
            "Matches Time",
            "News",
            "Teams",
            "Thanks for",
            "Whatsapp"
        ],

        icons=[
            "bricks",
            "calendar-event",
            "newspaper",
            "people",
            "heart",
            "whatsapp"
        ],

        menu_icon="list",

        default_index=0,

        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent"
            },

            "icon": {
                "font-size": "18px"
            },

            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px",
                "border-radius": "8px"
            },

            "nav-link-selected": {
                "font-size": "15px",
                "font-weight": "bold"
            }
        }
    )


    # ----------------------------------------------------------
    # MAIN MENU VARIABLES
    # ----------------------------------------------------------

    main = selected_main == "Main"

    matches_time = selected_main == "Matches Time"

    news = selected_main == "News"

    teams = selected_main == "Teams"

    thanks_for = selected_main == "Thanks for"

    whatsapp = selected_main == "Whatsapp"

    # ==========================================================
    # SUGGESTIONS
    # ==========================================================

    st.divider()

    st.subheader(
        "💡 الاقتراحات والمشاكل"
    )

    st.write(
        "هل لديك فكرة أو اقتراح لتطوير دوري المدرسة؟ "
        "اكتبه هنا ليصل للمدرسين مباشرة:"
    )

    student_suggestion = st.text_input(
        "اكتب اقتراحك هنا..."
    )


    if st.button(
        "إرسال الاقتراح للمدرسين"
    ):

        if student_suggestion.strip():

            username = st.session_state.get(
                "username",
                "unknown"
            )

            try:

                supabase.table(
                    "suggestions"
                ).insert(
                    {
                        "username": username,
                        "idea": student_suggestion.strip()
                    }
                ).execute()

                st.success(
                    "تم إرسال اقتراحك للمدرسين بنجاح! 🎉"
                )

            except Exception as error:

                st.error(
                    f"حدث خطأ أثناء حفظ الاقتراح: {error}"
                )

        else:

            st.warning(
                "من فضلك اكتب اقتراحك أولاً."
            )

# ==================================================================
# WHATSAPP
# ==================================================================

if whatsapp:

    st.title("🟢 WhatsApp Channel")

    st.subheader(
        "📢 Join the "
        "[WhatsApp Channel](https://whatsapp.com/channel/0029VbDeuTc7j6g05buuUD0S)"
    )

    st.success(
        "Join our WhatsApp channel to stay updated with everything "
        "about the N.I.L.S League!"
    )

    st.divider()

    st.header("Why should I join the WhatsApp channel? 🤔")

    st.subheader("📢 **Website Updates**")
    st.write("- You will know about the latest website updates.")

    st.subheader("🔔 **Choose What You Follow**")
    st.write("- You can choose which updates you want to follow.")

    st.subheader("🌐 **Easy Website Access**")
    st.write("- You can enter the website directly from WhatsApp.")

    st.subheader("🏆 **League News**")
    st.write("- You will receive important league news and announcements.")

    st.subheader("📅 **Match Updates**")
    st.write("- You can stay updated about matches and upcoming events.")

    st.subheader("💡 **Never Miss Important Information**")
    st.write("- You won't miss important information about the N.I.L.S League.")


# ==================================================================
# THANKS FOR
# ==================================================================

if thanks_for:

    st.title("❤️ Thanks for")

    st.write(
        "This section shows the people who helped build and improve "
        "the N.I.L.S League website."
    )

    st.divider()

    selected_thanks = option_menu(
        menu_title="Choose a section",
        options=[
            "Work on Menu",
            "Accepted Suggestions"
        ],
        icons=[
            "people-fill",
            "lightbulb-fill"
        ],
        menu_icon="heart-fill",
        default_index=0,
        orientation="horizontal",
    )

    # --------------------------------------------------------------
    # WORK ON MENU
    # --------------------------------------------------------------

    if selected_thanks == "Work on Menu":

        st.header("👨‍💻 People Who Worked on the Website")

        st.info("First Generation — 2026 to —NOW ")

        st.subheader("👨‍💻 Omar")
        st.write(
            "Had the original idea and built the N.I.L.S League website."
        )

        st.subheader("🏫 School")
        st.write(
            "Thanks to the school for accepting the website "
            "as the main website for the N.I.L.S League."
        )

        st.subheader("🏫Mr Ahmed")
        st.write(
            "Thanks for help us from the begging to the end"
        )

#        st.subheader("🎮 Moaz")
#        st.write(
#            "Had the game idea and created the game."
#        )

    # --------------------------------------------------------------
    # ACCEPTED SUGGESTIONS
    # --------------------------------------------------------------

    elif selected_thanks == "Accepted Suggestions":

        st.header("💡 Accepted Suggestions")

        st.success(
            "Suggestions that were accepted and added to the website."
        )

        st.write("No accepted suggestions yet.")


# ==============================================================
# DEFAULT TEAM VARIABLES
# ==============================================================

a1 = False
b1 = False
c1 = False
d1 = False

a2 = False
b2 = False
c2 = False
d2 = False


# ==============================================================
# TEAMS
# ==============================================================

if teams:

    import streamlit as st

    # =========================
    # STAGE SELECTOR
    # =========================

    st.markdown("""
    <style>
    .stage-title {
        font-size: 16px;
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="stage-title">Choose Stage</div>',
        unsafe_allow_html=True
    )

    stage = st.selectbox(
        "Stage",
        [
            "1st Preparatory",
            "2nd Preparatory"
        ],
        label_visibility="collapsed"
    )

    st.title("TEAMS")

    # ==========================================================
    # 1ST PREPARATORY
    # ==========================================================

    if stage == "1st Preparatory":

        selected_team = option_menu(
            menu_title=None,

            options=[
                "1A",
                "1B",
                "1C",
                "1D"
            ],

            icons=[
                "1-circle",
                "2-circle",
                "3-circle",
                "4-circle"
            ],

            orientation="horizontal",

            default_index=0
        )

        a1 = selected_team == "1A"
        b1 = selected_team == "1B"
        c1 = selected_team == "1C"
        d1 = selected_team == "1D"


    # ==========================================================
    # 2ND PREPARATORY
    # ==========================================================

    elif stage == "2nd Preparatory":

        selected_team = option_menu(
            menu_title=None,

            options=[
                "2A",
                "2B",
                "2C",
                "2D"
            ],

            icons=[
                "1-circle",
                "2-circle",
                "3-circle",
                "4-circle"
            ],

            orientation="horizontal",

            default_index=0
        )

        a2 = selected_team == "2A"
        b2 = selected_team == "2B"
        c2 = selected_team == "2C"
        d2 = selected_team == "2D"


# ==============================================================
# 1A
# ==============================================================

if a1:

    st.image(
        "1a_logo.jpeg",
        width=100
    )

    st.header(":green[1A] status")

    st.subheader(":green[1 PREP]")

    st.subheader("color:🟩")


    st.subheader(":green[1A] chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                0, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )

    st.header("الاحطيات")
    st.write("- ")
    st.write("- ")

    st.image(
        "1a_team.png",
        width=500
    )

# ==============================================================
# 1B
# ==============================================================

if b1:

    st.image(
        "1b_logo.png",
        width=100
    )

    st.header(":red[1]:blue[B] status")

    st.subheader(":red[1] :blue[PREP]")
    st.subheader("color: :red[ba]:blue[rca] 🟦🟥")

    st.subheader(":red[1]:blue[B] chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                0, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )

    st.header("الاحطيات")
    st.write("- ")
    st.write("- ")

    st.image(
        "1b_team.png",
        width=500
    )

# ==============================================================
# 1C
# ==============================================================

if c1:

    st.image(
        "1c_logo.jpeg",
        width=100
    )

    st.header("1C status")

    st.subheader("1 PREP")
    st.subheader("color:⬜")

    st.subheader("1C chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                0, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )

    st.header("الاحطيات")
    st.write("- malek badran")
    st.write("- omar fadel")
    st.write("- hamza sherif")

    st.image(
        "1c_team.png",
        width=500
    )

# ==============================================================
# 1D
# ==============================================================

if d1:

    st.image(
        "1d_logo.jpeg",
        width=100
    )

    st.header(":blue[1D] status")

    st.subheader(":blue[1 PREP]")
    st.subheader("color :blue[main]:🟦")
    st.subheader("color :red[second]:🟥")

    st.subheader(":blue[1D] chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                0, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )

    st.info("التشكيله متغيره غير محدده")

    
# ==============================================================
# 2A
# ==============================================================

if a2:

    st.image(
        "2a_logo.png",
        width=100
    )

    st.header(":yellow[2A] status")
    st.header("color:🟨")

    st.subheader(
        ":yellow[2 PREP]"
    )

    st.subheader(
        ":yellow[2A] chart:-"
    )

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                0, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )

    st.header("الاحطيات")
    st.write("- انس عبد الهادي")
    st.write("- احمد عبد العزيز")
    st.write("- عمر احمد ")

    st.image(
        "2A_TEAM.png",
        width=500
    )


# ==============================================================
# 2B
# ==============================================================

if b2:

    st.image(
        "2b_logo.jpeg",
        width=100
    )

    st.header(":blue[2B] status")
    st.header("color:🟦")

    st.subheader(
        ":blue[2 PREP]"
    )

    st.subheader(
        ":blue[2B] chart:-"
    )

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                1, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )
    st.caption("thanks for yassen shaf3e for help me and made the squade for me")
    st.header("الاحطيات")
    st.write("- ")
    st.write("- ")

    st.image(
        "2b_team_blue.jpeg",
        width=500
    )


# ==============================================================
# 2C
# ==============================================================

if c2:

    st.image(
        "2c_logo_temporory.png",
        width=100
    )

    st.header(":red[2C] status")
    st.header("color:🟥")

    st.subheader(
        ":red[2 PREP]"
    )

    st.subheader(
        ":red[2C] chart:-"
    )

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                3, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )

    st.header("الاحطيات")
    st.write("- yassen khaled")
    st.write("- ziad ibrahim")
    st.write("- mahmoud mohamed")
    st.write("- ادم جمعه")
    st.write("- moazen mostafa")

    st.image(
        "2c_team.png",
        width=500
    )


# ==============================================================
# 2D
# ==============================================================

if d2:

    st.image(
        "2d_logo.jpeg",
        width=100
    )

    st.header(":gray[2D] status")
    st.header("color:⬛")

    st.subheader(
        ":gray[2 PREP]"
    )

    st.subheader(
        ":gray[2D] chart:-"
    )

    data = pd.DataFrame(
        {
            "Matches Played": [
                1, 2, 3, 4, 5, 6
            ],

            "Match Result": [
                1, 0, 0, 0, 0, 0
            ]
        }
    )

    fig = px.line(
        data,
        x="Matches Played",
        y="Match Result",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Matches Played",
        yaxis_title="Match Result",
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "displayModeBar": False
        }
    )
    st.header("البدلاء")
    st.write("- youssef ahmed")
    st.write("- malek ahmed")

    st.image(
        "2D_team.jpeg",
        width=500
    )

# ==============================================================
# LEAGUE STATUS
# ==============================================================

if main:
    st.title(
        "WELCOME TO :green-background[:blue[N.I.L.S]] SCHOOL LEAGE"
    )


    # League Table - Supabase
    teams_response = (
        supabase.table("teams")
        .select("*")
        .execute()
    )

    teams_status = pd.DataFrame(teams_response.data)

    if not teams_status.empty:
        teams_status["points"] = pd.to_numeric(
            teams_status["points"], errors="coerce"
        ).fillna(0)
    teams_status = teams_status.rename(
        columns={
            "team_name": "Team",
            "played": "Played",
            "wins": "Wins",
            "draws": "Draws",
            "losses": "Losses",
            "points": "Points",
        }
    )

    teams_status = teams_status.sort_values(
        by=["Points", "Wins", "rank"],
        ascending=[False, False, True]
    )

    teams_status = teams_status[
        ["Team", "Played", "Wins", "Draws", "Losses", "Points"]
    ]

    st.header("LEAGUE TABLE")

    st.dataframe(
        teams_status,
        hide_index=True,
        use_container_width=True
    )

# ----------------------------------------------------------
# Best GK - Supabase
# ----------------------------------------------------------

    gk_response = (
        supabase.table("goalkeepers")
        .select("*")
        .execute()
    )

    teams_best_gk = pd.DataFrame(gk_response.data)

    if not teams_best_gk.empty:
        teams_best_gk["GK players"] = (
            teams_best_gk["team"].astype(str)
            + "("
            + teams_best_gk["name"].astype(str)
            + ")"
        )

        # Convert statistics to numbers
        for col in ["played", "clean_sheet", "goals_conceded"]:
            teams_best_gk[col] = pd.to_numeric(
                teams_best_gk[col], errors="coerce"
            ).fillna(0)

        # Automatic goalkeeper points:
        teams_best_gk["Points"] = teams_best_gk["points"]

        teams_best_gk = teams_best_gk.rename(
            columns={
                "played": "Played",
                "clean_sheet": "Clean Sheets",

                "goals_conceded": "Goals Conceded",
            }
        )

        teams_best_gk = teams_best_gk[
            [
                "GK players",
                "Played",
                "Clean Sheets",

                "Goals Conceded",
                "Points",

            ]
        ]

        teams_best_gk = teams_best_gk.sort_values(
            by=["Points", "Played"],
            ascending=[False, False]
        )

    st.header("LEAGUE BEST GK")

    st.dataframe(
        teams_best_gk,
        hide_index=True
    )
    #========================================#
    #CB
    #========================================#
    st.divider()
    st.subheader("NO CB SORRY")
    st.divider()

# ----------------------------------------------------------
# Best AT - Supabase
# ----------------------------------------------------------

    at_response = (
        supabase.table("attackers")
        .select("*")
        .execute()
    )

    teams_best_at = pd.DataFrame(at_response.data)

    if not teams_best_at.empty:
        teams_best_at["AT players"] = (
            teams_best_at["team"].astype(str)
            + "("
            + teams_best_at["name"].astype(str)
            + ")"
        )

        teams_best_at = teams_best_at.rename(
            columns={
                "played": "Played",
                "goals": "Scored",
                "assists": "Assists",
            }
        )

        teams_best_at["Points"] = teams_best_at["points"]

        teams_best_at = teams_best_at.sort_values(
            by="Points",
            ascending=False
        )

        teams_best_at = teams_best_at[
            ["AT players", "Played", "Scored", "Assists", "Points"]
        ]

    st.header("LEAGUE BEST AT")

    st.dataframe(
        teams_best_at,
        hide_index=True
    )

# ==============================================================
# MATCHES TIME
# ==============================================================

if matches_time:

    st.header("2026 School League")

    matches_table = pd.DataFrame(
        {
            "": [
                "1", "2", "3", "4", "5", "6", "7",
                "8", "9", "10", "11", "12", "13", "14",
                "15", "16", "17", "18", "19", "20", "21",
                "22", "23", "24", "25", "26", "27", "28"
            ],

            "team(1)": [
                "2A", "2B", "1A", "1C", "2A", "2B", "2C",
                "2D", "2A", "2B", "2C", "2D", "1A", "1B",
                "2A", "2C", "1A", "1B", "1C", "1D", "1A",
                "1B", "2A", "2B", "1A", "1B", "1C", "1D"
            ],

            "team(2)": [
                "2C", "2D", "1B", "1D", "1D", "1C", "1B",
                "1A", "1B", "1A", "1D", "1C", "1C", "1D",
                "2B", "2D", "2C", "2D", "2A", "2B", "1D",
                "1C", "2D", "2C", "2A", "2B", "2C", "2D"
            ],

            "date": [
                "28 September 2026",
                "1 October 2026",
                "5 October 2026",
                "8 October 2026",
                "12 October 2026",
                "15 October 2026",
                "19 October 2026",
                "22 October 2026",
                "26 October 2026",
                "29 October 2026",
                "2 November 2026",
                "5 November 2026",
                "9 November 2026",
                "12 November 2026",
                "16 November 2026",
                "19 November 2026",
                "23 November 2026",
                "26 November 2026",
                "30 November 2026",
                "3 December 2026",
                "7 December 2026",
                "10 December 2026",
                "14 December 2026",
                "17 December 2026",
                "21 December 2026",
                "24 December 2026",
                "28 December 2026",
                "31 December 2026"
            ],

            "day": [
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday",
                "Monday",
                "Thursday"
            ],
            "played": [
                #==========stage1========#
                "played",
                "played",
                "played",
                "played",
                #==========stage2========#
                "played",
                "played",
                "played",
                "played",
                #==========stage3========#
                "played",
                "played",
                "played",
                "played",
                #==========stage4========#
                "not played",
                "not played",
                "not played",
                "not played",
                #==========stage5========#
                "not played",
                "not played",
                "not played",
                "not played",
                #==========stage6========#
                "not played",
                "not played",
                "not played",
                "not played",
                #==========stage7========#
                "not played",
                "not played",
                "not played",
                "not played"
            ],
    
            "stage": [
                #==========stage1========#
                "stage1",
                "stage1",
                "stage1",
                "stage1",
                #==========stage2========#
                "stage2",
                "stage2",
                "stage2",
                "stage2",
                #==========stage3========#
                "stage3",
                "stage3",
                "stage3",
                "stage3",
                #==========stage4========#
                "stage4",
                "stage4",
                "stage4",
                "stage4",
                #==========stage6========#
                "stage5",
                "stage5",
                "stage5",
                "stage5",
                #==========stage6========#
                "stage6",
                "stage6",
                "stage6",
                "stage6",
                #==========stage7========#
                "stage7",
                "stage7",
                "stage7",
                "stage7",
            ],
        }
    )

    st.dataframe(
        matches_table,
        use_container_width=True,
        hide_index=True
    )


# ==============================================================
# NEWS
# ==============================================================

if news:

    st.title("NEWS")


    # ----------------------------------------------------------
    # NEWS MENU
    # ----------------------------------------------------------

    selected_news = option_menu(

        menu_title=None,

        options=[
            "League News",
            "Matchs"
        ],

        icons=[
            "megaphone-fill",
            "graph-up-arrow"
        ],

        orientation="horizontal",

        default_index=0
    )


    # ----------------------------------------------------------
    # LEAGUE NEWS
    # ----------------------------------------------------------

    if selected_news == "League News":

        st.subheader(
            "📢 League News"
        )


        try:

            response = (
                supabase
                .table("announcements")
                .select("*")
                .order(
                    "created_at",
                    desc=True
                )
                .execute()
            )

            announcements = response.data


        except Exception as error:

            st.error(
                f"حدث خطأ أثناء تحميل الأخبار: {error}"
            )

            announcements = []


        if announcements:

            for announcement in announcements:

                if isinstance(
                    announcement,
                    dict
                ):

                    text = announcement.get(
                        "text",
                        ""
                    )

                    author = announcement.get(
                        "author",
                        ""
                    )


                    if author:

                        st.info(
                            f"📢 {text}\n\n"
                            f"— {author}"
                        )

                    else:

                        st.info(
                            f"📢 {text}"
                        )

        else:

            st.write(
                "There is no news for now."
            )

    # ----------------------------------------------------------
    # MATCHS
    # ----------------------------------------------------------

    elif news:

        st.title("⚽ NEWS")

        # =========================
        # 2A vs 2C
        # =========================

        with st.container(border=True):
            st.subheader("🟨 2A")
            st.write("Team 1")
            st.write("0")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")
            st.write("28 September 2026")

            st.divider()

            st.subheader("🟥 2C")
            st.write("Team 2")
            st.write("2")

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("🟨Best Player")
                st.write("awsam")

        with col2:
            with st.container(border=True):
                st.subheader("🟨Best Player🟥")
                st.write("adam aref")

        with col3:
            with st.container(border=True):
                st.subheader("🟥Best Player")
                st.write("adam aref")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("no one")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()

        # =========================
        # 2B vs 2D
        # =========================

        with st.container(border=True):
            st.subheader("🟦 2B")
            st.write("Team 1")
            st.write("1")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")
            st.write("1 October 2026")

            st.divider()

            st.subheader("⬛ 2D")
            st.write("Team 2")
            st.write("1")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("🟦Best Player")
                st.write("ياسين مصطفي")

        with col2:
            with st.container(border=True):
                st.subheader("⬛Best Player🟦")
                st.write("مرسي")
        with col3:
            with st.container(border=True):
                st.subheader("⬛Best Player")
                st.write("مرسي")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("- yassin mostafa")
            st.write("- ياسين معروف")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")
            
        st.divider()

        # =========================
        # 1C vs 1D
        # =========================

        with st.container(border=True):
            st.subheader("⬜1C")
            st.write("Team 1")
            st.write("1")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")
            st.write("(changed) 5 October 2026")

            st.divider()

            st.subheader("🟦1D")
            st.write("Team 2")
            st.write("1")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("⬜ Best Player")
                st.write("omar fadel")

        with col2:
            with st.container(border=True):
                st.subheader("⬜ Best Player 🟦")
                st.write("mohamed khaled")
        with col3:
            with st.container(border=True):
                st.subheader("🟦 Best Player")
                st.write("mohamed khaled")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("malek badran")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()

        # =========================
        # 1B vs 1A
        # =========================

        with st.container(border=True):
            st.subheader("🟥🟦 1B")
            st.write("Team 1")
            st.write("1")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")
            st.write("(changed) 7 October 2026")

            st.divider()

            st.subheader("🟩1A")
            st.write("Team 2")
            st.write("3")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("🟩 Best Player")
                st.write("rayan")

        with col2:
            with st.container(border=True):
                st.subheader("🟩 Best Player 🟥🟦")
                st.write("rayan")
        with col3:
            with st.container(border=True):
                st.subheader("🟥🟦 Best Player")
                st.write("—")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("no one")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()

        # =========================
        # 2A vs 1D
        # =========================

        with st.container(border=True):
            st.subheader("2A")
            st.write("Team 1")
            st.write("1")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")

            st.divider()

            st.subheader("1D")
            st.write("Team 2")
            st.write("0")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("2A Best Player")
                st.write("mazen")

        with col2:
            with st.container(border=True):
                st.subheader(" Best Player ")
                st.write("mazen")
        with col3:
            with st.container(border=True):
                st.subheader("1D Best Player")
                st.write("—")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("ahmed wageh")
            st.write("mazen")
            st.write("awsam")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()

        # =========================
        # 2D vs 1A
        # =========================

        with st.container(border=True):
            st.subheader("1A")
            st.write("Team 1")
            st.write("1")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")

            st.divider()

            st.subheader("2D")
            st.write("Team 2")
            st.write("3")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("1A Best Player")
                st.write("يحيا")

        with col2:
            with st.container(border=True):
                st.subheader(" Best Player ")
                st.write("aser amer")
        with col3:
            with st.container(border=True):
                st.subheader("2D Best Player")
                st.write("aser amer")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("no one")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()

        # =========================
        # 2B vs 1C
        # =========================

        with st.container(border=True):
            st.subheader("1C")
            st.write("Team 1")
            st.write("2")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")

            st.divider()

            st.subheader("2B")
            st.write("Team 2")
            st.write("3")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("1C Best Player")
                st.write("omar")

        with col2:
            with st.container(border=True):
                st.subheader(" Best Player ")
                st.write("yassen shaf3e")
        with col3:
            with st.container(border=True):
                st.subheader("2B Best Player")
                st.write("yassen shaf3e")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("yassen ma3rof")
            st.write("mostafa")
            st.write("adham")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()
        st.divider()
        st.divider()

        # =========================
        # 2C vs 1B
        # =========================

        with st.container(border=True):
            st.subheader("1B")
            st.write("Team 1")
            st.write("1")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")
            st.info("تم عقاب الفائز بالخساره بسبب اعمال شغب")

            st.divider()

            st.subheader("2C")
            st.write("Team 2")
            st.write("2")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("1B Best Player")
                st.write("hassen")

        with col2:
            with st.container(border=True):
                st.subheader(" Best Player ")
                st.write("sigo")
        with col3:
            with st.container(border=True):
                st.subheader("2C Best Player")
                st.write("saged/sigo")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("ادم عارف")
            st.write("ادم شاذلي")
            st.write("محمد عبد الناصر")
            st.write("مالك فكري")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()
        st.divider()
        st.divider()
        # =========================
        # 2A vs 1B
        # =========================

        with st.container(border=True):
            st.subheader("1B")
            st.write("Team 1")
            st.write("0")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")


            st.divider()

            st.subheader("2A")
            st.write("Team 2")
            st.write("4")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("2A Best Player")
                st.write("malek")

        with col2:
            with st.container(border=True):
                st.subheader(" Best Player ")
                st.write("moaz")
        with col3:
            with st.container(border=True):
                st.subheader("1B Best Player")
                st.write("moaz")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("no one")

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()
        st.subheader("next match")
        st.divider()
        
        # =========================
        # 2C vs 1D
        # =========================

        with st.container(border=True):
            st.subheader("2C")
            st.write("Team 1")
            st.write("2")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")


            st.divider()

            st.subheader("1D")
            st.write("Team 2")
            st.write("0")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("2C Best Player")
                st.write("saged/sigo")

        with col2:
            with st.container(border=True):
                st.subheader(" Best Player ")
                st.write("saged/sigo")
        with col3:
            with st.container(border=True):
                st.subheader("1D Best Player")
                st.write("youssef mohamed")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("no one") 

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("no one")

        st.divider()
        st.subheader(":red-background[:red[next match]]")
        st.divider()

        # =========================
        # 2B vs 1A
        # =========================

        with st.container(border=True):
            st.subheader("2B")
            st.write("Team 1")
            st.write("1")

            st.divider()

            st.subheader("⚽ Match")
            st.write("**The match played**")


            st.divider()

            st.subheader("1A")
            st.write("Team 2")
            st.write("0")



        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.subheader("2B Best Player")
                st.write("yassen mostafa")

        with col2:
            with st.container(border=True):
                st.subheader(" Best Player ")
                st.write("yassen mostafa")
        with col3:
            with st.container(border=True):
                st.subheader("1A Best Player")
                st.write("يحيي")

        with st.container(border=True):
            st.subheader("card🟨")
            st.write("no one") 

        with st.container(border=True):
            st.subheader("card🟥")
            st.write("ahmed(2B)")

        st.divider()
        st.subheader(":red-background[:red[next match]]")
        st.divider()

