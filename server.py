import socket
import json
import tkinter as tk
from tkinter import messagebox
import threading  # 导入线程模块
import vgamepad

gamepad = vgamepad.VX360Gamepad()
#定义按键
UP    = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
DOWN  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
LEFT  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
RIGHT = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
 
START = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START
BACK  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK
GUIDE = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
 
LEFT_THUMB     = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
RIGHT_THUMB    = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
LEFT_SHOULDER  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
RIGHT_SHOULDER = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
 
A = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A
B = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B
X = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X
Y = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y
 

def LEFT_TRIGGER(value):
    gamepad.left_trigger_float(value)
    # 左扳机轴 value改成0.0到1.0之间的浮点值
def RIGHT_TRIGGER(value):    
    gamepad.right_trigger_float(value)
    # 右扳机轴 value改成0.0到1.0之间的浮点值
def LEFT_JOYSTICK(x_value, y_value):
    gamepad.left_joystick_float(x_value, y_value)
    # 左摇杆XY轴  x_values和y_values改成-1.0到1.0之间的浮点值
def RIGHT_JOYSTCIK(x_value, y_value):
    gamepad.right_joystick_float(x_value, y_value)
    # 右摇杆XY轴  x_values和y_values改成-1.0到1.0之间的浮点值


server_socket = None
client_socket = None
is_print = False


def send_to_virtual_bluetooth_device(signal):
    """
    模拟将信号发送到虚拟蓝牙设备。
    将接收到的信号映射到虚拟Xbox手柄。
    """
    axes = signal.get("axes", [])
    buttons = signal.get("buttons", [])
    dpad = signal.get("dpad", [])

    gamepad.left_joystick_float(axes[0], -axes[1])
    gamepad.right_joystick_float(axes[2], -axes[3])


    gamepad.left_trigger_float((axes[4]+1)/2)
    gamepad.right_trigger_float((axes[5]+1)/2)


    if buttons[0] == 1:
        gamepad.press_button(A)
    else:
        gamepad.release_button(A)   
    if buttons[1] == 1:
        gamepad.press_button(B)
    else:
        gamepad.release_button(B)
    if buttons[2] == 1:
        gamepad.press_button(X)
    else:
        gamepad.release_button(X)
    if buttons[3] == 1:
        gamepad.press_button(Y)
    else:
        gamepad.release_button(Y)
    if buttons[4] == 1:
        gamepad.press_button(LEFT_SHOULDER)
    else:
        gamepad.release_button(LEFT_SHOULDER)
    if buttons[5] == 1:
        gamepad.press_button(RIGHT_SHOULDER)
    else:
        gamepad.release_button(RIGHT_SHOULDER)
    if buttons[6] == 1:
        gamepad.press_button(BACK)
    else:
        gamepad.release_button(BACK)
    if buttons[7] == 1:
        gamepad.press_button(START)
    else:
        gamepad.release_button(START)
    if buttons[8] == 1:
        gamepad.press_button(LEFT_THUMB)
    else:
        gamepad.release_button(LEFT_THUMB)
    if buttons[9] == 1:
        gamepad.press_button(RIGHT_THUMB)
    else:
        gamepad.release_button(RIGHT_THUMB)


    # 方向键
    if dpad[0][0]==-1:
        gamepad.press_button(LEFT)
    else:
        gamepad.release_button(LEFT)

    if dpad[0][0]==1:
        gamepad.press_button(RIGHT)
    else:
        gamepad.release_button(RIGHT)

    if dpad[0][1]==1:
        gamepad.press_button(DOWN)
    else:
        gamepad.release_button(DOWN)

    if dpad[0][1]==-1:
        gamepad.press_button(UP)
    else:
        gamepad.release_button(UP)


def update_status(message):
    status_label.config(text=message)

def start_server():
    global server_socket, client_socket
    SERVER_HOST = entry_host.get()
    SERVER_PORT = int(entry_port.get())

    update_status("监听中...")

    try:
        # 创建Socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")
        update_output(f"Server is listening on \n {SERVER_HOST}:{SERVER_PORT}")

        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        update_output(f"Connection from \n {client_address}")
        update_status("已连接")

        # 接收手柄信号
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("No data received, closing connection.")
                update_output("No data received, closing connection.")
                break

            # 解析信号
            try:
                signal = json.loads(data.decode("utf-8"))
                if is_print:
                    output_text.delete(1.0, tk.END)
                    formatted_signal = json.dumps(signal, indent=4, ensure_ascii=False)
                    update_output(formatted_signal)
                send_to_virtual_bluetooth_device(signal)
                gamepad.update()
            except json.JSONDecodeError as e:
                print(f"Received invalid data: {e}")
                update_output(f"Received invalid data: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if client_socket:
            client_socket.close()
        if server_socket:
            server_socket.close()
        update_status("空闲")
        print("Server stopped.")
        update_output("Server stopped.")

def start_server_thread():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

def stop_server():
    global server_socket, client_socket
    if client_socket:
        client_socket.close()
        client_socket = None
    if server_socket:
        server_socket.close()
        server_socket = None
    update_status("空闲")
    print("Server stopped.")
    update_output("Server stopped.")
def on_closing():
    stop_server()  # 确保停止服务器
    root.destroy()  # 关闭窗口

# 创建图形界面
root = tk.Tk()
root.title("手柄信号接受端")
root.geometry("250x620")  # 指定窗口大小
root.resizable(False, False)  # 不允许用户调整窗口大小

tk.Label(root, text="Server IP:").pack(pady=5)
entry_host = tk.Entry(root)
entry_host.pack(pady=5)
entry_host.insert(0, "127.0.0.1")

tk.Label(root, text="Server Port:").pack(pady=5)
entry_port = tk.Entry(root)
entry_port.pack(pady=5)
entry_port.insert(0, "12345")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="监听", command=start_server_thread)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="停止", command=stop_server)
stop_button.pack(side=tk.LEFT, padx=5)

# 状态标签
status_label = tk.Label(root, text="空闲", font=("Helvetica", 12))
status_label.pack(pady=10)

output_text = tk.Text(root, height=70, width=30)
output_text.pack(pady=5)

def update_output(message):
    output_text.insert(tk.END, message + "\n")


# 处理窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
