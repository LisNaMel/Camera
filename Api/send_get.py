from random import randrange
import pymysql
import json


def get_data_json():
    with open('data.json', 'r', encoding="utf-8") as f:
        json_obj = json.load(f)
    return json_obj


def insert_json(place, item):
    """
    @param place: location you want to add item in. Such as in "user_id" , in "{some id}", in "{some id's personal}"
    or in "{wherever in json_obj}" by adding list of keys to this parameter example ["user_id", "2"]
    @param item: things that you want to add. However, Please be careful about the data-type.
    example code: insert(["user_id","2","personal"], {"university":"Fibo"})
    this will add new type of details to "2"'s personal.
    Former "2"'s personal have "age" and "sex" but now it'll have "university" with value="Fibo"
    """
    json_obj = get_data_json()
    new_json_obj=""
    if len(place) == 1:
        new_json_obj = json_obj[place[0]].update(item)
    elif len(place) == 2:
        new_json_obj = json_obj[place[0]][place[1]].update(item)
    elif len(place) == 3:
        new_json_obj = json_obj[place[0]][place[1]][place[2]].update(item)
    elif len(place) == 4:
        new_json_obj = json_obj[place[0]][place[1]][place[2]][place[3]].update(item)
    else:
        print("too much keys")

    file = open("data.json", "w")
    json.dump(new_json_obj, file, indent=4)
    file.close()


def delete_json(type_user, ids):
    json_obj = get_data_json()
    del json_obj[type_user][ids]

    file = open("data.json", "w")
    json.dump(json_obj, file, indent=4)
    file.close()


def update_json(type_user, ids, key, value):
    """
    @param type_user: "user_id" or "admin_id"
    @param ids: id of data you want to access
    @param key: what categories you want to change
    @param value: new value
    example code: update_json("user_id", "2", "password", 2002)
    this line of code changes password of data id "2" to 2002
    """
    json_obj = get_data_json()
    json_obj[type_user][ids][key] = value
    file = open("data.json", "w")
    json.dump(json_obj, file, indent=4)
    file.close()


def connect_db():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='a',
                          db='borrow_camera')
    return con


def get_data_sql(table_name, key, value):
    db = connect_db()
    cursor = db.cursor()
    sql_select_query = "SELECT * FROM `{table}` WHERE {key} = {value}".format(table=table_name,
                                                                              key=key.upper(), value=value)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    return record


def insert_sql(table_name, value_json):
    sql = ""
    if table_name == 'info':
        sql = "INSERT INTO `info` (`ID`, `PASSWORD`, `NAME`, `STATUS`, `CAMERA_ID`, `TIME`) \
         VALUES ('%d', '%d', '%s', '%d', '%d', '%d')" % \
              (value_json["id"], value_json["password"], value_json["name"], value_json["status"], value_json["camera_id"], value_json["time"])
    elif table_name == 'user_info':
        sql = "INSERT INTO `user_info` (`ID`, `LAST_ACTION`, `HISTORY`, `REPORT`, `PERSONAL`) \
         VALUES ('%d', '%s', '%s', '%s', '%s')" %\
              (value_json["id"], value_json['last_action'], value_json["history"], value_json['report'], value_json["personal"])
    return sql


def update_sql(table_name, update, value_json):
    sql = "UPDATE {table} SET {update_what}={update_value} WHERE ID={id}".format(table=table_name,update_what=update.upper(),
                                                                                 update_value=value_json[update],
                                                                                 id=value_json["id"])
    return sql


def delete_sql(table_name, delete, value_json):
    sql = "DELETE FROM `{table}` WHERE {delete_what}={value}".format(table=table_name, delete_what=delete.upper()
                                                                      ,value=value_json[delete])
    return sql


def sent_password(ids):
    password = randrange(100000)
    update_json("data.json", ids, "password", password)
    json_obj = get_data_json()
    data = json_obj["user_id"]
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute(update_sql('info', 'password', data))
        db.commit()
    except pymysql.err as e:
        print(e)
        db.rollback()
        return None
    db.close()
