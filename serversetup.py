from cx_Freeze import setup, Executable

setup(
    name="手柄信号传输接收端2025年1月12日14点44分",
    version="0.1.2",
    description="手柄信号传输接收端",
    executables=[Executable("server.py", base="Win32GUI")]
)
# python setup.py build