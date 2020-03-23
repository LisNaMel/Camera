from random import randrange
import pymysql
import json

data = {
  "id": 123456,
  "password": 123256,
  "name": 'Ryujin Jakra ภูเขาไฟ',
  "status": 2,
  "camera_id": 102030,
  "time": 10.00,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(data))


def connect_db():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='a',
                          db='borrow_camera')
    return con


def insert_sql(table_name, value_json):
    sql = ""
    if table_name == 'info':
        sql = "INSERT INTO `info` (`ID`, `PASSWORD`, `NAME`, `STATUS`, `CAMERA_ID`, `TIME`) \
         VALUES ('%d', '%d', '%s', '%d', '%d', '%d')" % \
              (value_json["id"], value_json["password"], value_json["name"], value_json["status"], value_json["camera_id"],value_json["time"])
    elif table_name == 'user_info':
        sql = "INSERT INTO `user_info` (`ID`, `LAST_ACTION`, `HISTORY`, `REPORT`, `PERSONAL`) \
         VALUES ('%d', '%s', '%s', '%s', '%s')" %\
              (value_json["id"],value_json['last_action'],value_json["history"],value_json['report'],value_json["personal"])
    return sql


def update_sql(table_name, update, value_json):
    sql = ""
    if table_name == 'info':
        sql = "UPDATE info SET {update_what}={update_value} WHERE ID={id}".format(update_what=update.upper(),
                                                                                  update_value=value_json[update],
                                                                                  id=value_json["id"])
    elif table_name == 'user_info':
        sql = "UPDATE info SET {update_what}={update_value} WHERE ID={id}".format(update_what=update.upper(),
                                                                                  update_value=value_json[update],
                                                                                  id=value_json["id"])
    return sql


def delete_sql(table_name, delete, value_json):
    sql = "DELETE FROM `{table}` WHERE `{delete_what}={value}".format(table=table_name, delete_what=delete.upper()
                                                                      ,value=value_json[delete])
    return sql


def update_json(json_file, ids, key, value):
    json_obj[ids][key] = value
    file = open(json_file, "w")
    json.dump(json_obj, file)
    file.close()


def sent_password(ids):
    password = randrange(100000)
    update_json("data.json", ids, "password", password)

    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute(update_sql('info', 'password', data))
        db.commit()
    except:
        print('error')
        db.rollback()

    db.close()


def main():
    pass


if __name__ =="__main__":
    main()