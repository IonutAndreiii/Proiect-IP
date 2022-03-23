import socket
import mysql.connector
from mysql.connector import errorcode
import msvcrt

sock = None
db_config = {
  'host':'acces-server-sql.mysql.database.azure.com',
  'user':'acces@acces-server-sql',
  'password':'Madrid10',
  'database':'acces'
}

OPEN_GATE_REQUEST = bytes('GATh', 'ascii')
OPEN_GATE_MESSAGE = bytes([0x47, 0x41, 0x54, 0x42])
GATE_OPENING_MESSAGE = bytes([0x47, 0x41, 0x54, 0x01])
GATE_OPENED_MESSAGE = bytes([0x47, 0x41, 0x54, 0x02])
GATE_CLOSING_MESSAGE = bytes([0x47, 0x41, 0x54, 0x03])
GATE_CLOSED_MESSAGE = bytes([0x47, 0x41, 0x54, 0x04])
LOGIN_OK_MESSAGE = bytes([0x47, 0x41, 0x54, 0x05])
LOGIN_WRONG_MESSAGE = bytes([0x47, 0x41, 0x54, 0x06])
PROFILE_DATA_REQUEST_MESSAGE = bytes([0x47, 0x41, 0x54, 0x07])
LOGIN_REQUEST_MESSAGE = bytes([0x47, 0x41, 0x54, 0x33])

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('192.168.1.177', 23) # telnet port
    print('Connecting to arduino at {}'.format(addr))
    sock.connect(addr)

def send_message(message):
    sock.sendall(message)

def get_message():
    msg = sock.recv(100)
    return msg

def query_db_for_uid(uid):
    try:
        conn = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT `Cod_secur`, `Nume`, `Marca`, `Nr_masina` FROM evid_angajati;")
        rows = cursor.fetchall()
        str_uid = uid.decode('ascii')
        for row in rows:
            if row[0] == str_uid:
                print('Gasit angajat {}, marca {}, numar masina {}'.format(row[1], row[2], row[3]))
                return True
        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
    print('Nu s-a gasit angajat cu cod de securitate {}'.format(str_uid))
    return False

def check_credidentials(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE `username`='{}' AND `password`='{}';".format(username, password))
        rows = cursor.fetchall()
        if len(rows) > 0:
            print('Login successful!')
            return True
        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
    print('Failed login.')
    return False

def send_profile_data_for_uid(uid):
    try:
        conn = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT `Nume`, `Divizie`, `Nr_masina`, `Orar_acces` FROM evid_angajati WHERE `Cod_secur`='{}';".format(uid))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('Nu s-au gasit detalii pentru angajatul cu codul de securitate {}'.format(uid))
        else:
            detalii = rows[0]
            print('Detalii profil: {}'.format(detalii))
            nume = detalii[0]
            divizie = detalii[1]
            nr_masina = detalii[2]
            orar_acces = detalii[3]
            msg_list = list()
            for b in "GAT":
                msg_list.append(ord(b))
            msg_list.append(0x07)
            msg_list.append(len(nume))
            for b in nume:
                msg_list.append(ord(b))
            msg_list.append(len(divizie))
            for b in divizie:
                msg_list.append(ord(b))
            msg_list.append(len(nr_masina))
            for b in nr_masina:
                msg_list.append(ord(b))
            msg_list.append(len(orar_acces))
            for b in orar_acces:
                msg_list.append(ord(b))
            message = bytes(msg_list)
            print('Sending profile details...')
            send_message(message)
        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()

def check_message_and_take_action(msg):
    if msg[:4] == OPEN_GATE_REQUEST: # G A T 0x68 + UID
        uid = msg[4:19]
        print('Got gate open request for uid UID: {}'.format(uid.decode('ascii')))
        if query_db_for_uid(uid):
            print('Gate will open')
            send_message(OPEN_GATE_MESSAGE) # G A T 0x42
    elif msg[:4] == GATE_OPENING_MESSAGE:
        print('---------------')
        print('Gate is opening...')
        print('---------------')
    elif msg[:4] == GATE_OPENED_MESSAGE:
        print('---------------')
        print('Gate is opened !')
        print('---------------')
    elif msg[:4] == GATE_CLOSING_MESSAGE:
        print('---------------')
        print('Gate is closing...')
        print('---------------')
    elif msg[:4] == GATE_CLOSED_MESSAGE:
        print('---------------')
        print('Gate is closed !')
        print('---------------')
    elif msg[:4] == LOGIN_REQUEST_MESSAGE:
        print('Got login request')
        user_len = msg[4]
        username = msg[5:5+user_len]
        pass_len = msg[5+user_len]
        password = msg[6+user_len:6+user_len+pass_len]
        if check_credidentials(username.decode('ascii'), password.decode('ascii')):
            send_message(LOGIN_OK_MESSAGE)
        else:
            send_message(LOGIN_WRONG_MESSAGE)
    elif msg[:4] == PROFILE_DATA_REQUEST_MESSAGE:
        uid = msg[4:19]
        print('Got profile data request for UID: {}'.format(uid.decode('ascii')))
        send_profile_data_for_uid(uid.decode('ascii'))
    else:
        print('Got unknown message: {}'.format(msg))

def main():
    try:
        connect()
    except Exception as e:
        print('Failed connecting to arduino\n\tException: {}'.format(e))
        return
    print('Connected, sending initial message...')
    send_message(bytes('x', 'ascii')) # initial message, so board can see we are connected
    print('Done')
    paused = False
    while 'school' is not 'cool':
        if(msvcrt.kbhit()):
            paused = not paused
            if paused:
                print(60*'-')
                print('Acces interzis! Apasati un buton pentru a relua accesul...')
                print(60*'-')
            else:
                print(15*'-')
                print('Acces permis!')
                print(15*'-')
                sock.recv(4096)# curatare buffer intrare

        if not paused:
            msg = get_message()
            if len(msg) > 0:
                check_message_and_take_action(msg)

if __name__ == '__main__':
    main()
