import streamlit as st
import json
import os

from streamlit_cookies_manager import EncryptedCookieManager
from supabase import create_client


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="N.I.L.S League",
    page_icon="⚽"
)


# --------------------------------------------------
# Supabase
# --------------------------------------------------

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
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
# Backup / Migration
# --------------------------------------------------

ACCOUNTS_FILE = "accounts.json"


def load_json_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return {}

    try:
        with open(
            ACCOUNTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_json_accounts(accounts):
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
# Supabase Account Functions
# --------------------------------------------------

def get_account(username):
    try:
        response = (
            supabase
            .table("accounts")
            .select("username, password, role")
            .eq("username", username)
            .execute()
        )

        if response.data:
            return response.data[0]

        return None

    except Exception as error:
        st.error(f"Database error: {error}")
        return None


def create_account(username, password, role):
    try:
        response = (
            supabase
            .table("accounts")
            .insert({
                "username": username,
                "password": password,
                "role": role
            })
            .execute()
        )

        st.success("Database insert successful!")
        return True

    except Exception as error:
        st.error(f"Database insert failed: {error}")
        return False


def migrate_json_accounts_to_supabase():
    """
    Copies old accounts.json accounts to Supabase
    without deleting anything from accounts.json.
    """

    json_accounts = load_json_accounts()

    if not json_accounts:
        return

    for username, account in json_accounts.items():

        existing = get_account(username)

        if existing is None:

            create_account(
                username,
                account["password"],
                account["role"]
            )


# --------------------------------------------------
# Migrate Old Accounts
# --------------------------------------------------

if "accounts_migrated" not in st.session_state:

    try:
        migrate_json_accounts_to_supabase()
    except Exception:
        pass

    st.session_state.accounts_migrated = True


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = "guest"

if "username" not in st.session_state:
    st.session_state.username = ""

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

        account = get_account(saved_username)

        if account:

            st.session_state.logged_in = True

            st.session_state.username = saved_username

            st.session_state.role = account["role"]


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

        st.subheader(
            "dont enter your :red[*gmail*] "
            "or your :red[*personal information*] "
            "only your :green[*name*] "
            "and :green[choose your *password*]"
        )

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

                username = name.strip()

                # --------------------------------------------------
                # Check Account In Supabase
                # --------------------------------------------------

                existing_account = get_account(username)

                if existing_account:

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


                    # --------------------------------------------------
                    # Save Account To Supabase
                    # --------------------------------------------------

                    account_created = create_account(
                        username,
                        password,
                        saved_role
                    )


                    if account_created:

                        # Also save locally as backup
                        accounts = load_json_accounts()

                        accounts[username] = {
                            "password": password,
                            "role": saved_role
                        }

                        save_json_accounts(accounts)


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

            username = name.strip()


            if not username:

                st.error(
                    "Name cannot be empty."
                )

            elif not password:

                st.error(
                    "Password cannot be empty."
                )

            else:

                # --------------------------------------------------
                # Get Account From Supabase
                # --------------------------------------------------

                account = get_account(username)


                if not account:

                    st.error(
                        "Account not found."
                    )

                elif account["password"] != password:

                    st.error(
                        "Wrong password."
                    )

                else:

                    # --------------------------------------------------
                    # Session Login
                    # --------------------------------------------------

                    st.session_state.logged_in = True

                    st.session_state.role = (
                        account["role"]
                    )

                    st.session_state.username = username

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

        st.session_state.skip_cookie_restore = True


        # --------------------------------------------------
        # Delete Persistent Login
        # --------------------------------------------------

        cookies["username"] = ""

        cookies.save()

        st.rerun()