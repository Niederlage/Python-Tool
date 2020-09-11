from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.spatial.transform import Rotation as R
import msgpack
import numpy as np


def quaternion2Rot(quart_list):
    r_list = [R.from_quat(i).as_matrix() for i in quart_list]
    return np.array(r_list)

def quaternion2Euler(quart_list):
    r_list = [R.from_quat(i).as_euler('zyx', degrees=True) for i in quart_list]
    return np.array(r_list)

def angle_constraint(theta_list):
    quat_list = []
    for i in range(len(theta_list)):
        ta = theta_list[i, 0]
        tb = theta_list[i, 1]
        tc = theta_list[i, 2]
        if abs(ta) > 178:
            theta_list[i, 0] = np.sign(ta) * (180. - abs(ta))
        if abs(tb) > 178:
            theta_list[i, 1] = np.sign(tb) * (180. - abs(tb))
        if abs(tc) > 178:
            theta_list[i, 2] = np.sign(tc) * (180. - abs(tc))
        r = R.from_rotvec(theta_list[i])
        quat_list.append(r.as_quat())

    return np.array(quat_list)


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

def msg_unpack_to_array(path_in):
    landmark_list = []
    keyframe_scale = []
    keyframe_pose_cw = np.zeros((1, 9))
    keyframe_undists = []
    # path_in = 'test_simu_equirectangular_uni.msg'
    with open(path_in, 'rb') as data_file:
        data_load = msgpack.unpack(data_file, encoding='utf-8')
        landmarks = data_load['landmarks']
        keyframes = data_load['keyframes']
        for i in landmarks:
            landmark_list.append(landmarks[i]['pos_w'])
        for j in keyframes:
            keyframe_undists.append(keyframes[j]['undists'])
            keyframe_scale.append(keyframes[j]['scale_factor'])
            src_frame_id = keyframes[j]['src_frm_id']
            kf_temp = np.hstack(([int(j), src_frame_id], np.array(keyframes[j]['trans_cw'])))
            kf_temp = np.hstack((kf_temp, np.array(keyframes[j]['rot_cw'])))
            keyframe_pose_cw = np.vstack((keyframe_pose_cw, kf_temp))

    keyframe_pose_cw = np.delete(keyframe_pose_cw, 0, axis=0)

    return np.array(landmark_list), np.array(keyframe_scale), keyframe_pose_cw, keyframe_undists


def plot_landmarks(line):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # # Plot the surface.
    # surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm,
    #                    linewidth=0, antialiased=False,alpha = 0.5)
    ax.scatter(line[:, 0], line[:, 2], line[:, 1], label='Feather points', color='r', marker='o')
    ax.legend()  # 画一条空间曲线
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim(-5, 12)
    ax.set_ylim(-6, 12)
    ax.set_zlim(-6, 6)
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def plot_2D_Landmarks(landmarks):
    plt.figure('Scatter Feather points')
    ax = plt.gca()
    # 设置x轴、y轴名称
    # 画散点图，以x_list中的值为横坐标，以y_list中的值为纵坐标
    # 参数c指定点的颜色，s指定点的大小,alpha指定点的透明度
    ax.scatter(landmarks[:, 2], landmarks[:, 0], label='Feather points', color='r', marker='o', alpha=0.5)
    ax.legend()  # 画一条空间曲线
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(-6.5, 18)
    ax.set_ylim(-3, 14)

    plt.show()


def plot_unidists(unidists):
    plt.figure('Scatter Feather points')
    ax = plt.gca()

    # 画散点图，以x_list中的值为横坐标，以y_list中的值为纵坐标
    # 参数c指定点的颜色，s指定点的大小,alpha指定点的透明度
    ax.scatter(unidists[:, 0], unidists[:, 1], label='Feather points in one frame', color='b', marker='o', alpha=0.5)
    ax.legend()  # 画一条空间曲线
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    # ax.set_xlim(-6.5, 18)
    # ax.set_ylim(-3, 14)
    plt.show()


def plot_animation(keyframe_undists):
    for unidists in keyframe_undists:
        plt.cla()
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        ax = plt.gca()
        # for stopping simulation with the esc key.
        unidists = np.array(unidists)
        # point_num = len(unidists)
        plt.gcf().canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])
        # for i in range(point_num):
        ax.scatter(unidists[:, 0], unidists[:, 1], label='Feather points in one frame', color='purple', marker='o',
                   alpha=0.5)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_xlim(0, 1280)
        ax.set_ylim(0, 720)
        ax.axis("equal")
        plt.grid(True)
        plt.pause(0.1)

    plt.show()


def plot_pose(pose_cw, rot_trans=True):

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
    ax.scatter(pose_w[0, 0], pose_w[0, 1], pose_w[0, 2], color="red")
    ax.scatter(pose_w[10, 0], pose_w[10, 1], pose_w[10, 2], color="red")
    ax.scatter(pose_w[-1, 0], pose_w[-1, 1], pose_w[-1, 2], color="purple")
    ax.legend()  # 画一条空间曲线
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # ax.set_xlim(-5, 12)
    # ax.set_ylim(-6, 12)
    # ax.set_zlim(-6, 6)
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def plot_baseline(baseline):
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


if __name__ == '__main__':
    path = 'test_simu_equirectangular_resident.msg'
    SAVE_MSG = False
    PLOT_POSE = True
    PLOT_LANDMARKS = False
    PLOT_LANDMARKS_3D = True
    PLOT_ANIMATION = False


    if SAVE_MSG:
        landmarks, keyframe_scale, keyframe_pose_cw, keyframe_undists = msg_unpack_to_array(path)
        np.save('landmarks.npy',landmarks)
        np.save('keyframe_scale.npy',keyframe_scale)
        np.save('keyframe_pose_cw.npy',keyframe_pose_cw)
        np.save('keyframe_unidists.npy',keyframe_undists[6])
        if PLOT_ANIMATION:
            plot_animation(keyframe_undists)


    if PLOT_POSE:
        kf_pose_cw = np.load('keyframe_pose_cw.npy')
        # theta = quaternion2Euler(kf_pose_cw[:, 5:])
        # quat = angle_constraint(theta)
        # kf_pose_cw[:, 5:] = quat
        # t2 = quaternion2Euler(quat)
        zw = kf_pose_cw[kf_pose_cw[:, 0].argsort()]  # 按第'1'列排序
        plot_pose(zw[:, 2:], rot_trans=True)

    if PLOT_LANDMARKS:
        lm = np.load('landmarks.npy')
        if PLOT_LANDMARKS_3D:
            plot_landmarks(lm)
        else:
            plot_2D_Landmarks(lm)


    print(1)
