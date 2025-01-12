import socket
import json
import time
import pygame
import tkinter as tk
from tkinter import messagebox

# 客户端配置
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

client_socket = None  # 初始化客户端socket为None

def connect_to_server(host, port):
    # 创建 Socket
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def start_client():
    # 获取用户输入的 IP 和端口
    host = entry_host.get()
    port = int(entry_port.get())

    try:
        connect_to_server(host, port)
        print(f"Connected to server at {host}:{port}")

        while True:
            # 获取手柄事件
            pygame.event.pump()

            # 读取手柄按键和轴数据
            signal = {
                "axes": [joystick.get_axis(i) for i in range(joystick.get_numaxes())],
                "buttons": [joystick.get_button(i) for i in range(joystick.get_numbuttons())],
                "dpad": [joystick.get_hat(i) for i in range(joystick.get_numhats())],
            }

            # 发送信号
            client_socket.sendall(json.dumps(signal).encode("utf-8"))
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Client disconnected")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        disconnect()  # 确保断开连接

def disconnect():
    global client_socket
    if client_socket:
        client_socket.close()
        client_socket = None
        print("Disconnected from server")
        connect_button.config(state=tk.NORMAL)  # 重新启用连接按钮

def quit_program():
    disconnect()  # 先断开连接
    root.quit()  # 退出程序

def check_gamepad():
    # 初始化 Pygame 手柄支持
    pygame.init()
    pygame.joystick.init()

    # 检查是否有手柄连接
    if pygame.joystick.get_count() == 0:
        messagebox.showerror("Error", "No gamepad connected")
        connect_button.config(state=tk.DISABLED)  # 禁用连接按钮
        return False

    global joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to gamepad: {joystick.get_name()}")
    return True

# 创建图形界面
root = tk.Tk()
root.title("Gamepad Client")
root.geometry("600x400")  # 设置初始窗口大小
root.resizable(True, True)  # 允许窗口大小调整

tk.Label(root, text="Server IP:").pack()
entry_host = tk.Entry(root)
entry_host.pack()
entry_host.insert(0, SERVER_HOST)

tk.Label(root, text="Server Port:").pack()
entry_port = tk.Entry(root)
entry_port.pack()
entry_port.insert(0, str(SERVER_PORT))

connect_button = tk.Button(root, text="Connect", command=start_client)
connect_button.pack()

disconnect_button = tk.Button(root, text="Disconnect", command=disconnect)
disconnect_button.pack()

quit_button = tk.Button(root, text="Quit", command=quit_program)
quit_button.pack()

# 检查手柄连接
check_gamepad()

root.mainloop()
