import socket

sock = None

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('192.168.1.177', 23) # telnet port
    print('Connecting to arduino at {}'.format(addr))
    sock.connect(addr)

def send_message(message):
    sock.sendall(message.encode())

def get_message():
    msg = sock.recv(100)
    return msg

def query_db_for_uid():
    return True

def main():
    try:
        connect()
    except Exception as e:
        print('Failed connecting to arduino\n\tException: {}'.format(e))
        return
    print('Connected, sending initial message...')
    send_message("x") # initial message, so board can see we are connected
    print('Done')
    while 'school' is not 'cool':
        msg = get_message()
        if len(msg) > 0:
            # print('Got message: ' + msg)
            if(msg.startswith('GATh')): # G A T 0x68 + UID
                uid = msg.split('GATh')[1][:16]
                print('Got request for uid UID: ' + uid)
                if query_db_for_uid():
                    print('Valid message, opening gate')
                send_message('GATB') # G A T 0x42

if __name__ == '__main__':
    main()

