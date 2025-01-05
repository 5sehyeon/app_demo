from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import logging
import pymysql

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

AWS_RDS_INSTANCE_LOGIN = {
    'host' : 'database-1.cv2aemsqejer.ap-northeast-2.rds.amazonaws.com',
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

def query_info(db_name,name):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"""
                SELECT 남은선물
                FROM main
                WHERE 이름 = %s
                """
                cursor.execute(sql,(name,))
                row = cursor.fetchall()
                ## 이부분을 수정
                return row[0][0]
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, query에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        
def insert_row_in_eat_sum_log_table(db_name, name, sum):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO eat_sum_log
                (name, eat_sum)
                VALUES(%s, %s)
                """
                VALUES = (name,sum)
                cursor.execute(sql,VALUES)
                connection.commit()
                app.logger.info("eat_sum_log 테이블에 row가 성공적으로 삽입되었습니다.")
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
    
"""
@app.route('/menu_order', methods=['POST'])

def menu_order():
    data = request.get_json()
    name = data.get('name')
    menu = data.get('menu')
    cup = data.get('cup')
    app.logger.info(f"이름은 {name} 메뉴는 {menu} 수량은 {cup}")
    
    insert_row_in_zumoon_log_table("app_demo",name,menu,cup)
    
    return jsonify({'name' : name})
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
"""

@app.route('/menu_order', methods=['POST'])
def menu_order():
    data = request.get_json()
    name = data.get('name')
    sum = data.get('sum')
    app.logger.info(f"이름은 {name} 먹은금액은 {sum}")
    
    insert_row_in_eat_sum_log_table("app_demo",name,sum)
    
    return jsonify({'name' : name})


@app.route('/finall', methods=['POST'])
def finall():
    data = request.get_json()
    name = data.get('name')
    gift = query_info("gcc_공감",name)
    return jsonify({"gift" : gift})

    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)