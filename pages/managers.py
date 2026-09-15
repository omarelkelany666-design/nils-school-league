import streamlit as st
import json
import os


# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ==========================================================
# MANAGER CHAT FILE
# ==========================================================

CHAT_FILE = os.path.join(
    PROJECT_ROOT,
    "manager_chat.json"
)


# ==========================================================
# MANAGER CHAT PROTECTION
# ==========================================================

if (
    not st.session_state.get(
        "logged_in",
        False
    )

    or st.session_state.get(
        "role"
    ) != "manager"
):

    st.error(
        "🚫 هذه الصفحة مخصصة للـ Managers فقط."
    )

    if st.button(
        "العودة للصفحة الرئيسية"
    ):

        st.switch_page(
            "sign_in.py"
        )

    st.stop()


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title(
    "👨‍💼 Manager Chat"
)


# ==========================================================
# FUNCTIONS
# ==========================================================

def load_messages():

    if not os.path.exists(
        CHAT_FILE
    ):

        return []


    if os.path.getsize(
        CHAT_FILE
    ) == 0:

        return []


    try:

        with open(
            CHAT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_messages(messages):

    with open(
        CHAT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            messages,
            file,
            ensure_ascii=False,
            indent=4
        )


# ==========================================================
# LOAD CHAT
# ==========================================================

messages = load_messages()


# ==========================================================
# DISPLAY MESSAGES
# ==========================================================

if messages:

    for message in messages:

        name = message.get(
            "name",
            "Unknown"
        )

        text = message.get(
            "text",
            ""
        )

        st.write(
            f"**{name}:** {text}"
        )

else:

    st.info(
        "لا توجد رسائل حتى الآن."
    )


# ==========================================================
# SEND MESSAGE
# ==========================================================

st.divider()


message = st.text_input(
    "اكتب رسالتك..."
)


if st.button(
    "إرسال"
):

    if message.strip():

        new_message = {
            "name": st.session_state.get(
                "username",
                "Manager"
            ),

            "text": message.strip()
        }


        messages.append(
            new_message
        )


        save_messages(
            messages
        )


        st.success(
            "تم إرسال الرسالة."
        )

        st.rerun()

    else:

        st.warning(
            "اكتب رسالة أولاً."
        )