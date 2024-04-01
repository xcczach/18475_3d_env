from arm3d import Arm3D, Joint, animate, initialize_plot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

joints = [
    Joint(theta=0, d=0, a=1, alpha=0, joint_type="rotational"),
    Joint(theta=0, d=0, a=1, alpha=0, joint_type="rotational"),
    Joint(theta=0, d=1, a=0, alpha=0, joint_type="prismatic"),
]

arm = Arm3D(joints, linewidth=5)
ax = initialize_plot()

# 定义旋转角度或平移距离变化，创建动画
angles = [
    # 分别对应节点1、2的旋转角度和节点3的平移距离
    [0, 0, 0],
    [0, 0, 1],
    [0, 0, 2],
    # ... 更多变化 ...
    [0, 0, 2],
    [45, 0, 2],
    [90, 0, 2],
    [90, 45, 2],
    [90, 90, 2],
]

ani = FuncAnimation(
    plt.gcf(), animate, frames=len(angles), fargs=(arm, ax, angles), interval=1000
)

plt.show()
