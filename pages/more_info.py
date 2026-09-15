import streamlit as st

import json

import os

from supabase import create_client


# ==========================================================
# SUPABASE
# ==========================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]

SUPABASE_SERVICE_ROLE_KEY = st.secrets[
    "SUPABASE_SERVICE_ROLE_KEY"
]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)


# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ==========================================================
# JSON FILES
# ==========================================================

ANNOUNCEMENTS_FILE = os.path.join(
    PROJECT_ROOT,
    "announcements.json"
)

SUGGESTIONS_FILE = os.path.join(
    PROJECT_ROOT,
    "suggestions.json"
)


# ==========================================================
# PROTECTION
# ==========================================================

if (
    not st.session_state.get(
        "logged_in",
        False
    )
    or st.session_state.get(
        "role"
    ) not in [
        "teacher",
        "manager"
    ]
):

    st.error(
        "🚫 غير مسموح لك بالدخول لهذه الصفحة! "
        "هذه الصفحة مخصصة للمعلمين والـ Manager فقط."
    )

    if st.button(
        "العودة للصفحة الرئيسية"
    ):

        st.switch_page(
            "sign_in.py"
        )

    st.stop()


# ==========================================================
# FUNCTIONS
# ==========================================================

def load_json_file(
    file_path,
    default
):

    if not os.path.exists(
        file_path
    ):

        return default

    if os.path.getsize(
        file_path
    ) == 0:

        return default

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            return data

    except (
        json.JSONDecodeError,
        OSError
    ):

        return default


def save_json_file(
    file_path,
    data
):

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


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title(
    "🔒 لوحة تحكم المعلمين"
)


# ==========================================================
# TABS
# ==========================================================

tab1, tab2 = st.tabs(
    [
        "📢 لوحة الإعلانات",
        "💡 صندوق اقتراحات الطلاب"
    ]
)


# ==========================================================
# TAB 1
# ANNOUNCEMENTS
# ==========================================================

with tab1:

    st.subheader(
        "إضافة إعلان جديد للطلاب"
    )

    new_announcement = st.text_area(
        "اكتب نص الإعلان أو التنبيه هنا:"
    )

    if st.button(
        "📢 نشر الإعلان"
    ):

        if new_announcement.strip():

            # --------------------------------------------------
            # Get current username
            # --------------------------------------------------

            username = st.session_state.get(
                "username",
                "Teacher"
            )

            # --------------------------------------------------
            # Create announcement in Supabase
            # --------------------------------------------------

            new_data = {
                "text": new_announcement.strip(),
                "author": username
            }

            try:

                supabase.table(
                    "announcements"
                ).insert(
                    new_data
                ).execute()

                st.success(
                    "✅ تم نشر الإعلان بنجاح!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"❌ حدث خطأ أثناء حفظ الإعلان: {error}"
                )

        else:

            st.warning(
                "من فضلك اكتب نص الإعلان أولاً."
            )


    # ======================================================
    # CURRENT ANNOUNCEMENTS
    # ======================================================

    st.divider()

    st.subheader(
        "📢 الإعلانات الحالية المنشورة:"
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
            f"❌ حدث خطأ أثناء تحميل الإعلانات: {error}"
        )

        announcements = []


    if announcements:

        for i, announcement in enumerate(
            announcements
        ):

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
                    "Teacher"
                )

                st.info(
                    f"📢 {text}\n\n"
                    f"👤 بواسطة: {author}"
                )

            else:

                st.info(
                    f"📢 {announcement}"
                )

    else:

        st.write(
            "لا توجد إعلانات حالياً."
        )


# ==========================================================
# TAB 2
# SUGGESTIONS
# ==========================================================

with tab2:

    st.subheader(
        "💡 متابعة اقتراحات وأفكار الطلاب"
    )

    try:

        response = (
            supabase
            .table("suggestions")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        suggestions = response.data

    except Exception as error:

        st.error(
            f"❌ حدث خطأ أثناء تحميل الاقتراحات: {error}"
        )

        suggestions = []


    if suggestions:

        for i, suggestion in enumerate(
            suggestions
        ):

            if isinstance(
                suggestion,
                dict
            ):

                # Supabase uses username
                user = suggestion.get(
                    "username",
                    "unknown"
                )

                # Supabase uses idea
                idea = suggestion.get(
                    "idea",
                    ""
                )

                st.success(
                    f"💡 اقتراح #{len(suggestions)-i}\n\n"
                    f"👤 الطالب: {user}\n\n"
                    f"📝 الاقتراح: {idea}"
                )

            else:

                st.success(
                    str(suggestion)
                )

    else:

        st.write(
            "لم يرسل الطلاب أي اقتراحات حتى الآن."
        )


# ==========================================================
# LOGOUT
# ==========================================================

st.divider()

if st.button(
    "🚪 تسجيل خروج من الحساب"
):

    st.session_state.logged_in = False

    st.session_state.role = "guest"

    st.session_state.username = ""

    st.switch_page(
        "sign_in.py"
    )