from openai import OpenAI
import mysql.connector
from mysql.connector import Error
import os
import platform
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.environ['DB_NAME']
DB_PASS = os.environ['DB_PASS']
DB_PORT = os.environ['DB_PORT']
DB_PREFIX = os.environ['DB_PREFIX']
DB_USER = os.environ['DB_USER']
HOST_NAME = os.environ['HOST_NAME']
DB_SOCKET = os.environ['DB_SOCKET']
OPERATING_SYSTEM = platform.system()
chatgpt_api_key = os.environ['CHATGPT_API']

cur_dir = os.path.dirname(__file__)

def create_db_connection(host_name, user_name, user_password, port, db_name):
    global connection
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=port,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_mac_db_connection(host_name, user_name, user_password, socket, db_name):
    global connection
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            unix_socket=socket,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")


def ram_kit_fixer():

    data = []
    if OPERATING_SYSTEM == 'Darwin':
        connection = create_mac_db_connection(HOST_NAME,DB_USER,DB_PASS,DB_SOCKET,DB_NAME)
    else:
        connection = create_db_connection(HOST_NAME,DB_USER,DB_PASS,DB_PORT,DB_NAME)
    query_get_ids = f"""
    SELECT post_id FROM {DB_PREFIX}postmeta WHERE meta_key = 'ram_kit' AND meta_value = 'SINGLE' OR meta_value = 'KIT'
    """
    ids = read_query(connection, query_get_ids)

    for id_num in ids:
        query_get_name = f"""
        SELECT meta_value FROM {DB_PREFIX}postmeta WHERE meta_key = 'ram_name' AND post_id = {id_num[0]}
        """

        query_get_url = f"""
        SELECT meta_value FROM {DB_PREFIX}postmeta WHERE meta_key = 'ram_url' AND post_id = {id_num[0]}
        """

        name = read_query(connection, query_get_name)
        url = read_query(connection, query_get_url)

        RAM_PROMPT = """
        YOU ARE GIVEN THE NAME OF THE RAM AND THE LINK IN CSV FORMAT.

        YOU ARE TO RETURN THE FOLLOWING DATA IN CSV FORMAT IN THE FOLLOWING ORDER:
        <KIT>

        KIT MUST BE IN THE FORMAT <AMOUNT_OF_STICKS>X<STICK_CAPACITY> EG 2X8GB
        ONLY RETURN THE FORMATTED DATA AND NOTHING ELSE.
        """
        client = OpenAI(api_key=chatgpt_api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": f"{RAM_PROMPT}"}, {"role": "user", "content": f"{name[0][0]},{url[0][0]}"}]
            )
        
        ram_data = response.choices[0].message.content
        ram_data = ram_data.upper().strip()
        print(ram_data)
        data.append({'id':id_num[0], 'name':name[0][0], 'url':url[0][0], 'kit':ram_data})

    with open(f'{cur_dir}/ram_kit_data.csv', 'w') as f:
        for item in data:
            f.write(f"{item['id']},{item['name']},{item['url']},{item['kit']}\n")


def check_gpt_output():
    with open(f'{cur_dir}/ram_kit_data.csv', 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.strip()
            id_num, name, url, kit = line.split(',')
            os.system('cls' if os.name == 'nt' else 'clear')
            print('')
            print(name)
            print('----------------')
            print(url)
            print('----------------')
            print(kit)
            print('')
            is_correct = input("Is the data correct? (y/n): ")

            if is_correct == 'y':
                with open(f'{cur_dir}/gpt_ram_kit_data.csv', 'a') as f:
                    f.write(f"{id_num},{kit}\n")
            else:
                new_kit = input("Enter the correct kit: ")
                with open(f'{cur_dir}/gpt_ram_kit_data.csv', 'a') as f:
                    f.write(f"{id_num},{new_kit}\n")

def apply_gpt_output():
    if OPERATING_SYSTEM == 'Darwin':
        connection = create_mac_db_connection(HOST_NAME,DB_USER,DB_PASS,DB_SOCKET,DB_NAME)
    else:
        connection = create_db_connection(HOST_NAME,DB_USER,DB_PASS,DB_PORT,DB_NAME)

    with open(f'{cur_dir}/gpt_ram_kit_data.csv', 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.strip()
            id_num, kit = line.split(',')
            query = f"""
            UPDATE {DB_PREFIX}postmeta SET meta_value = '{kit}' WHERE post_id = {id_num} AND meta_key = 'ram_kit'
            """
            execute_query(connection, query)

if __name__ == "__main__":
    #ram_kit_fixer()

    #check_gpt_output()

    apply_gpt_output()