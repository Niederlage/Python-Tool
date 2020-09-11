import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import namedtuple
from scipy.spatial.transform import Rotation as R


# header = ['Timestamp','Trans_x', 'Trans_y', 'Trans_z',
#           'Quaternion_w', 'Quaternion_x', 'Quaternion_y', 'Quaternion_z']

def quaternion2Rot(quart_list):
    r_list = [R.from_quat(i).as_matrix() for i in quart_list]
    return np.array(r_list)


def quaternion2Euler(quart_list):
    r_list = [R.from_quat(i).as_euler('zyx', degrees=True) for i in quart_list]
    return np.array(r_list)

def pose_2_SE3(pose):
    trans = pose[:, :3]
    rot = quaternion2Rot(pose[:, 3:])
    pose_list = []
    for i in range(len(rot)):
        p = trans[i,None]
        pose_up = np.hstack((rot[i], p.T))
        pose_m = np.vstack((pose_up, [0.,0.,0.,1.]))
        pose_list.append(pose_m)

    return pose_list

def csv_to_pose(path):
    camPose_list = []
    with open(path) as cam_csv:
        camdata = csv.reader(cam_csv)
        headers = next(camdata)
        Row = namedtuple('Row', headers)
        for r in camdata:
            row = Row(*r)
            for temp in row:
                camPose_list.append(float(temp))

    pose = np.array(camPose_list).reshape(-1, 8)
    if 'noisy' in path:
        pose[:, 2] = -pose[:, 2]

    return pose


def calculate_baseline(traj):
    size = np.size(traj, axis=0)
    dis_seq = []
    for i in range(1, size):
        dis_seq.append(np.linalg.norm(traj[i][1:4] - traj[i - 1][1:4]))
        # print('d{order} = {num:.2f}m'.format(order=i, num=dis_list[i-1]))
    dis_seq = np.array(dis_seq)
    return dis_seq


def plot_baseline(baseline):
    baseline = np.delete(baseline, 0)

    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.plot(baseline, color='tab:red', label='ground truth')
    ax1.set_xlabel('frame', fontsize=20)
    ax1.set_ylabel('baseline', fontsize=20)
    ax1.set_title('compared OpenVSLAM and Ground Truth', fontsize=20)
    ax1.tick_params(axis='x', rotation=0, labelsize=12)
    ax1.tick_params(axis='y', rotation=0)
    ax1.grid(alpha=.4)
    ax1.grid(True)

    # # # Plot Line2 (Right Y Axis)
    ax2 = fig.add_subplot(122)
    counts, bins = np.histogram(baseline)
    edges = np.delete(bins, 0)
    res = edges.dot(counts) / len(baseline)

    ax2.hist(bins[:-1], bins, weights=counts, facecolor='tab:red', alpha=0.75)
    print('average baseline:={:.3f}m'.format(res))
    ax2.grid(alpha=.4)
    ax2.grid(True)

    # # # ax2 (right Y axis)
    ax2.set_ylabel("frequency", color='tab:blue', fontsize=20)
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_xlabel('baseline/m', fontsize=20)
    # plt.ylim(0, 1)
    ax2.set_title("Distribution of Baseline", fontsize=22)
    # plt.tight_layout()
    plt.show()

def plot_pose(pose_cw, rot_trans=False):

    # zw = pose_cw[pose_cw[:, 0].argsort()]  # 按第'1'列排序
    if rot_trans:
        pose_matrix = pose_2_SE3(pose_cw)

        pose_ = pose_matrix[0]
        pose_w = np.copy(pose_[:3, 3])
        for i in range(len(pose_matrix)):
            pose_ = pose_matrix[i].dot(pose_)
            pose_w = np.vstack((pose_w, pose_[:3, 3]))
    else:
        pose_w = pose_cw[:, :3]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # ax = fig.gca()
    # # Plot the surface.
    # surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm,
    #                    linewidth=0, antialiased=False,alpha = 0.5)
    ax.plot(pose_w[:, 0], pose_w[:, 1], pose_w[:, 2], "o-", label='pose points')
    ax.legend()  # 画一条空间曲线
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # ax.set_xlim(-5, 12)
    # ax.set_ylim(-6, 12)
    # ax.set_zlim(-6, 6)
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def visualize_pose_baseline(pathreal):
    realpose = csv_to_pose(pathreal)
    total_frame = np.size(realpose, axis=0)
    real_baseline = calculate_baseline(realpose)
    traj_name = pathreal.replace('_blender.csv', '')
    real_traj_length = real_baseline.sum()
    print(traj_name + ' length =', real_traj_length)
    print('average driving speed = {:.3f} m/frame'.format(real_traj_length / total_frame))
    plot_baseline(real_baseline)


if __name__ == "__main__":
    path = 'Camera_Resident_ideal_blender.csv'
    path2 = 'Camera_Uni_ideal_blender.csv'
    path3 = 'Camera_Resident_noisy_blender.csv'
    path4 = 'Camera_Uni_noisy_blender.csv'

    # visualize_pose_baseline(path)
    # visualize_pose_baseline(path)
    # visualize_pose_baseline(path2)
    pose = csv_to_pose(path)
    plot_pose(pose[:, 1:])

    print(2)
