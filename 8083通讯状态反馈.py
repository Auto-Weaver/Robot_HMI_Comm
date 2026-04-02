import struct
import socket
import time


def socket_1():
    # 连接端口获取信息
    Con_SOCKET = socket.socket()
    Con_SOCKET.connect(('192.168.58.2', 8083))
    RV = Con_SOCKET.recv(1024)
    rvv = []

    for i in range(len(RV)):
        rvv.append(hex(RV[i]))
    # print("字节流数据:" + str(RV))
    # print("hex类型数组:" + str(rvv))
    print("字节流长度:" + str(len(RV)))
    print("数据类容长度:" + str(RV[3]))
    print("机器人状态:" + str(RV[5]))
    print("机器人错误码:" + str(RV[6]))
    print("机器人主故障码:" + str(RV[7]))
    print("机器人子故障码:" + str(RV[8]))
    print("机器人运行模式:" + str(RV[9]))


def socket_2():
    Con_SOCKET = socket.socket()
    Con_SOCKET.connect(('192.168.58.2', 8083))
    RV = Con_SOCKET.recv(1024)

    pose_name = ["j1", "j2", "j3", "j4", "j5", "j6", "x_pose", "y_pose", "z_pose", "rx_pose", "ry_pose", "rz_pose"]
    Torque_name = ["j1 tor", "j2 tor", "j3 tor", "j4 tor", "j5 tor", "j6 tor"]
    # 关节位置和TCP位置
    for i in range(len(pose_name)):
        # 每个 double 占 8 字节，从 i * 8 开始
        value = struct.unpack("d", RV[i * 8:(i + 1) * 8])[0]
        print(f"{pose_name[i]}: {value:.4f}")

    tool_num = int.from_bytes(RV[104:108], byteorder="little")
    print("tool number:", tool_num)
    # 输出关节扭矩
    for i in range(len(Torque_name)):
        value = struct.unpack("d", RV[i * 8 + 108:(i + 1) * 8 + 108])[0]
        print(f"{Torque_name[i]}: {value:.4f}")


def reverse_IO(str1):
    states = [f"输出{i+1}: {'ON' if b == '1' else 'OFF'}" for i, b in enumerate(str1[::-1])]
    return ", ".join(states)


def socket_3():
    Con_SOCKET = socket.socket()
    Con_SOCKET.connect(('192.168.58.2', 8083))
    RV = Con_SOCKET.recv(1024)

    co_binary_str = bin(RV[178])[2:].zfill(8)
    do_binary_str = bin(RV[179])[2:].zfill(8)
    ci_binary_str = bin(RV[181])[2:].zfill(8)
    di_binary_str = bin(RV[182])[2:].zfill(8)
    dO_END_binary_str = bin(RV[180])[2:].zfill(8)
    di_END_binary_str = bin(RV[183])[2:].zfill(8)

    print("CO状态: " + reverse_IO(co_binary_str))
    print("DO状态: " + reverse_IO(do_binary_str))
    print("CI状态: " + reverse_IO(ci_binary_str))
    print("DI状态: " + reverse_IO(di_binary_str))
    # print("末端do状态: " + reverse_IO(dO_END_binary_str))
    # print("末端di状态: " + reverse_IO(di_END_binary_str))

    #输出急停
    print("EmergencyStop:" + str(RV[234]))
    #输出运动到位信号
    print("motion_done:" + str(RV[238]))
    #输出碰撞检测信号
    # print("collisionState:" + str(RV[186]))
    # #输出安全停止SI0,SI1
    # print("safety_stop0_state:" + str(RV[187]))
    # print("safety_stop1_state:" + str(RV[188]))
    # #输出运动队列长度
    # print("mc_queue_len:" + str(RV[189]))
    #输出夹爪运动完成信号
    print("gripper_motiondone:" + str(RV[239]))

while True:
    # socket_1()
    socket_2()
    time.sleep(1)
    # socket_3()
