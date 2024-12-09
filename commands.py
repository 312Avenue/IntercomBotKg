import sqlite3


def upsert_ticket(teleid, field, value):
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    cur.execute('INSERT INTO info (id, %s) values( "%s", "%s") ON CONFLICT (id) DO UPDATE SET id=%s, %s="%s";' % (
        field, teleid, value, teleid, field, value,))
    con.commit()


def get_ticket(teleid):
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM info where id = %s;" % (teleid,))
    result = cur.fetchone()
    return result


def reset_row(teleid):
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    cur.execute("REPLACE into info (id) VALUES(%s);" % (teleid,))
    con.commit()


def upsert_user_state(teleid, state):
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    cur.execute("INSERT INTO user_state (id, state) values( %s, %s) ON CONFLICT (id) DO UPDATE SET id=%s, state=%s;" % (
        teleid, state, teleid, state,))
    con.commit()


def get_user_state(teleid):
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    cur.execute("SELECT state FROM user_state where id = %s;" % (teleid,))
    result = cur.fetchone()
    return result


def reset_state(teleid):
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    cur.execute("REPLACE into user_state (id) VALUES(%s);" % (teleid,))
    con.commit()


def upsert_report(fields):
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    cur.execute(f'UPDATE report SET {fields} = {fields} + 1;')
    con.commit()
    

def report_about_report():
    con = sqlite3.connect("stg.db")
    cur = con.cursor()
    info = cur.execute(f'SELECT * FROM report').fetchall()
    con.commit()
    return info
