from flask import Flask, request, jsonify
import logging
import pymysql
from flask_cors import CORS

check = '0'

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

CORS(app)

"""
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
"""

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
        
def query_pay(db_name):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 금액
                FROM pay_sum
                """
                cursor.execute(sql)
                row = cursor.fetchall()
                ## 이부분을 수정
                return row[0][0]
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, query에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        

def update_pay_table(db_name,pay):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"""
                UPDATE pay_sum
                SET 금액 = %s
                where id = 1
                """
                cursor.execute(sql,(pay,))
                connection.commit()
                print("pay_sum 테이블에 row가 성공적으로 삽입되었습니다.")
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        
def update_main_table(db_name,gift,name):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"""
                UPDATE main
                SET 남은선물 = %s
                where 이름 = %s
                """
                cursor.execute(sql,(gift,name,))
                connection.commit()
                print("main 테이블에 row가 성공적으로 삽입되었습니다.")
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        
def update_main_table_2(db_name,most,name):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"""
                UPDATE main
                SET 내야할 = 내야할 + %s
                where 이름 = %s
                """
                cursor.execute(sql,(most,name,))
                connection.commit()
                print("main 테이블에 row가 성공적으로 삽입되었습니다.")
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        

def insert_jumoon_log_table(db_name,log):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO jumoon_log
                (기록)
                VALUES(%s)
                """
                VALUES = (log)
                cursor.execute(sql,VALUES)
                connection.commit()
                print("user_login 테이블에 row가 성공적으로 삽입되었습니다.")
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        
        
        
def query_log(db_name):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 기록 FROM jumoon_log
                """
                cursor.execute(sql)
                row = cursor.fetchall()
                c = []
                for i in row:
                    c.append(i[0])
                    
                return c
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        
        

def update_ok(db_name,state):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"""
                UPDATE jumoon_log
                SET 상태 = '완료'
                where 기록 = %s
                """
                cursor.execute(sql,(state,))
                connection.commit()
                print("jumoon_log 테이블에 state가 성공적으로 삽입되었습니다.")
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        

def update_no(db_name,state):
    connection = connect_to_database(db_name)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"""
                UPDATE jumoon_log
                SET 상태 = '거절'
                where 기록 = %s
                """
                cursor.execute(sql,(state,))
                connection.commit()
                print("jumoon_log 테이블에 state가 성공적으로 삽입되었습니다.")
        except Exception as e:
            print(f'{e} 이러한 오류 때문에, row 삽입에 실패하였습니다.')
        finally:
            connection.close()
    else:
        print(f"{db_name} 데이터 베이스 연결에 실패하였습니다.")
        
        
        
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



@app.route('/finall', methods=['POST'])
def finall():
    data = request.get_json()
    name = data.get('name')
    gift = query_info("gcc_공감",name)
    return jsonify({"gift" : gift})

@app.route('/pay', methods=['POST'])
def pay():
    pay = query_pay("gcc_공감")
    return jsonify({"pay" : pay})

@app.route('/pay_to_db',methods=['POST'])
def pay_to_db():
    data = request.get_json()
    pay_data = data.get('pay')
    update_pay_table("gcc_공감",pay_data)
    return jsonify({"pay" : pay_data})
    
@app.route('/gift_to_db',methods=['POST'])
def gift_to_db():
    data = request.get_json()
    gift = data.get('gift')
    name = data.get('name')
    update_main_table("gcc_공감",gift,name)
    return jsonify({"name" : name})

@app.route('/most_to_db',methods=['POST'])
def most_to_db():
    data = request.get_json()
    most = data.get('most')
    name = data.get('name')
    update_main_table_2("gcc_공감",most,name)
    return jsonify({"name" : name})

@app.route('/log_to_db',methods=['POST'])
def log_to_db():
    data = request.get_json()
    log = data.get('log')
    insert_jumoon_log_table('gcc_공감',log)
    return jsonify({"name" : log})

@app.route('/log', methods=['POST'])
def log():
    log = query_log("gcc_공감")
    return jsonify({"log" : log})

@app.route('/temp', methods=['POST'])
def temp():
    global check
    data = request.get_json()
    jumoon = data.get('jumoon')
    check = jumoon
    print(check)
    return jsonify({"jumoon" : jumoon})

@app.route('/to_B', methods=['GET'])
def to_B():
    return jsonify(check)

@app.route('/reset', methods=['POST'])
def reset():
    global check
    data = request.get_json()
    reset = data.get('reset')
    check = '0'
    print(check)
    return jsonify({'reset' : reset})
    
@app.route('/ok', methods=['POST'])
def ok():
    data = request.get_json()
    state = data.get('state')
    update_ok('gcc_공감',state)
    return jsonify({'reset' : state})
    
    
@app.route('/no', methods=['POST'])
def no():
    data = request.get_json()
    state = data.get('state')
    update_no('gcc_공감',state)
    return jsonify({'reset' : state})


"""
@socketio.on('message_from_A')
def handle_message_from_a(data):
    print(f"Received data: {data}")
    if data:
        print("Data received successfully")
    else:
        print("No data received")
    emit('message_to_B', data, broadcast=True)
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)