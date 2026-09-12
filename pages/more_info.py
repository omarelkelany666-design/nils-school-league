import streamlit as st
import json
import os

# 1. حماية الصفحة (للمدرسين والـ Manager فقط)

if not st.session_state.get("logged_in", False) or st.session_state.get("role") not in ["teacher", "manager"]:
    st.error("🚫 غير مسموح لك بالدخول لهذه الصفحة! هذه الصفحة مخصصة للمعلمين والـ Manager فقط.")

    if st.button("العودة للصفحة الرئيسية"):
        st.switch_page("sign_in.py")

    st.stop()


st.title("🔒 لوحة تحكم المعلمين - الإدارة والاقتراحات")


# تقسيم الصفحة لتبويبين عشان التنظيم

tab1, tab2 = st.tabs([
    "📢 لوحة الإعلانات",
    "💡 صندوق اقتراحات الطلاب"
])


# --- التبويب الأول: لوحة الإعلانات والتنبيهات ---

with tab1:

    st.subheader("إضافة إعلان جديد للطلاب")

    new_announcement = st.text_input(
        "اكتب نص الإعلان أو التنبيه هنا:"
    )

    if st.button("نشر الإعلان"):

        if new_announcement.strip():

            announcements = []

            if (
                os.path.exists("announcements.json")
                and os.path.getsize("announcements.json") > 0
            ):

                try:

                    with open(
                        "announcements.json",
                        "r",
                        encoding="utf-8"
                    ) as f:

                        announcements = json.load(f)

                except json.JSONDecodeError:

                    announcements = []

            announcements.append(new_announcement)

            with open(
                "announcements.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    announcements,
                    f,
                    ensure_ascii=False
                )

            st.success(
                "تم نشر الإعلان بنجاح وسيظهر للطلاب الآن!"
            )

            st.rerun()

        else:

            st.warning(
                "من فضلك اكتب نص الإعلان أولاً."
            )


    st.divider()

    st.subheader("الإعلانات الحالية المنشورة:")

    announcements = []

    if (
        os.path.exists("announcements.json")
        and os.path.getsize("announcements.json") > 0
    ):

        try:

            with open(
                "announcements.json",
                "r",
                encoding="utf-8"
            ) as f:

                announcements = json.load(f)

        except json.JSONDecodeError:

            announcements = []


    if announcements:

        for i, ann in enumerate(
            reversed(announcements)
        ):

            st.info(
                f"إعلان #{len(announcements)-i}: {ann}"
            )

    else:

        st.write(
            "لا توجد إعلانات حالياً."
        )


# --- التبويب الثاني: صندوق اقتراحات الطلاب ---

with tab2:

    st.subheader(
        "متابعة اقتراحات وأفكار الطلاب لتطوير الموقع"
    )

    suggestions = []

    if (
        os.path.exists("suggestions.json")
        and os.path.getsize("suggestions.json") > 0
    ):

        try:

            with open(
                "suggestions.json",
                "r",
                encoding="utf-8"
            ) as f:

                suggestions = json.load(f)

        except json.JSONDecodeError:

            suggestions = []


    if suggestions:

        for i, sug in enumerate(
            reversed(suggestions)
        ):

            st.success(
                f"اقتراح #{len(suggestions)-i}: {sug}"
            )

    else:

        st.write(
            "لم يرسل الطلاب أي اقتراحات حتى الآن."
        )


# زرار تسجيل خروج في أسفل الصفحة

st.divider()

if st.button("تسجيل خروج من الحساب"):

    st.session_state.logged_in = False
    st.session_state.role = "guest"

    st.switch_page("sign_in.py")