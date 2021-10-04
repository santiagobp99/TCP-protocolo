
import os
import socket
import threading

#IP = socket.gethostbyname(socket.gethostname()) 
IP = socket.gethostbyname(socket.gethostname() + ".local")
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))
        
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        elif cmd == "HELP":
            data = "OK@"
            data += "LIST: List all the files from the server.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands."

            conn.send(data.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def archivos(conn):
    print("Menu de opciones")
    
    opc = int(input("(Opciones 0 y 1 )Desea transmitir un archivo: No:0 , Si:1"))
    while(opc!=0):
        if opc == 0:
            break
        elif opc == 1:
             opc = int(input("(Opciones 2 y 3 ) Que archivo desea transmitir: 100MB:2 , 250MB:3"))
        elif opc == 2:
            num = int(input("Escriba al numero de clientes que desea transmitir el archivo:"))
            enviar_archivos(2, num, conn)
            print("Archivos enviados!")
            opc = int(input(" 4 - Salir de la aplicacion"))
        elif opc == 3:
            num = int(input("Escriba al numero de clientes que desea transmitir el archivo:"))
            enviar_archivos(3, num, conn)
            print("Archivos enviados!")
            opc = int(input(" 4 - Salir de la aplicacion"))
        elif opc == 4:
            opc = int(input("(Opciones 1 y 0 ) Finalizar envio de paquetes: No:1 , Si:0") )
        else:
            break
        
def enviar_archivos(tipo, cantidad, conn):
        cmd = "UPLOADSERVER"
        if tipo == 2:
            path = "server_data/100MB.txt"

        with open(f"{path}", "r") as f:
            text = f.read()

        filename = path.split("/")[-1]
        send_data = f"{cmd}@{filename}@{text}"
        conn.send(send_data.encode(FORMAT))
   

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")
    conexiones = []

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        
        modo = int(input('desea enviar archivos No:0 , Si:1'))
        
        conexiones.append(conn)
        if modo == 1:
            archivos(conn)

if __name__ == "__main__":
    main()