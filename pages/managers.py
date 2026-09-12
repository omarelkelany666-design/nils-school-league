import streamlit as st
import json
import os

# --------------------------------------------------
# Manager Chat Protection
# --------------------------------------------------

if (
    not st.session_state.get("logged_in", False)
    or st.session_state.get("role") != "manager"
):
    st.error("🚫 هذه الصفحة مخصصة للـ Managers فقط.")

    if st.button("العودة للصفحة الرئيسية"):
        st.switch_page("sign_in.py")

    st.stop()


# --------------------------------------------------
# Page Title
# --------------------------------------------------

st.title("👨‍💼 Manager Chat")


# --------------------------------------------------
# Chat File
# --------------------------------------------------

CHAT_FILE = "manager_chat.json"


def load_messages():

    if not os.path.exists(CHAT_FILE):
        return []

    if os.path.getsize(CHAT_FILE) == 0:
        return []

    try:

        with open(
            CHAT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError:

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


# --------------------------------------------------
# Load Chat
# --------------------------------------------------

messages = load_messages()


# --------------------------------------------------
# Display Messages
# --------------------------------------------------

if messages:

    for message in messages:

        st.write(
            f"**{message['name']}:** {message['text']}"
        )

else:

    st.info(
        "لا توجد رسائل حتى الآن."
    )


# --------------------------------------------------
# Send Message
# --------------------------------------------------

st.divider()

message = st.text_input(
    "اكتب رسالتك..."
)

if st.button("إرسال"):

    if message.strip():

        new_message = {
            "name": st.session_state.username,
            "text": message.strip()
        }

        messages.append(new_message)

        save_messages(messages)

        st.rerun()

    else:

        st.warning(
            "اكتب رسالة أولاً."
        )