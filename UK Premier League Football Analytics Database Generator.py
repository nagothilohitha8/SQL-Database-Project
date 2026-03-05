import sqlite3
import random
from datetime import datetime, timedelta

random.seed(99)

# ============================================================================
# REFERENCE DATA
# ============================================================================

FIRST_NAMES_MALE = [
    "James", "Oliver", "Jack", "Harry", "Charlie", "Thomas", "Oscar",
    "William", "George", "Leo", "Ethan", "Mason", "Logan", "Lucas",
    "Alexander", "Daniel", "Matthew", "Ryan", "Connor", "Dylan",
    "Marcus", "Jadon", "Bukayo", "Raheem", "Kalvin", "Declan",
    "Bruno", "Cristiano", "Diogo", "Bernardo", "Ruben", "Pedro",
    "Antoine", "Kylian", "Ousmane", "Karim", "Luka", "Mateo",
    "Erling", "Martin", "Sven", "Lars", "Kai", "Timo", "Leroy",
    "Sadio", "Naby", "Ibrahima", "Wilfried", "Yves", "Jean-Philippe"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Wilson",
    "Taylor", "Davies", "Evans", "Thomas", "Roberts", "Walker",
    "Wright", "Turner", "Hill", "Scott", "Green", "Adams",
    "Mitchell", "Phillips", "Campbell", "Parker", "Edwards",
    "Fernandes", "Silva", "Santos", "Costa", "Oliveira", "Pereira",
    "Rodriguez", "Martinez", "Garcia", "Lopez", "Hernandez",
    "Mueller", "Schmidt", "Weber", "Fischer", "Schneider",
    "Eriksen", "Andersen", "Hansen", "Larsen", "Pedersen",
    "Diallo", "Toure", "Kante", "Dembele", "Traore", "Camara"
]

NATIONALITIES = [
    "English", "Scottish", "Welsh", "Irish", "French", "German",
    "Spanish", "Portuguese", "Brazilian", "Argentine", "Dutch",
    "Belgian", "Italian", "Norwegian", "Danish", "Swedish",
    "Nigerian", "Ghanaian", "Senegalese", "Ivorian", "Egyptian",
    "Japanese", "South Korean", "Australian", "American", "Canadian"
]
NATIONALITY_WEIGHTS = [
    25, 5, 3, 4, 8, 5, 6, 4, 6, 4, 3, 3, 3, 3, 2, 2,
    3, 2, 2, 2, 1, 1, 1, 1, 1, 1
]

POSITIONS = ["Goalkeeper", "Centre-back", "Full-back", "Midfielder",
             "Winger", "Striker"]
POSITION_WEIGHTS = [8, 18, 14, 28, 16, 16]

# Fictional club names inspired by UK football culture
CLUBS = [
    ("Northfield United", "North West", "Northfield Park", 55000, 1878, "Red"),
    ("Eastbridge City", "London", "Eastbridge Stadium", 62000, 1886, "Blue"),
    ("Southport Wanderers", "South East", "The Valley Ground", 42000, 1892, "Green"),
    ("Westham Athletic", "London", "Olympic Arena", 60000, 1895, "Claret"),
    ("Riverside Rangers", "North East", "Riverside Stadium", 38000, 1882, "Black"),
    ("Hillcrest Town", "Midlands", "Hillcrest Park", 32000, 1901, "Yellow"),
    ("Lakeside FC", "North West", "Lakeside Arena", 48000, 1890, "White"),
    ("Stonewall City", "Yorkshire", "Stonewall Ground", 36000, 1888, "Orange"),
    ("Greenfield Rovers", "South West", "Greenfield Park", 28000, 1905, "Purple"),
    ("Ironbridge United", "Midlands", "Iron Park", 30000, 1898, "Navy"),
    ("Castlegate FC", "Scotland", "Castlegate Arena", 51000, 1872, "Royal Blue"),
    ("Thornbury Albion", "South East", "Thornbury Lane", 25000, 1910, "Sky Blue"),
    ("Ashford Dynamo", "East", "Ashford Stadium", 27000, 1903, "Amber"),
    ("Moorland FC", "North East", "Moorland Park", 33000, 1894, "Maroon"),
    ("Bridgewater Harriers", "South West", "Bridgewater Arena", 22000, 1912, "Teal"),
    ("Kingswood Palace", "London", "Palace Ground", 45000, 1885, "Crimson"),
    ("Oakfield Town", "Midlands", "Oak Park", 24000, 1908, "Silver"),
    ("Harrowgate Sporting", "Yorkshire", "Harrowgate Lane", 20000, 1915, "Lime"),
    ("Millbrook FC", "Wales", "Millbrook Stadium", 26000, 1900, "Gold"),
    ("Falconridge City", "North West", "Falcon Arena", 40000, 1880, "Burgundy")
]

VENUES = ["Home", "Away"]
MATCH_RESULTS = ["Win", "Draw", "Loss"]
GOAL_TYPES = ["Open Play", "Header", "Free Kick", "Penalty", "Own Goal",
              "Long Range", "Tap In", "Volley"]
GOAL_TYPE_WEIGHTS = [35, 12, 5, 8, 3, 7, 20, 10]

MATCH_IMPORTANCE = ["Low", "Medium", "High", "Critical"]
MATCH_IMPORTANCE_WEIGHTS = [15, 40, 30, 15]

INJURY_TYPES = [
    "Hamstring Strain", "ACL Tear", "Ankle Sprain", "Muscle Fatigue",
    "Concussion", "Knee Ligament", "Groin Strain", "Calf Injury",
    "Back Spasm", "Shoulder Dislocation", "Fracture", "Bruised Ribs"
]

INJURY_SEVERITY = ["Minor", "Moderate", "Severe", "Career-threatening"]
INJURY_SEVERITY_WEIGHTS = [40, 35, 20, 5]

SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_dob_player():
    """Generate DOB for professional footballer (age 17-38)."""
    today = datetime(2026, 2, 1)
    age_days = random.randint(17 * 365, 38 * 365)
    return (today - timedelta(days=age_days)).strftime("%Y-%m-%d")


def generate_match_date(season):
    """Generate a match date within a given season."""
    season_starts = {
        "2021-22": datetime(2021, 8, 14),
        "2022-23": datetime(2022, 8, 6),
        "2023-24": datetime(2023, 8, 12),
        "2024-25": datetime(2024, 8, 17),
        "2025-26": datetime(2025, 8, 16)
    }
    start = season_starts[season]
    end = start + timedelta(days=300)
    return (start + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d")


def generate_salary(position):
    """Generate weekly salary in GBP based on position (RATIO data)."""
    ranges = {
        "Goalkeeper": (15000, 120000),
        "Centre-back": (20000, 150000),
        "Full-back": (18000, 130000),
        "Midfielder": (25000, 200000),
        "Winger": (30000, 220000),
        "Striker": (35000, 300000)
    }
    low, high = ranges.get(position, (20000, 150000))
    return round(random.triangular(low, high, (low + high) / 3), 2)


def generate_transfer_fee(salary):
    """Generate transfer fee based on salary (higher salary = higher fee)."""
    if random.random() < 0.15:
        return 0.0  # Free transfer / academy graduate
    multiplier = random.triangular(50, 3000, 500)
    return round(salary * multiplier, 2)


def generate_height(position):
    """Generate realistic height in cm based on position (RATIO data)."""
    height_ranges = {
        "Goalkeeper": (185, 200),
        "Centre-back": (180, 196),
        "Full-back": (170, 185),
        "Midfielder": (168, 188),
        "Winger": (165, 183),
        "Striker": (172, 195)
    }
    low, high = height_ranges.get(position, (170, 190))
    return round(random.triangular(low, high, (low + high) / 2), 1)


def generate_weight(height):
    """Generate realistic weight in kg correlated to height (RATIO data)."""
    base = height * 0.4 + random.uniform(-5, 10)
    return round(max(60, min(100, base)), 1)


# ============================================================================
# DATABASE CREATION
# ============================================================================

def create_database(db_path="premier_league.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("Creating tables...")

    # TABLE: clubs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clubs (
            club_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            club_name      TEXT    NOT NULL UNIQUE,
            region         TEXT    NOT NULL,              -- NOMINAL
            stadium_name   TEXT    NOT NULL,
            stadium_capacity INTEGER NOT NULL             -- RATIO
                           CHECK(stadium_capacity > 0),
            year_founded   INTEGER NOT NULL               -- INTERVAL
                           CHECK(year_founded > 1800),
            kit_colour     TEXT    NOT NULL               -- NOMINAL
        );
    """)

    # TABLE: players (1200+ rows)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id         INTEGER NOT NULL,             -- FK
            first_name      TEXT    NOT NULL,
            last_name       TEXT    NOT NULL,
            date_of_birth   TEXT    NOT NULL,             -- INTERVAL
            nationality     TEXT    NOT NULL,             -- NOMINAL
            position        TEXT    NOT NULL              -- NOMINAL
                            CHECK(position IN ('Goalkeeper','Centre-back',
                            'Full-back','Midfielder','Winger','Striker')),
            height_cm       REAL    NOT NULL              -- RATIO
                            CHECK(height_cm > 0),
            weight_kg       REAL    NOT NULL              -- RATIO
                            CHECK(weight_kg > 0),
            salary_weekly_gbp REAL  NOT NULL              -- RATIO
                            CHECK(salary_weekly_gbp >= 0),
            transfer_fee_gbp  REAL  NOT NULL              -- RATIO
                            CHECK(transfer_fee_gbp >= 0),
            shirt_number    INTEGER NOT NULL
                            CHECK(shirt_number BETWEEN 1 AND 99),
            FOREIGN KEY (club_id) REFERENCES clubs(club_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    """)

    # TABLE: matches
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            home_club_id    INTEGER NOT NULL,             -- FK
            away_club_id    INTEGER NOT NULL,             -- FK
            match_date      TEXT    NOT NULL,             -- INTERVAL
            season          TEXT    NOT NULL,             -- NOMINAL
            venue           TEXT    NOT NULL              -- NOMINAL
                            CHECK(venue IN ('Home','Away')),
            home_goals      INTEGER NOT NULL              -- RATIO
                            CHECK(home_goals >= 0),
            away_goals      INTEGER NOT NULL              -- RATIO
                            CHECK(away_goals >= 0),
            attendance      INTEGER NOT NULL              -- RATIO
                            CHECK(attendance >= 0),
            match_importance TEXT   NOT NULL              -- ORDINAL
                            CHECK(match_importance IN 
                            ('Low','Medium','High','Critical')),
            referee_rating  INTEGER                       -- ORDINAL
                            CHECK(referee_rating BETWEEN 1 AND 10),
            FOREIGN KEY (home_club_id) REFERENCES clubs(club_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (away_club_id) REFERENCES clubs(club_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    """)

    # TABLE: goals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            goal_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id        INTEGER NOT NULL,             -- FK
            player_id       INTEGER NOT NULL,             -- FK
            minute_scored   INTEGER NOT NULL              -- RATIO
                            CHECK(minute_scored BETWEEN 1 AND 120),
            goal_type       TEXT    NOT NULL,             -- NOMINAL
            assist_player_id INTEGER,                     -- FK (nullable)
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (assist_player_id) REFERENCES players(player_id)
                ON DELETE SET NULL ON UPDATE CASCADE
        );
    """)

    # TABLE: player_injuries (COMPOUND KEY)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_injuries (
            player_id       INTEGER NOT NULL,             -- FK
            injury_date     TEXT    NOT NULL,             -- INTERVAL
            injury_type     TEXT    NOT NULL,             -- NOMINAL
            severity        TEXT    NOT NULL              -- ORDINAL
                            CHECK(severity IN ('Minor','Moderate',
                            'Severe','Career-threatening')),
            recovery_days   INTEGER NOT NULL              -- RATIO
                            CHECK(recovery_days >= 0),
            PRIMARY KEY (player_id, injury_date),         -- COMPOUND KEY
            FOREIGN KEY (player_id) REFERENCES players(player_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    """)

    # TABLE: player_ratings (per match performance)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_ratings (
            rating_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id        INTEGER NOT NULL,             -- FK
            player_id       INTEGER NOT NULL,             -- FK
            performance_rating INTEGER NOT NULL           -- ORDINAL
                            CHECK(performance_rating BETWEEN 1 AND 10),
            minutes_played  INTEGER NOT NULL              -- RATIO
                            CHECK(minutes_played BETWEEN 0 AND 120),
            distance_km     REAL    NOT NULL              -- RATIO
                            CHECK(distance_km >= 0),
            passes_completed INTEGER NOT NULL             -- RATIO
                            CHECK(passes_completed >= 0),
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    """)

    print("Inserting data...")

    # --- Insert Clubs ---
    for c in CLUBS:
        cursor.execute("""
            INSERT INTO clubs (club_name, region, stadium_name,
            stadium_capacity, year_founded, kit_colour)
            VALUES (?, ?, ?, ?, ?, ?)
        """, c)

    club_ids = list(range(1, len(CLUBS) + 1))

    # --- Insert Players (1200) ---
    num_players = 1200
    used_shirts = {}  # Track shirt numbers per club

    for i in range(num_players):
        club_id = random.choice(club_ids)
        first_name = random.choice(FIRST_NAMES_MALE)
        last_name = random.choice(LAST_NAMES)
        dob = generate_dob_player()
        nationality = random.choices(
            NATIONALITIES, weights=NATIONALITY_WEIGHTS, k=1)[0]
        position = random.choices(
            POSITIONS, weights=POSITION_WEIGHTS, k=1)[0]
        height = generate_height(position)
        weight = generate_weight(height)
        salary = generate_salary(position)
        transfer_fee = generate_transfer_fee(salary)

        if club_id not in used_shirts:
            used_shirts[club_id] = set()
        shirt = random.randint(1, 99)
        while shirt in used_shirts[club_id]:
            shirt = random.randint(1, 99)
        used_shirts[club_id].add(shirt)

        cursor.execute("""
            INSERT INTO players (club_id, first_name, last_name,
            date_of_birth, nationality, position, height_cm, weight_kg,
            salary_weekly_gbp, transfer_fee_gbp, shirt_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (club_id, first_name, last_name, dob, nationality,
              position, height, weight, salary, transfer_fee, shirt))

    player_ids = list(range(1, num_players + 1))

    # --- Insert Matches (2000) ---
    num_matches = 2000
    for i in range(num_matches):
        home_club = random.choice(club_ids)
        away_club = random.choice([c for c in club_ids if c != home_club])
        season = random.choice(SEASONS)
        match_date = generate_match_date(season)
        home_goals = random.choices(
            [0, 1, 2, 3, 4, 5, 6],
            weights=[20, 30, 25, 15, 6, 3, 1], k=1)[0]
        away_goals = random.choices(
            [0, 1, 2, 3, 4, 5, 6],
            weights=[25, 30, 22, 13, 6, 3, 1], k=1)[0]

        home_capacity = None
        for c in CLUBS:
            if club_ids[CLUBS.index(c)] == home_club:
                home_capacity = c[3]
                break
        if home_capacity is None:
            home_capacity = 30000
        attendance = random.randint(
            int(home_capacity * 0.7), home_capacity)

        importance = random.choices(
            MATCH_IMPORTANCE, weights=MATCH_IMPORTANCE_WEIGHTS, k=1)[0]
        ref_rating = random.choices(
            list(range(1, 11)),
            weights=[3, 4, 6, 8, 12, 18, 20, 15, 10, 4], k=1)[0]

        cursor.execute("""
            INSERT INTO matches (home_club_id, away_club_id, match_date,
            season, venue, home_goals, away_goals, attendance,
            match_importance, referee_rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (home_club, away_club, match_date, season, "Home",
              home_goals, away_goals, attendance, importance, ref_rating))

    match_ids = list(range(1, num_matches + 1))

    # --- Insert Goals (5000) ---
    for i in range(5000):
        match_id = random.choice(match_ids)
        player_id = random.choice(player_ids)
        minute = random.choices(
            list(range(1, 121)),
            weights=[1 + (0.3 if m > 85 else 0) for m in range(1, 121)],
            k=1)[0]
        goal_type = random.choices(
            GOAL_TYPES, weights=GOAL_TYPE_WEIGHTS, k=1)[0]
        assist = random.choice(player_ids) if random.random() < 0.7 else None

        cursor.execute("""
            INSERT INTO goals (match_id, player_id, minute_scored,
            goal_type, assist_player_id)
            VALUES (?, ?, ?, ?, ?)
        """, (match_id, player_id, minute, goal_type, assist))

    # --- Insert Player Injuries (Compound Key) ---
    injury_records = set()
    injured_players = random.sample(player_ids, k=int(num_players * 0.35))

    for pid in injured_players:
        num_injuries = random.choices([1, 2, 3, 4],
                                       weights=[45, 30, 18, 7], k=1)[0]
        for _ in range(num_injuries):
            inj_date = (datetime(2021, 8, 1) +
                        timedelta(days=random.randint(0, 1600))
                        ).strftime("%Y-%m-%d")
            if (pid, inj_date) not in injury_records:
                injury_records.add((pid, inj_date))
                inj_type = random.choice(INJURY_TYPES)
                severity = random.choices(
                    INJURY_SEVERITY,
                    weights=INJURY_SEVERITY_WEIGHTS, k=1)[0]
                recovery = {"Minor": random.randint(3, 14),
                            "Moderate": random.randint(14, 60),
                            "Severe": random.randint(60, 240),
                            "Career-threatening": random.randint(240, 540)
                            }[severity]
                cursor.execute("""
                    INSERT INTO player_injuries (player_id, injury_date,
                    injury_type, severity, recovery_days)
                    VALUES (?, ?, ?, ?, ?)
                """, (pid, inj_date, inj_type, severity, recovery))

    # --- Insert Player Ratings (6000) ---
    for i in range(6000):
        match_id = random.choice(match_ids)
        player_id = random.choice(player_ids)
        rating = random.choices(
            list(range(1, 11)),
            weights=[2, 3, 5, 8, 14, 22, 20, 14, 8, 4], k=1)[0]
        minutes = random.choices(
            [0, 15, 30, 45, 60, 75, 90],
            weights=[5, 8, 10, 12, 15, 20, 30], k=1)[0]
        distance = round(random.triangular(0, 13, 9.5), 2)
        passes = random.randint(5, 95)

        cursor.execute("""
            INSERT INTO player_ratings (match_id, player_id,
            performance_rating, minutes_played, distance_km,
            passes_completed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (match_id, player_id, rating, minutes, distance, passes))

    # --- Indexes ---
    cursor.execute("CREATE INDEX idx_players_club ON players(club_id);")
    cursor.execute("CREATE INDEX idx_matches_home ON matches(home_club_id);")
    cursor.execute("CREATE INDEX idx_matches_away ON matches(away_club_id);")
    cursor.execute("CREATE INDEX idx_goals_match ON goals(match_id);")
    cursor.execute("CREATE INDEX idx_goals_player ON goals(player_id);")
    cursor.execute("CREATE INDEX idx_ratings_match ON player_ratings(match_id);")
    cursor.execute("CREATE INDEX idx_ratings_player ON player_ratings(player_id);")

    conn.commit()

    # --- Summary ---
    print("\n" + "=" * 55)
    print("DATABASE GENERATION COMPLETE")
    print("=" * 55)
    tables = ["clubs", "players", "matches", "goals",
              "player_injuries", "player_ratings"]
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  {t:25s}: {cursor.fetchone()[0]:>6,} rows")
    print(f"\nSaved to: {db_path}")

    conn.close()
    return db_path


if __name__ == "__main__":
    create_database("premier_league.db")