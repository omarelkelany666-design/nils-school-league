
import tomllib
from pathlib import Path
from supabase import create_client

# قراءة بيانات الاتصال من أسرار المشروع
secrets_path = Path(".streamlit/secrets.toml")

with secrets_path.open("rb") as file:
    secrets = tomllib.load(file)

supabase = create_client(
    secrets["SUPABASE_URL"],
    secrets["SUPABASE_SERVICE_ROLE_KEY"]
)

# 1) جدول ترتيب الفرق
teams = [
    {"team_name": "2D", "played": 2, "wins": 1, "draws": 1, "losses": 0, "points": 4, "rank": 1},
    {"team_name": "2B", "played": 2, "wins": 1, "draws": 1, "losses": 0, "points": 4, "rank": 2},
    {"team_name": "1A", "played": 2, "wins": 1, "draws": 1, "losses": 0, "points": 4, "rank": 3},
    {"team_name": "1B", "played": 2, "wins": 1, "draws": 1, "losses": 0, "points": 4, "rank": 4},
    {"team_name": "2A", "played": 2, "wins": 1, "draws": 0, "losses": 1, "points": 3, "rank": 5},
    {"team_name": "2C", "played": 2, "wins": 1, "draws": 0, "losses": 1, "points": 3, "rank": 6},
    {"team_name": "1D", "played": 2, "wins": 0, "draws": 1, "losses": 1, "points": 1, "rank": 7},
    {"team_name": "1C", "played": 2, "wins": 0, "draws": 1, "losses": 1, "points": 1, "rank": 8},
]

# 2) جدول الهدافين والمهاجمين
attackers = [
    {"team": "2C", "name": "adam aref", "played": 2, "goals": 1, "assists": 1, "rank": 1},
    {"team": "2C", "name": "mohamed", "played": 2, "goals": 1, "assists": 1, "rank": 2},
    {"team": "1A", "name": "yehia", "played": 2, "goals": 1, "assists": 1, "rank": 3},
    {"team": "1A", "name": "rayan", "played": 2, "goals": 1, "assists": 1, "rank": 4},
    {"team": "2B", "name": "mostafa", "played": 2, "goals": 1, "assists": 0, "rank": 5},
    {"team": "1C", "name": "malek badran", "played": 2, "goals": 1, "assists": 0, "rank": 6},
    {"team": "2D", "name": "yossef", "played": 2, "goals": 1, "assists": 0, "rank": 7},
    {"team": "1A", "name": "اسر عبد العليم", "played": 2, "goals": 1, "assists": 1, "rank": 8},
    {"team": "1D", "name": "محمد خالد", "played": 2, "goals": 0, "assists": 1, "rank": 9},
    {"team": "2A", "name": "moaz", "played": 2, "goals": 0, "assists": 0, "rank": 10},
    {"team": "2A", "name": "awsam", "played": 2, "goals": 0, "assists": 0, "rank": 11},
    {"team": "2A", "name": "ahmed", "played": 2, "goals": 0, "assists": 0, "rank": 12},
    {"team": "2B", "name": "ma3rof", "played": 2, "goals": 0, "assists": 0, "rank": 13},
    {"team": "2B", "name": "shaf3e", "played": 2, "goals": 0, "assists": 0, "rank": 14},
    {"team": "2C", "name": "abed elazez", "played": 2, "goals": 0, "assists": 0, "rank": 15},
    {"team": "2D", "name": "hassan", "played": 2, "goals": 0, "assists": 0, "rank": 16},
    {"team": "1C", "name": "omar hany", "played": 2, "goals": 0, "assists": 0, "rank": 17},
    {"team": "1C", "name": "adham sherif", "played": 2, "goals": 0, "assists": 0, "rank": 18},
    {"team": "1C", "name": "mostafa mohamed", "played": 2, "goals": 0, "assists": 0, "rank": 19},
    {"team": "1B", "name": "عمر جلال", "played": 2, "goals": 0, "assists": 0, "rank": 20},
    {"team": "1B", "name": "مالك فكري", "played": 2, "goals": 0, "assists": 0, "rank": 21},
]

# 3) جدول حراس المرمى
goalkeepers = [
    {"team": "2C", "name": "mutasim", "played": 2, "clean_sheet": 1, "penalty_saves": 0, "goals_conceded": 0, "rate": 8.5, "rank": 1},
    {"team": "2D", "name": "malek", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 1, "rate": 7.0, "rank": 2},
    {"team": "2A", "name": "omar", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 1, "rate": 5.0, "rank": 3},
    {"team": "2B", "name": "asser", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 1, "rate": 7.0, "rank": 4},
    {"team": "1C", "name": "yassin youssife", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 1, "rate": 6.5, "rank": 5},
    {"team": "1A", "name": "hamza mahmoud", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 1, "rate": 6.5, "rank": 6},
    {"team": "1D", "name": "ahmed mohamed", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 2, "rate": 6.5, "rank": 7},
    {"team": "1B", "name": "moaz mohamed", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 3, "rate": 4.5, "rank": 8},
    {"team": "2C", "name": "saged", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 0, "rate": 0.0, "rank": 9},
    {"team": "2B", "name": "baraa", "played": 2, "clean_sheet": 0, "penalty_saves": 0, "goals_conceded": 0, "rate": 0.0, "rank": 10},
]

# لا نضيف بيانات مكررة إذا كان الجدول يحتوي على بيانات بالفعل
def migrate(table_name, rows):
    existing = (
        supabase.table(table_name)
        .select("id")
        .limit(1)
        .execute()
    )

    if existing.data:
        print(f"SKIPPED {table_name}: الجدول يحتوي على بيانات بالفعل.")
        return

    supabase.table(table_name).insert(rows).execute()
    print(f"SUCCESS {table_name}: تم نقل {len(rows)} سجلًا.")

migrate("teams", teams)
migrate("attackers", attackers)
migrate("goalkeepers", goalkeepers)

print("انتهى نقل البيانات.")
