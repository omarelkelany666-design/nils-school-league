import streamlit as st
import json
import os
from streamlit_cookies_manager import EncryptedCookieManager

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="N.I.L.S League",
    page_icon="⚽"
)

# --------------------------------------------------
# Persistent Login Cookie
# --------------------------------------------------

cookies = EncryptedCookieManager(
    prefix="nils_league/",
    password=os.environ.get(
        "COOKIES_PASSWORD",
        "NILS-League-Change-This-Secret-2026"
    )
)

if not cookies.ready():
    st.stop()

# --------------------------------------------------
# Accounts JSON File
# --------------------------------------------------

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return {}

    with open(
        ACCOUNTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_accounts(accounts):
    with open(
        ACCOUNTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            accounts,
            file,
            indent=4,
            ensure_ascii=False
        )

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = "guest"

if "username" not in st.session_state:
    st.session_state.username = ""

# NEW: Prevent old cookie from logging in again after Sign Out
if "skip_cookie_restore" not in st.session_state:
    st.session_state.skip_cookie_restore = False

# --------------------------------------------------
# Restore Login From Cookie
# --------------------------------------------------

if (
    not st.session_state.logged_in
    and not st.session_state.skip_cookie_restore
):
    saved_username = cookies.get("username")

    if saved_username:
        accounts = load_accounts()

        if saved_username in accounts:
            st.session_state.logged_in = True
            st.session_state.username = saved_username
            st.session_state.role = (
                accounts[saved_username]["role"]
            )

# --------------------------------------------------
# Teacher Passwords From Streamlit Secrets
# --------------------------------------------------

NORMAL_TEACHER_PASSWORD = st.secrets[
    "NORMAL_TEACHER_PASSWORD"
]

MANAGER_PASSWORD = st.secrets[
    "MANAGER_PASSWORD"
]

# --------------------------------------------------
# Pages
# --------------------------------------------------

main_page = st.Page(
    "pages/the_main_menu.py",
    title="القائمة الرئيسية",
    icon="🏠"
)

more_info_page = st.Page(
    "pages/more_info.py",
    title="المزيد من المعلومات",
    icon="🔒"
)

manager_page = st.Page(
    "pages/managers.py",
    title="Manager",
    icon="👨‍💼"
)

# --------------------------------------------------
# LOGIN SCREEN
# --------------------------------------------------

if not st.session_state.logged_in:

    # --------------------------------------------------
    # Hide Sidebar
    # --------------------------------------------------

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("⚽ N.I.L.S League")

    login_type = st.radio(
        "Choose:",
        ["Sign In", "Sign Up"],
        horizontal=True
    )

    # ==================================================
    # SIGN UP
    # ==================================================

    if login_type == "Sign Up":

        st.header("Create an account")
        st.subheader("dont enter your :red[-gmail-]or :red[your **personal information**]only your name and choose your password")

        name = st.text_input("Name")

        password = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Who are you?",
            ["student", "teacher"],
            index=None
        )

        teacher_type = None
        teacher_password = ""

        # --------------------------------------------------
        # Teacher Type
        # --------------------------------------------------

        if role == "teacher":

            teacher_type = st.selectbox(
                "Teacher type",
                ["Normal Teacher", "Manager"],
                index=None
            )

            teacher_password = st.text_input(
                "Teacher Verification Password",
                type="password"
            )

        # --------------------------------------------------
        # SIGN UP BUTTON
        # --------------------------------------------------

        if st.button("Sign Up"):

            if not name.strip():

                st.error(
                    "Name cannot be empty."
                )

            elif not password:

                st.error(
                    "Password cannot be empty."
                )

            elif role is None:

                st.error(
                    "Please choose your role."
                )

            elif (
                role == "teacher"
                and teacher_type is None
            ):

                st.error(
                    "Please choose your teacher type."
                )

            elif (
                role == "teacher"
                and not teacher_password
            ):

                st.error(
                    "Teacher verification password cannot be empty."
                )

            elif (
                role == "teacher"
                and teacher_type == "Normal Teacher"
                and teacher_password != NORMAL_TEACHER_PASSWORD
            ):

                st.error(
                    "Wrong Normal Teacher password."
                )

            elif (
                role == "teacher"
                and teacher_type == "Manager"
                and teacher_password != MANAGER_PASSWORD
            ):

                st.error(
                    "Wrong Manager password."
                )

            else:

                accounts = load_accounts()

                if name.strip() in accounts:

                    st.error(
                        "This name is already registered."
                    )

                else:

                    if role == "student":

                        saved_role = "student"

                    elif teacher_type == "Manager":

                        saved_role = "manager"

                    else:

                        saved_role = "teacher"

                    accounts[name.strip()] = {
                        "password": password,
                        "role": saved_role
                    }

                    save_accounts(accounts)

                    st.success(
                        "Account created successfully!"
                    )

                    st.info(
                        "Your account has been saved. "
                        "You can now Sign In."
                    )

    # ==================================================
    # SIGN IN
    # ==================================================

    elif login_type == "Sign In":

        st.header("Sign in")

        name = st.text_input("Name")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Sign In"):

            accounts = load_accounts()

            if not name.strip():

                st.error(
                    "Name cannot be empty."
                )

            elif not password:

                st.error(
                    "Password cannot be empty."
                )

            elif name.strip() not in accounts:

                st.error(
                    "Account not found."
                )

            elif (
                accounts[name.strip()]["password"]
                != password
            ):

                st.error(
                    "Wrong password."
                )

            else:

                username = name.strip()

                # --------------------------------------------------
                # Session Login
                # --------------------------------------------------

                st.session_state.logged_in = True

                st.session_state.role = (
                    accounts[username]["role"]
                )

                st.session_state.username = username

                # Allow cookie restore again after login
                st.session_state.skip_cookie_restore = False

                # --------------------------------------------------
                # Save Persistent Login
                # --------------------------------------------------

                cookies["username"] = username
                cookies.save()

                st.success(
                    "Signed in successfully!"
                )

                st.rerun()

# --------------------------------------------------
# NAVIGATION AFTER LOGIN
# --------------------------------------------------

else:

    # ==================================================
    # STUDENT
    # ==================================================

    if st.session_state.role == "student":

        pg = st.navigation([
            main_page
        ])

    # ==================================================
    # NORMAL TEACHER
    # ==================================================

    elif st.session_state.role == "teacher":

        pg = st.navigation([
            main_page,
            more_info_page
        ])

    # ==================================================
    # MANAGER
    # ==================================================

    elif st.session_state.role == "manager":

        pg = st.navigation([
            main_page,
            more_info_page,
            manager_page
        ])

    # ==================================================
    # UNKNOWN ROLE
    # ==================================================

    else:

        st.error(
            "Unknown account role."
        )

        st.session_state.logged_in = False
        st.session_state.role = "guest"
        st.session_state.username = ""

        if cookies.get("username"):

            del cookies["username"]
            cookies.save()

        st.rerun()

    # --------------------------------------------------
    # Run Selected Page
    # --------------------------------------------------

    pg.run()

    # --------------------------------------------------
    # Sidebar User Information
    # --------------------------------------------------

    st.sidebar.write(
        f"👤 {st.session_state.username}"
    )

    # --------------------------------------------------
    # Role Name
    # --------------------------------------------------

    if st.session_state.role == "student":

        role_name = "Student"

    elif st.session_state.role == "teacher":

        role_name = "Normal Teacher"

    elif st.session_state.role == "manager":

        role_name = "Manager"

    else:

        role_name = "Guest"

    st.sidebar.write(
        f"Role: {role_name}"
    )

    # --------------------------------------------------
    # Role Message
    # --------------------------------------------------

    if st.session_state.role == "manager":

        st.sidebar.success(
            "👨‍💼 Manager Mode"
        )

    elif st.session_state.role == "teacher":

        st.sidebar.info(
            "👨‍🏫 Teacher Mode"
        )

    elif st.session_state.role == "student":

        st.sidebar.info(
            "🎓 Student Mode"
        )

    # --------------------------------------------------
    # Sign Out
    # --------------------------------------------------

    if st.sidebar.button("🚪 Sign Out"):

        st.session_state.logged_in = False
        st.session_state.role = "guest"
        st.session_state.username = ""

        # Prevent the old cookie from logging in again
        st.session_state.skip_cookie_restore = True

        # --------------------------------------------------
        # Delete Persistent Login
        # --------------------------------------------------

        cookies["username"] = ""
        cookies.save()

        st.rerun()