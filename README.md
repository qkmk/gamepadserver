# 远程手柄

使用cursor写的,实现了基本功能

受够了联机受限于服务器和加速器。
只传输手柄信号，视频流可以使用别的软件来

发送端连接手柄，指定ip端口。
接收端创建虚拟手柄，从指定ip端口接收手柄信号。

先打开接收端监听再点击发送端的连接按钮。

# 需要
可能需要vcruntime140.dll，确保和server在同一文件夹下
需要安装虚拟手柄驱动ViGEmBus<https://github.com/ViGEm/ViGEmBus>

# 测试
自己还没测试,可以的话找朋友联机玩会儿再说.

# 缺点
好多好多的炒饭,想不到也处理不到.
发送端退出可能会留下几个线程,需要在任务管理器自己结束一下.
接收端目前看来没啥问题.
连接过程不太顺畅

# 未来可能的功能
可以指定手柄进行发送.(为什么要发送两个及以上的手柄的,,这么多人玩点别的吧)
接收端可以指定虚拟手柄的ID.
信号返回,从而支持手柄震动.
