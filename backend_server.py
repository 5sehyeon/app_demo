from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import logging
import pymysql

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

AWS_RDS_INSTANCE_LOGIN = {
    'host' : 'test-database.cj40aism4clv.ap-southeast-2.rds.amazonaws.com',
    'user' : 'admin',
    'password' : 'nx12131213!',
    'port' : 3306
}

def connect_to_database(db_name):
    try:
        connection = pymysql.connect(
            host=AWS_RDS_INSTANCE_LOGIN['host'],
            user=AWS_RDS_INSTANCE_LOGIN['user'],
            password=AWS_RDS_INSTANCE_LOGIN['password'],
            port=AWS_RDS_INSTANCE_LOGIN['port'],
            database=db_name
        )
        return connection
    except Exception as e:
        return None

def insert_row_in_info_table(db_name, user_id, suppli_info_id,i):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO info
                (name, menu, cup)
                VALUES(%s, %s, %s)
                """
                VALUES = (user_id,suppli_info_id,i)
                cursor.execute(sql,VALUES)
                connection.commit()
                app.logger.info("user_profile 테이블에 row가 성공적으로 삽입되었습니다.")
        except Exception as e:
            app.logger.info(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        app.logger.info(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        

@app.route('/login_button_click', methods=['POST'])
def login_button_click():
    data = request.get_json()
    passward = data.get("password")
    
    check = 0
    answer = "nx12131213!"
    if passward == answer:
        check = 1
        app.logger.info(f"유저가 패스워드 : {passward}로 접근을 시도함")
        app.logger.info("유저가 홈화면에 들어갔다")
        return jsonify({"check" : check})
    
    else:
        check = 0
        app.logger.info(f"유저가 패스워드 : {passward}로 접근을 시도함")
        app.logger.info("유저가 비밀번호를 틀렸다")
        return jsonify({"check" : check})
    
    
@app.route('/menu_order', methods=['POST'])
def menu_order():
    data = request.get_json()
    name = data.get('name')
    menu = data.get('menu')
    cup = data.get('cup')
    app.logger.info(f"이름은 {name} 메뉴는 {menu} 수량은 {cup}")
    
    insert_row_in_info_table("app_demo",name,menu,cup)
    
    return jsonify({'name' : name})
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    