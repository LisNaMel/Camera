from random import randrange
import pymysql
import json
import datetime

def get_data_json():
    with open('data.json', 'r', encoding="utf-8") as f:
        json_obj = json.load(f)
    return json_obj


def insert_json(place, item):
    """
    @param place: location you want to add item in. Such as in "user_id" , in "{some id}", in "{some id's personal}"
    or in "{wherever in json_obj}" by adding list of keys to this parameter example ["user_id", "2"]
    @param item: things that you want to add. However, Please be careful about the data-type.
    example code: insert_json(["user_id","2","personal"], {"university":"Fibo"})
    this will add new type of details to "2"'s personal.
    Former "2"'s personal have "age" and "sex" but now it'll have "university" with value="Fibo"
    """
    json_obj = get_data_json()
    new_json_obj=""
    if len(place) == 1:
        new_json_obj = json_obj[place[0]].append(item)
    elif len(place) == 2:
        new_json_obj = json_obj[place[0]][place[1]].append(item)
    elif len(place) == 3:
        new_json_obj = json_obj[place[0]][place[1]][place[2]].append(item)
    elif len(place) == 4:
        new_json_obj = json_obj[place[0]][place[1]][place[2]][place[3]].append(item)
    else:
        print("too much")

    file = open("data.json", "w", encoding="utf-8")
    json.dump(new_json_obj, file, indent=4)
    file.close()


def delete_json(type_user, ids):
    """
    delete entire id data
    @param type_user: "user_id" or "admin_id"
    @param ids: "1" "2"...
    @return: None
    """
    json_obj = get_data_json()
    del json_obj[type_user][ids]

    file = open("data.json", "w", encoding="utf-8")
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
    file = open("data.json", "w", encoding="utf-8")
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
    if table_name == 'app_info':
        sql = "INSERT INTO `app_info` (`ORDER_ID`, `ID`, `ACTION`, `DATETIME`, `CAMERA_ID`, `RANDOM_KEY`) \
         VALUES ('%d', '%d', '%s', '%d', '%d', '%d')" % \
              (value_json["order_id"], value_json["id"], value_json["action"], value_json["datetime"],
               value_json["camera_id"], value_json["random_key"])
    elif table_name == 'user_info':
        sql = "INSERT INTO `user_info` (`ID`, `FIRST_NAME`, `LAST_NAME`, `PASSWORD`, `TYPE_USER`, `STATUS`,`TEL`,`HISTORY) \
         VALUES ('%d', '%s', '%s', '%s', '%s', '%s, %s, %s)" %\
              (value_json["id"], value_json['first_name'], value_json["last_name"], value_json['password'], value_json["type_user"],
               value_json["status"], value_json["tel"], value_json["history"])
    elif table_name == 'camera_info':
        sql = "INSERT INTO `camera_info` (`CAMERA_ID`, `CAMERA_STATUS`, `CAMERA_DATA`) \
                 VALUES ('%d', '%s', '%s')" % \
              (value_json["camera_id"], value_json['camera_status'], value_json["camera_data"])
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
    """
    save random password to json and mysql then return password
    @param ids: id of user you want to send him password
    @return: password
    """
    password = randrange(100000, 1000000)
    update_json("data.json", ids, "status", password)
    json_obj = get_data_json()
    data = json_obj["user_id"]
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute(update_sql('user_info', 'status', data))
        db.commit()
    except pymysql.err as e:
        print(e)
        db.rollback()
        return None
    db.close()

    return password


def register_user(data):

    if not get_data_sql('user_info', "ID", int(data[0])):
        type_id = ""
        if data[0:3] == "999" and data[-4:-1] == "999":
            type_id = "admin_id"
        else:
            type_id = "user_id"
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        json_obj = {
                    "id": int(data[0]),
                    "first_name": data[1],
                    "last_name": data[2],
                    "password": data[4],
                    "type_user": type_id,
                    "status": "init",
                    "tel": data[3],
                    "history": {"=>register at " + date}
        }
        insert_json([type_id], {str(data[0]): json_obj})
        insert_sql("user_info", json_obj)



register_user(['283984','jfoe','dfieoo','028746','dfkoro'])
