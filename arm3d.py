import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection


class Joint:
    def __init__(self, theta=0, d=0, a=0, alpha=0, joint_type="rotational"):
        self.theta = np.radians(
            theta
        )  # Joint angle for rotational, translation value for prismatic
        self.d = d  # Distance along previous z to the common normal
        self.a = a  # Length of the common normal (aka arm's length)
        self.alpha = np.radians(
            alpha
        )  # Angle about common normal, from old z axis to new z axis
        self.joint_type = joint_type  # 'rotational' or 'prismatic'
        self.transform_matrix = None
        self.update_transform_matrix()

    def update_transform_matrix(self):
        ct = np.cos(self.theta)
        st = np.sin(self.theta)
        ca = np.cos(self.alpha)
        sa = np.sin(self.alpha)
        self.transform_matrix = np.array(
            [
                [ct, -st * ca, st * sa, self.a * ct],
                [st, ct * ca, -ct * sa, self.a * st],
                [0, sa, ca, self.d],
                [0, 0, 0, 1],
            ]
        )

    def set_param(self, param):
        self.set_theta(param)
        self.set_d(param)

    def set_theta(self, theta):
        if self.joint_type == "rotational":
            self.theta = np.radians(theta)
            self.update_transform_matrix()

    def set_d(self, d):
        if self.joint_type == "prismatic":
            self.d = d
            self.update_transform_matrix()


class Arm3D:
    def __init__(self, joints, linewidth=2):
        self.joints = joints
        self.points = []
        self.linewidth = linewidth
        self.update_points()

    def update_points(self):
        # Update the points positions based on the joints' transformations
        transform = np.eye(4)  # Identity matrix
        points = [transform[:3, 3]]  # Start with the base position
        for joint in self.joints:
            transform = np.dot(transform, joint.transform_matrix)
            points.append(transform[:3, 3])
        self.points = np.array(points)

    def plot_arm(self, ax):
        # Clear previous drawings
        ax.cla()
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([0, 4])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Plot the arm
        lines = [
            [self.points[i], self.points[i + 1]] for i in range(len(self.points) - 1)
        ]
        lc = Line3DCollection(lines, colors="blue", linewidths=self.linewidth)
        ax.add_collection(lc)

        # Plot joints
        for pt in self.points:
            ax.scatter(pt[0], pt[1], pt[2], color="red", s=100)


def initialize_plot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    return ax


def animate(i, arm, ax, angle_or_distances):
    for j, param in enumerate(angle_or_distances[i]):
        arm.joints[j].set_param(param)
    arm.update_points()
    arm.plot_arm(ax)
