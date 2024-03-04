import mysql.connector
import json

with open("config.json", "r") as file:
    database_config = json.load(file)["database"]

conn = mysql.connector.connect(
    host=database_config["db_host"],
    user=database_config["db_user"],
    password=database_config["db_password"],
    database=database_config["db_name"]
)

db = conn.cursor(buffered=True)

db.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
        id TEXT,
        alts TEXT,
        won_tournaments TEXT,
        won_games INT,
        lost_games INT
    );
    """
)

db.execute(
    """
    CREATE TABLE IF NOT EXISTS tournaments(
        id INT NOT NULL,
        name TEXT,
        link TEXT,
        date TEXT,
        players INT,
        winner TEXT,
        second TEXT,
        third TEXT
    );
    """
)

conn.commit()


async def register_user(user_id: str) -> tuple:
    db.execute(
        "INSERT INTO users VALUES(%s, %s, %s, %s, %s);",
        (user_id, "", "", 0, 0)
    )
    conn.commit()

    db.execute(
        "SELECT * FROM users WHERE id = %s;",
        (user_id,)
    )

    return db.fetchone()


async def get_user(user_id: str) -> tuple:
    db.execute(
        "SELECT * FROM users WHERE id = %s;",
        (user_id,)
    )
    search = db.fetchone()

    if search:
        return search
    else:
        return await register_user(user_id)


async def update_user_score(user_id: str, won: int, lost: int) -> None:
    user_data = await get_user(user_id)

    total_wins = user_data[3] + won
    total_loss = user_data[4] + lost

    db.execute(
        "UPDATE users SET won_games = %s, lost_games = %s WHERE id = %s;",
        (total_wins, total_loss, user_id)
    )
    conn.commit()


# { winner: { playerDiscordID: id, score: score }, loser: { playerDiscordID: id, score: score } }
async def match_results(scores: dict) -> None:
    winner = scores["winner"]
    loser = scores["loser"]

    await update_user_score(winner["playerDiscordID"], winner["score"], loser["score"])
    await update_user_score(loser["playerDiscordID"], loser["score"], winner["score"])


async def add_alt(user_id: str, alt_name: str) -> str or None:
    if not (alt_name.isascii() and len(alt_name) <= 40):
        return "InvalidName"

    user_data = await get_user(user_id)
    acc_list = user_data[1].split("#")

    if len(acc_list) > 40:
        return "AltsListLimit"
    elif alt_name.lower() in map(lambda name: name.lower(), acc_list):
        return "AlreadyInDB"

    acc_list.append(alt_name)
    db.execute(
        "UPDATE users SET alts = %s WHERE id = %s;",
        ("#".join(acc_list), user_id)
    )
    conn.commit()


async def remove_alt(user_id: str, alt_name: str) -> bool:
    user_data = await get_user(user_id)
    acc_list = user_data[1].split("#")
    lower_acc_list = list(map(lambda name: name.lower(), acc_list))

    if alt_name.lower() in lower_acc_list:
        acc_list.pop(lower_acc_list.index(alt_name.lower()))
    else:
        return False

    db.execute(
        "UPDATE users SET alts = %s WHERE id = %s;",
        ("#".join(acc_list), user_id)
    )
    conn.commit()

    return True


async def get_tournaments() -> bool or list:
    db.execute(
        "SELECT * FROM tournaments"
    )
    return db.fetchall()


async def insert_tournament(name: str, link: str, date: str, players: int, winner: str, second: str, third: str) -> bool:
    if not (name.isascii() and link.isascii() and date.isascii() and winner.isascii()):
        return False

    db.execute(
        "INSERT INTO tournaments VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
        (None, name, link, date, players, winner, second, third)
    )
    conn.commit()

    return True
