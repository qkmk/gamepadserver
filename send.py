import socket
import json
import threading
import pygame
import tkinter as tk
from tkinter import messagebox
import time

# 定义状态标志
STATUS_IDLE = "空闲"
STATUS_CONNECTED = "已连接"

# 初始化状态
current_status = STATUS_IDLE

running = True  # 控制线程运行的标志

test_thread = None  # 用于存储测试线程的引用
testing = False  # 控制测试状态

available_joysticks = []  # 存储可用手柄的列表

frequency = 0.05  # 默认发送频率


def connect_to_server(host, port):
    # 创建 Socket
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def check_gamepad():
    # 初始化 Pygame 手柄支持
    pygame.init()
    pygame.joystick.init()

    # 检查是否有手柄连接
    if pygame.joystick.get_count() == 0:
        messagebox.showerror("Error", "No gamepad connected")
        return False

    global joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to gamepad: {joystick.get_name()}")
    update_output(f"Connected to gamepad: {joystick.get_name()}")
    return True

def update_status(message):
    global current_status
    current_status = message
    status_label.config(text=message)
    connection_button.config(text="断开连接" if message == STATUS_CONNECTED else "连接")  # 更新按钮文本

def start_server_thread():
    global running  # 声明使用全局变量
    host = entry_host.get()
    port = int(entry_port.get())
    
    def run():
        global running  # 声明使用全局变量
        try:
            connect_to_server(host, port)  # 连接到服务器
            update_status(STATUS_CONNECTED)  # 更新状态标签
            update_output(f"成功连接到服务器 {host}:{port}")
            
            while running:  # 检查运行标志
                # 获取手柄信号并发送
                signal = get_signal()
                if client_socket:  # 确保 client_socket 有效
                    output_text.delete(1.0, tk.END)
                    client_socket.sendall(json.dumps(signal).encode("utf-8"))
                    # formatted_signal = json.dumps(signal, indent=4, ensure_ascii=False)
                    # update_output(formatted_signal)
                time.sleep(frequency)  # 使用用户设置的频率

        except Exception as e:
            messagebox.showerror("Error", str(e))
            update_status(STATUS_IDLE)  # 更新状态标签为空闲

    # 创建并启动线程
    thread = threading.Thread(target=run)
    thread.start()

def stop_server_thread():
    global client_socket
    if 'client_socket' in globals() and client_socket:  # 检查 client_socket 是否已定义且有效
        client_socket.close()
    update_status(STATUS_IDLE)  # 更新状态标签为空闲
    update_output("已断开连接")

def get_signal():
    signal = {
        "axes": [joystick.get_axis(i) for i in range(joystick.get_numaxes())],
        "buttons": [joystick.get_button(i) for i in range(joystick.get_numbuttons())],
        "dpad": [joystick.get_hat(i) for i in range(joystick.get_numhats())],
    }
    return signal

def test_signal_output():
    global testing
    testing = True
    while testing:
        signal = get_signal()  # 获取手柄信号
        output_text.delete(1.0, tk.END)
        formatted_signal = json.dumps(signal, indent=4, ensure_ascii=False)
        update_output(formatted_signal)  # 输出到调试窗口
        time.sleep(frequency)  # 使用用户设置的频率

def start_test_thread():
    global test_thread
    test_thread = threading.Thread(target=test_signal_output)
    test_thread.start()
    test_button.config(text="停止", command=stop_test_thread)  # 更改按钮文本和命令

def stop_test_thread():
    global testing
    testing = False  # 停止测试
    output_text.delete(1.0, tk.END)
    test_button.config(text="测试", command=start_test_thread)  # 恢复按钮文本和命令

# 修改按钮的创建和功能
def toggle_connection():
    if current_status == STATUS_IDLE:
        start_server_thread()  # 连接
    else:
        stop_server_thread()  # 断开连接

def update_frequency():
    global frequency
    try:
        frequency = float(frequency_entry.get())  # 获取用户输入的频率
        if frequency <= 0:
            raise ValueError("频率必须大于0")
    except ValueError:
        messagebox.showerror("Error", "请输入有效的频率值")

# 创建图形界面
root = tk.Tk()
root.title("手柄信号接受端")
root.geometry("250x680")  # 指定窗口大小
root.resizable(False, True)  # 不允许用户调整窗口大小

tk.Label(root, text="Server IP:").pack(pady=5)
entry_host = tk.Entry(root)
entry_host.pack(pady=5)
entry_host.insert(0, "127.0.0.1")

tk.Label(root, text="Server Port:").pack(pady=5)
entry_port = tk.Entry(root)
entry_port.pack(pady=5)
entry_port.insert(0, "12345")

# 添加发送频率输入框
tk.Label(root, text="发送间隔 (秒):").pack(pady=5)
frequency_frame = tk.Frame(root)  # 创建一个框架来放置输入框和按钮
frequency_frame.pack(pady=5)

frequency_entry = tk.Entry(frequency_frame)  # 将输入框放入框架中
frequency_entry.pack(side=tk.LEFT)  # 输入框在左边
frequency_entry.insert(0, str(frequency))  # 设置默认值

frequency_button = tk.Button(frequency_frame, text="设置频率", command=update_frequency)  # 将按钮放入框架中
frequency_button.pack(side=tk.LEFT)  # 按钮在右边

button_frame = tk.Frame(root)
button_frame.pack(pady=10)  

# 创建连接/断开连接按钮
connection_button = tk.Button(button_frame, text="连接", command=toggle_connection)
connection_button.pack(side=tk.LEFT, padx=5)

# 添加测试按钮
test_button = tk.Button(button_frame, text="测试", command=start_test_thread)
test_button.pack(side=tk.LEFT, padx=5)

# 状态标签
global status_label
status_label = tk.Label(root, text="空闲", font=("Helvetica", 12))
status_label.pack(pady=10)

output_text = tk.Text(root, height=70, width=30)
output_text.pack(pady=5)

def update_output(message):
    output_text.insert(tk.END, message + "\n")

# 处理窗口关闭事件
def on_closing():
    global running
    running = False  # 设置标志为 False，停止线程
    stop_server_thread()  # 确保停止线程
    root.destroy()  # 关闭窗口

check_gamepad()

# 处理窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()