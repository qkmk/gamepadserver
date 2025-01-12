from cx_Freeze import setup, Executable

setup(
    name="手柄信号传输发射端2025年1月12日12点54分",
    version="0.2",
    description="手柄信号传输发射端",
    executables=[Executable("send.py", base="Win32GUI")]
)
# python sendsetup.py build