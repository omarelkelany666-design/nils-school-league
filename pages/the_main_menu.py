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

        st.subheader("🎮 Moaz")
        st.write(
            "Had the game idea and created the game."
        )

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
        "there_is_no_logo.png",
        width=100
    )

    st.header("1A status")

    st.subheader("1 PREP")

    st.subheader("1A chart:-")

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

    st.image(
        "idk_team.png",
        width=500
    )

# ==============================================================
# 1B
# ==============================================================

if b1:

    st.image(
        "there_is_no_logo.png",
        width=100
    )

    st.header("1B status")

    st.subheader("1 PREP")

    st.subheader("1B chart:-")

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

    st.image(
        "idk_team.png",
        width=500
    )

# ==============================================================
# 1C
# ==============================================================

if c1:

    st.image(
        "there_is_no_logo.png",
        width=100
    )

    st.header(":yellow[1C] status")

    st.subheader(":yellow[1 PREP]")

    st.subheader(":yellow[1C] chart:-")

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

    st.image(
        "idk_team.png",
        width=500
    )

# ==============================================================
# 1D
# ==============================================================

if d1:

    st.image(
        "there_is_no_logo.png",
        width=100
    )

    st.header("1D status")

    st.subheader("1 PREP")

    st.subheader("1D chart:-")

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

    st.image(
        "idk_team.png",
        width=500
    )
    
# ==============================================================
# 2A
# ==============================================================

if a2:

    st.image(
        "2a_logo.png",
        width=100
    )

    st.header(":yellow[2A] status")

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

    st.image(
        "2c_team.png",
        width=500
    )


# ==============================================================
# 2D
# ==============================================================

if d2:

    st.image(
        "2d_logo_temporory.png",
        width=100
    )

    st.header(":gray[2D] status")

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

    st.image(
        "2d_team.png",
        width=500
    )

# ==============================================================
# LEAGUE STATUS
# ==============================================================

if main:
    prep_choose = option_menu(
        menu_title="select prep you want",
        options=["prep1", "prep2"],
        orientation="horizontal",
    )
    

    if prep_choose=="prep2":

        st.title(
            "WELCOME TO :green-background[:blue[N.I.L.S]] SCHOOL LEAGE"
        )
 




        # ----------------------------------------------------------
        # League Table
        # ----------------------------------------------------------

        teams_status = pd.DataFrame(
            {
                "Team": [
                    "2A",
                    "2B",
                    "2C",
                    "2D"
                ],

                "Played": [
                    0, 0, 0, 0
                ],

                "Wins": [
                    0, 0, 0, 0
                ],

                "Draws": [
                    0, 0, 0, 0
                ],

                "Losses": [
                    0, 0, 0, 0
                ],

                "Points": [
                    0, 0, 0, 0
                ]
            }
        )


        st.header("LEAGUE TABLE")

        st.dataframe(
            teams_status,
            hide_index=True
        )


        # ----------------------------------------------------------
        # Best GK
        # ----------------------------------------------------------

        teams_best_gk = pd.DataFrame(
            {
                "GK players": [
                    "2A(omar)",
                    "2B(baraa)",
                    "2C(saged)",
                    "2C(mutasim)",
                    "2D(malek)"
                ],

                "Played": [
                    0,
                    0,
                    0,
                    0,
                    0
                ],

                "clean sheet": [
                    0,
                    0,
                    0,
                    0,
                    0
                ],

                "saves": [
                    0,
                    0,
                    0,
                    0,
                    0
                ],

                "penalty saves": [
                    0,
                    0,
                    0,
                    0,
                    0
                ],

                "enterd goals": [
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            }
        )


        st.header("LEAGUE BEST GK")

        st.dataframe(
            teams_best_gk,
            hide_index=True
        )


        # ----------------------------------------------------------
        # Best CB
        # ----------------------------------------------------------

        teams_best_cb = pd.DataFrame(
            {
                "CB players": [
                    "2A(mazen)",
                    "2B(malek mohamed)",
                    "2C(adam aref)",
                    "2C(adam shazely)",
                    "2D(asser eslam)",
                    "2D(asser amer)"
                ],

                "Played": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],

                "takel": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
            }
        )


        st.header("LEAGUE BEST CB")

        st.dataframe(
            teams_best_cb,
            hide_index=True
        )


        # ----------------------------------------------------------
        # Best AT
        # ----------------------------------------------------------

        teams_best_at = pd.DataFrame(
            {
                "AT players": [
                    "2A(moaz)",
                    "2A(awsam)",
                    "2A(ahmed)",
                    "2B(mostafa)",
                    "2B(ma3rof)",
                    "2B(shaf3e)",
                    "2C(mohamed)",
                    "2C(abed elazez)",
                    "2D(hassen)",
                    "2D(yossef)"
                ],

                "Played": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],

                "scored": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],

                "assist": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],

            }
        )


        st.header("LEAGUE BEST AT")

        st.dataframe(
            teams_best_at,
            hide_index=True
        )
#========================================#
#prep1 choose#
#========================================#
    if prep_choose=="prep1":

        st.title(
            "WELCOME TO :green-background[:blue[N.I.L.S]] SCHOOL LEAGE"
        )




        # ----------------------------------------------------------
        # League Table
        # ----------------------------------------------------------

        teams_status = pd.DataFrame(
            {
                "Team": [
                    "1A",
                    "1B",
                    "1C",
                    "1D"
                ],

                "Played": [
                    0, 0, 0, 0
                ],

                "Wins": [
                    0, 0, 0, 0
                ],

                "Draws": [
                    0, 0, 0, 0
                ],

                "Losses": [
                    0, 0, 0, 0
                ],

                "Points": [
                    0, 0, 0, 0
                ]
            }
        )


        st.header("LEAGUE TABLE")

        st.dataframe(
            teams_status,
            hide_index=True
        )


        # ----------------------------------------------------------
        # Best GK
        # ----------------------------------------------------------

        teams_best_gk = pd.DataFrame(
            {
                "GK players": [
                    "1A()",
                    "1B()",
                    "1C()",
                    "1D()"
                ],

                "Played": [
                    0, 0, 0, 0
                ],

                "clean sheet": [
                    0, 0, 0, 0 
                ],

                "saves": [
                    0, 0, 0, 0
                ],

                "penalty saves": [
                    0, 0, 0, 0 
                ],

                "enterd goals": [
                    0, 0, 0, 0
                ]
            }
        )


        st.header("LEAGUE BEST GK")

        st.dataframe(
            teams_best_gk,
            hide_index=True
        )


        # ----------------------------------------------------------
        # Best CB
        # ----------------------------------------------------------

        teams_best_cb = pd.DataFrame(
            {
                "CB players": [
                    "1A()",
                    "1B()",
                    "1C()",
                    "1D()"
                ],

                "Played": [
                    0, 0, 0, 0
                ],

                "takel": [
                    0, 0, 0, 0
                ],

                "correct pass": [
                    0, 0, 0, 0
                ]
            }
        )


        st.header("LEAGUE BEST CB")

        st.dataframe(
            teams_best_cb,
            hide_index=True
        )


        # ----------------------------------------------------------
        # Best AT
        # ----------------------------------------------------------

        teams_best_at = pd.DataFrame(
            {
                "AT players": [
                    "1a()",
                    "1b()",
                    "1C()",
                    "1D()"
                ],

                "Played": [
                    0, 0, 0, 0
                ],

                "scored": [
                    0, 0, 0, 0
                ],

                "assist": [
                    0, 0, 0, 0
                ],

                "correct pass": [
                    0, 0, 0, 0
                ]
            }
        )


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


        st.subheader(
            "⚽ Matchs"
        )
    # ----------------------------------------------------------
    # MATCHS
    # ----------------------------------------------------------

    elif news:

        col1, col2, col3,= st.columns([3, 3, 3])

        with col1:
            with st.container(border=True):
                st.title("🟨2A")
                st.header("Team 1")
                st.subheader("—")

        with col2:
            with st.container(border=True):
                st.subheader("⚽ Match")
                st.write("**The match didn't play yet**")
                st.write("28 September 2026")

        with col3:
            with st.container(border=True):
                st.title("🟥 2C")
                st.header("Team 2")
                st.subheader("—")
        col1, col2, col3,= st.columns([2, 3, 2])

        with col1:
            with st.container(border=True):
                st.header("best player")
                st.subheader("—")

        with col2:
            with st.container(border=True):
                st.title("⚽ Match")
                st.write("🟨man of the match🟥")
                st.write("—")

        with col3:
            with st.container(border=True):
                st.header("best player")
                st.subheader("—")

        # Separator
        st.divider()

        col1, col2, col3,= st.columns([3, 3, 3])

        with col1:
            with st.container(border=True):
                st.title("🟦2B")
                st.header("Team 1")
                st.subheader("—")

        with col2:
            with st.container(border=True):
                st.subheader("⚽ Match")
                st.write("**The match didn't play yet**")
                st.write("1 october 2026")

        with col3:
            with st.container(border=True):
                st.title("⬛ 2D")
                st.header("Team 2")
                st.subheader("—")
        col1, col2, col3,= st.columns([2, 3, 2])

        with col1:
            with st.container(border=True):
                st.header("best player")
                st.subheader("—")

        with col2:
            with st.container(border=True):
                st.title("⚽ Match")
                st.write("🟦man of the match⬛")
                st.write("—")

        with col3:
            with st.container(border=True):
                st.header("best player")
                st.subheader("—")

        # Separator
        st.divider()

