import streamlit as st
import plotly.express as px
import pandas as pd
import json
import os


# ============================================================== #
# USER ROLE
# ============================================================== #

user_role = st.session_state.get("role", "guest")

if user_role == "manager":
    st.sidebar.success("👨‍💼 Manager Mode")

elif user_role == "teacher":
    st.sidebar.info("👨‍🏫 Normal Teacher")

elif user_role == "student":
    st.sidebar.info("🎓 Student")


# ============================================================== #
# SIDEBAR
# ============================================================== #

st.sidebar.title(
    ":red[HELLO], this is :green-background[:blue[N.I.L.S]] SCHOOL LEAGE"
)

with st.sidebar:

    # ---------------------------------------------------------- #
    # Main buttons
    # ---------------------------------------------------------- #

    leage_states = st.button("leage states")
    rules = st.button("RULES")
    matches_time = st.button("matches time")
    news = st.button("NEWS")

    # ---------------------------------------------------------- #
    # 2A
    # ---------------------------------------------------------- #

    a2 = st.button("2A")

    # ---------------------------------------------------------- #
    # 2B
    # ---------------------------------------------------------- #

    b2 = st.button("2B")

    # ---------------------------------------------------------- #
    # 2C
    # ---------------------------------------------------------- #

    c2 = st.button("2C")

    # ---------------------------------------------------------- #
    # 2D
    # ---------------------------------------------------------- #

    d2 = st.button("2D")

    st.divider()

    # ========================================================== #
    # SUGGESTIONS
    # ========================================================== #

    st.subheader("💡 صندوق اقتراحات و المشاكل")

    st.write(
        "هل لديك فكرة أو اقتراح لتطوير دوري المدرسة؟ "
        "اكتبه هنا ليصل للمدرسين مباشرة:"
    )

    student_suggestion = st.text_input(
        "اكتب اقتراحك هنا..."
    )

    if st.button("إرسال الاقتراح للمدرسين"):

        if student_suggestion.strip():

            suggestions = []

            # -------------------------------------------------- #
            # Load suggestions
            # -------------------------------------------------- #

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

            # -------------------------------------------------- #
            # Username
            # -------------------------------------------------- #

            username = st.session_state.get(
                "username",
                "unknown"
            )

            # -------------------------------------------------- #
            # Add suggestion
            # -------------------------------------------------- #

            suggestions.append(
                {
                    "user": username,
                    "ideas": student_suggestion.strip()
                }
            )

            # -------------------------------------------------- #
            # Save suggestion
            # -------------------------------------------------- #

            with open(
                "suggestions.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    suggestions,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            st.success(
                "تم إرسال اقتراحك للمدرسين بنجاح! 🎉"
            )

        else:

            st.warning(
                "من فضلك اكتب اقتراحك أولاً."
            )


# ============================================================== #
# RULES
# ============================================================== #

if rules:

    st.header("RULES")

    st.write(
        """

# اللائحة الرسمية للدوري المدرسي

## 1. نظام البطولة

يتكون الدوري من 4 فرق، وكل فريق يضم 5 لاعبين.

يلعب كل فريق مع كل فريق مرتين بنظام الذهاب والإياب، بإجمالي 12 مباراة.

- الفوز: 3 نقاط.
- التعادل: نقطة واحدة.
- الخسارة: صفر نقاط.

## 2. إدارة الفرق

- لكل فريق قائد مسؤول عن إدارة الفريق والتواصل مع لجنة الدوري.
- لكل فريق نائب قائد من الطلاب يساعد القائد ويحل محله عند غيابه.
- لكل فريق كابتن من اللاعبين لقيادة الفريق داخل الملعب.
- يمكن أن يكون لكل فريق مدرب ومدرب مساعد من الطلاب (تحت الدراسة).

## 3. لجنة الدوري

- يشرف مدرسو التربية الرياضية على البطولة.
- يمكن توزيع المهام بينهم على التنظيم والانتقالات والإحصائيات والانضباط.
- بسبب وجود 4 مدرسين للتربية الرياضية، يكون حكم المباراة مدرسًا غير مسؤول عن الفريقين، ولا تكون له أي استفادة من فوز أو خسارة أي من الفريقين.
- تكون قرارات اللجنة المتعلقة بالسلامة والتنظيم ملزمة للجميع.

## 4. الميزانية وقيمة اللاعبين

يبدأ كل فريق بميزانية افتراضية قدرها 100 مليون.

### تصنيف اللاعبين

- مبتدئ: من 3 إلى 7 ملايين.
- متوسط: من 8 إلى 14 مليونًا.
- جيد: من 15 إلى 24 مليونًا.
- ممتاز: من 25 إلى 34 مليونًا.
- نجم: من 35 إلى 45 مليونًا.

**ملاحظة:** النجم هو اللاعب الذي يقود الفريق للفوز، وتكون قيمته مرتفعة للمساعدة في جعل الفرق متوازنة.

في البداية لا توجد رواتب، وهذه الفترة تستمر لمدة أسبوع، وبعدها يتم تحديد العقود.

الأموال افتراضية ولا تمثل أموالًا حقيقية.

## 5. العقود

- العقد الأساسي للاعب مدته موسم واحد.
- يمكن الاتفاق على عقد لمدة موسمين.
- يمكن أن يكون العقد قصير المدة حسب الاتفاق.
- يسجل لكل لاعب اسم اللاعب والفريق ومدة العقد والقيمة السوقية.
- لا ينتقل اللاعب المتعاقد إلا بموافقته ووفق قواعد الانتقالات.

## 6. الانتقالات

- توجد فترة انتقالات قبل بداية الموسم وفترة في منتصف الموسم.
- الحد المقترح هو صفقتان لكل فريق في كل فترة انتقالات.
- يجب تسجيل كل صفقة لدى لجنة الدوري.
- إذا انتقل لاعب متعاقد، يتفق الفريقان واللاعب على الصفقة.

## 7. الأكاديمية وتصعيد اللاعبين

- أي طالب موهوب خارج قائمة العشرين لاعبًا يمكن اعتباره لاعب أكاديمية.
- يحق لكل فريق تصعيد لاعب أو لاعبين في كل فترة انتقالات.
- الحد الأقصى لتصعيد لاعبين جدد لكل فريق خلال الموسم.
- إذا كانت قائمة الفريق مكتملة، يجب تحرير لاعب قبل تسجيل اللاعب الجديد.
- العقد الأول للاعب الأكاديمية مدته موسم واحد، وقيمته المقترحة من 1 إلى 5 ملايين.
- إذا أراد أكثر من فريق اللاعب نفسه، يمكن عمل مزاد افتراضي أو يختار اللاعب فريقه، مع تطبيق نفس القاعدة على الجميع.

## 8. المكافآت والجوائز

- يمكن منح الفريق 5 ملايين افتراضية عند الفوز.
- يمكن منح الفريق 2 مليون عند التعادل.
- يمكن منح أفضل لاعب في المباراة مليونًا افتراضيًا.
- الجوائز: أفضل لاعب، الهداف، أفضل حارس، أفضل صفقة (تحت الدراسة)، وفريق الموسم.

## 9. البطاقات والانضباط

- تطبق البطاقات حسب قواعد المباراة.
- يمكن اعتماد إيقاف مباراة بعد ثلاث بطاقات حمراء.
- يمكن أن تؤدي المخالفات إلى إيقاف مباراة على الأقل أو غرامة مالية أو سحب نقاط.
- يمنع العنف والتنمر والإهانة والسلوك غير الرياضي.

## 10. الكأس

- يمكن إقامة بطولة كأس منفصلة.
- في نظام الأربعة فرق يمكن إقامة نصف النهائي ثم النهائي.
- يمكن تسجيل أسماء الأبطال في سجل تاريخي للدوري.

## 11. الإعلام والإحصائيات

- يمكن إنشاء جروب داخلي لنشر النتائج والترتيب والهدافين والصفقات والإحصائيات.
- لا تُنشر صور أو بيانات الطلاب خارج النطاق المدرسي دون الموافقة المناسبة.

## 12. حل النزاعات

- يقدم الاعتراض قائد الفريق إلى لجنة الدوري.
- تراجع اللجنة سجل المباراة والأدلة المتاحة.
- يعلن القرار لجميع الأطراف.
- يمنع التهديد أو الشتم أو التشهير.
- إذا كان هناك ظلم تحكيمي واضح، يتم التحقيق.
- إذا تم اكتشاف رشوة، يمكن فرض غرامة تصل إلى 60 مليونًا وإيقاف منح الأموال، مع إمكانية خفض الغرامة حسب الموقف.

## 13. السلامة والروح الرياضية

- سلامة الطلاب أهم من نتيجة المباراة.
- توقف المباراة عند وجود خطر أو إصابة تحتاج إلى تدخل المشرف.
- يجب احترام جميع اللاعبين والمشرفين.

"""
    )


# ============================================================== #
# 2A
# ============================================================== #

if a2:

    st.image("2a_logo.png", width=100)

    st.header(":yellow[2A] status")
    st.subheader(":yellow[leader:] ######")
    st.subheader(":yellow[2 PREP]")
    st.caption("made by :green[omar.w.e]")

    st.subheader(":yellow[2A] chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [1, 2, 3, 4, 5, 6],
            "Match Result": [0, 0, 0, 0, 0, 0]
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

    st.image("2A_team.png", width=500)


# ============================================================== #
# 2B
# ============================================================== #

if b2:

    st.image("2a_logo.png", width=100)

    st.header(":yellow[2B] status")
    st.subheader(":yellow[leader:] ######")
    st.subheader(":yellow[2 PREP]")
    st.caption("made by :green[omar.w.e]")

    st.subheader(":yellow[2B] chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [1, 2, 3, 4, 5, 6],
            "Match Result": [0, 0, 0, 0, 0, 0]
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

    st.image("2A_team.png", width=500)


# ============================================================== #
# 2C
# ============================================================== #

if c2:

    st.image("2a_logo.png", width=100)

    st.header(":yellow[2C] status")
    st.subheader(":yellow[leader:] ######")
    st.subheader(":yellow[2 PREP]")
    st.caption("made by :green[omar.w.e]")

    st.subheader(":yellow[2C] chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [1, 2, 3, 4, 5, 6],
            "Match Result": [0, 0, 0, 0, 0, 0]
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

    st.image("2A_team.png", width=500)


# ============================================================== #
# 2D
# ============================================================== #

if d2:

    st.image(
        "download (8).jpg",
        width=100
    )

    st.header(":red[2D] status")
    st.subheader(":red[leader:] ######")
    st.subheader(":red[2 PREP]")
    st.caption("made by :green[omar.w.e]")

    st.subheader(":red[2D] chart:-")

    data = pd.DataFrame(
        {
            "Matches Played": [1, 2, 3, 4, 5, 6],
            "Match Result": [0, 0, 0, 0, 0, 0]
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
        "Haramball 😐 @fifaworldcup __@millitakimlar _ @esnetspor __#wordcup #fifaworldcup #esnetspor #millitakım #sondakika.jpg",
        width=500
    )


# ============================================================== #
# LEAGUE STATUS
# ============================================================== #

if leage_states:

    st.title(
        "WELCOME TO :green-background[:blue[N.I.L.S]] SCHOOL LEAGE"
    )

    st.caption("made by :green[omar.w.e]")

    # ---------------------------------------------------------- #
    # League Table
    # ---------------------------------------------------------- #

    teams_status = pd.DataFrame(
        {
            "Team": ["2A", "2B", "2C", "2D"],
            "Played": [0, 0, 0, 0],
            "Wins": [0, 0, 0, 0],
            "Draws": [0, 0, 0, 0],
            "Losses": [0, 0, 0, 0],
            "Points": [0, 0, 0, 0]
        }
    )

    st.header("LEAGUE TABLE")

    st.dataframe(
        teams_status,
        hide_index=True
    )

    # ---------------------------------------------------------- #
    # Best GK
    # ---------------------------------------------------------- #

    teams_best_gk = pd.DataFrame(
        {
            "GK players": [
                "2A(omar)",
                "2B()",
                "2C(saged)",
                "2C(mutasim)",
                "2D(malek)"
            ],
            "Played": [0, 0, 0, 0, 0],
            "clean sheet": [0, 0, 0, 0, 0],
            "saves": [0, 0, 0, 0, 0],
            "penalty saves": [0, 0, 0, 0, 0],
            "enterd goals": [0, 0, 0, 0, 0]
        }
    )

    st.header("LEAGUE BEST GK")

    st.dataframe(
        teams_best_gk,
        hide_index=True
    )

    # ---------------------------------------------------------- #
    # Best CB
    # ---------------------------------------------------------- #

    teams_best_cb = pd.DataFrame(
        {
            "CB players": [
                "2A(mazen)",
                "2B(mohamed)",
                "2C(adam)",
                "2C(idk)",
                "2D(all of the team)"
            ],
            "Played": [0, 0, 0, 0, 0],
            "takel": [0, 0, 0, 0, 0],
            "correct pass": [0, 0, 0, 0, 0]
        }
    )

    st.header("LEAGUE BEST CB")

    st.dataframe(
        teams_best_cb,
        hide_index=True
    )

    # ---------------------------------------------------------- #
    # Best AT
    # ---------------------------------------------------------- #

    teams_best_at = pd.DataFrame(
        {
            "AT players": [
                "2A(moaz)",
                "2a(awsam)",
                "2a(ahmed)",
                "2C(mohamed)",
                "2D(all of the team)"
            ],
            "Played": [0, 0, 0, 0, 0],
            "scored": [0, 0, 0, 0, 0],
            "assist": [0, 0, 0, 0, 0],
            "correct pass": [0, 0, 0, 0, 0]
        }
    )

    st.header("LEAGUE BEST AT")

    st.dataframe(
        teams_best_at,
        hide_index=True
    )


# ============================================================== #
# MATCHES TIME
# ============================================================== #

if matches_time:

    matches_table = pd.DataFrame(
        {
            "day": ["#", "#", "#", "#", "#"],
            "month": ["#", "#", "#", "#", "#"],
            "year": ["#", "#", "#", "#", "#"],
            "match(1)": ["#", "#", "#", "#", "#"],
            "match(2)": ["#", "#", "#", "#", "#"]
        }
    )

    st.header("LEAGUE MATCHES TIME")

    st.dataframe(
        matches_table,
        hide_index=True
    )


# ============================================================== #
# NEWS
# ============================================================== #

if news:

    st.title("NEWS")

    st.write(
        "there is no news for now"
    )