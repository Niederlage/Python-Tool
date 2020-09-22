import numpy as np
import matplotlib.pyplot as plt
from mathutils import Quaternion
from blender_to_traj import Blender_to_Traj
from msg_to_traj import Msg_to_Traj


def plot_baseline(b_line, m_line):

    fig = plt.figure()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    # plot ground truth baseline info
    ax = fig.add_subplot(221)
    ax.plot(b_line, color='tab:red', label='ground truth')
    # ax.set_xlabel('frame', fontsize=20)
    ax.set_ylabel('baseline/m', fontsize=20)
    ax.set_title('Ground Truth', fontsize=20)
    ax.tick_params(axis='x', rotation=0, labelsize=12)
    ax.tick_params(axis='y', rotation=0)
    ax.grid(alpha=.4)
    ax.grid(True)

    # # # Plot Line2 (Right Y Axis)
    ax = fig.add_subplot(222)
    counts, bins = np.histogram(b_line)
    # edges = np.delete(bins, 0)
    # res = edges.dot(counts) / len(b_line)
    b_sum = 0
    for i, _ in enumerate(b_line):
        b_sum += b_line[i]**2
    b_RMSE = np.sqrt(b_sum/len(b_line))

    ax.hist(bins[:-1], bins, weights=counts, facecolor='tab:red', alpha=0.75)
    b_str = 'Groud Truth RPE:={:.3f}m'.format(b_RMSE)
    plt.text(0.42, 400, b_str, fontsize=16)
    # ax.grid(alpha=.4)
    # ax.grid(True)

    # # # ax (right Y axis)
    ax.set_ylabel("frequency", fontsize=20)
    ax.tick_params(axis='y') #, labelcolor='tab:blue'
    # ax.set_xlabel('baseline/m', fontsize=20)
    # plt.ylim(0, 1)
    ax.set_title("Distribution of Baseline Length", fontsize=20)

    # plot OpenVSLAM baseline info
    ax = fig.add_subplot(223)
    ax.plot(m_line, color='tab:blue', label='OpenVSLAM')
    ax.set_xlabel('frame', fontsize=20)
    ax.set_ylabel('baseline/m', fontsize=20)
    ax.set_title('OpenVSLAM', fontsize=20)
    ax.tick_params(axis='x', rotation=0, labelsize=12)
    ax.tick_params(axis='y', rotation=0)
    ax.grid(alpha=.4)
    ax.grid(True)

    # # # Plot Line2 (Right Y Axis)
    ax = fig.add_subplot(224)
    counts, bins = np.histogram(m_line)
    # edges = np.delete(bins, 0)
    # res = edges.dot(counts) / len(m_line)
    m_sum = 0
    for i, _ in enumerate(m_line):
        m_sum += m_line[i] ** 2
    m_RMSE = np.sqrt(m_sum / len(m_line))
    ax.hist(bins[:-1], bins, weights=counts, facecolor='tab:blue', alpha=0.75)
    m_str = 'OpenVSLAM RPE :={:.3f}m'.format(m_RMSE)
    plt.text(0.8, 35, m_str, fontsize=16)
    # ax.grid(alpha=.4)
    # ax.grid(True)

    # # # ax (right Y axis)
    ax.set_ylabel("frequency", fontsize=20)
    ax.tick_params(axis='y')
    ax.set_xlabel('baseline/m', fontsize=20)
    # plt.ylim(0, 1)
    # ax.set_title("Distribution of Baseline", fontsize=22)


    # plt.tight_layout()
    # plt.show()


def plot_traj(pose_b, pose_m):
    fig = plt.figure()

    ax = fig.gca()
    # draw groud truth trajectory
    ax.plot(pose_b[:, 0], pose_b[:, 1], "-", color='tab:red', label='groud truth trajectory')
    ax.plot(pose_b[0, 0], pose_b[0, 1], color="red")
    # ax.scatter(pose_b[10, 0], pose_b[10, 1], color="green")
    ax.scatter(pose_b[-1, 0], pose_b[-1, 1], color="purple")

    # draw OpenVSLAM trajectory
    ax.plot(pose_m[:, 0], pose_m[:, 1], "-", color='tab:blue', label='OpenVSLAM trajectory')
    ax.plot(pose_m[0, 0], pose_m[0, 1], color="red")
    # ax.scatter(pose_m[10, 0], pose_m[10, 1], color="green")
    ax.scatter(pose_m[-1, 0], pose_m[-1, 1], color="purple")

    ax.legend()  # 画一条空间曲线
    ax.set_xlabel('X/m',fontsize=20)
    ax.set_ylabel('Y/m',fontsize=20)
    # ax.set_xlim(-5, 12)
    # ax.set_ylim(-6, 12)
    # ax.set_zlim(-6, 6)
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    # plt.show()

def get_corresponding_frame(m_list, b_list):
    a = m_list[:, 2]


def main():
    # msgpath = 'test_simu_equirectangular_resident.msg'
    msgpath = 'resident_EQT_0p5.msg'
    blenderpath = 'Camera_Resident_ideal_blender.csv'
    msgfolderpath = 'saved_data/from_msg_data/'
    blenderfolderpath = 'saved_data/from_blender_csv/'

    msgtraj = Msg_to_Traj(msgpath)
    blendertraj = Blender_to_Traj(blenderfolderpath + blenderpath)

    # loading msg data
    if LOAD_MSGDATA:
        load_data = np.load(msgfolderpath + 'saved_resident_EQT_0p5.npz')
        print('file loaded successfully...')
        kf_pose_cw = load_data['keyframe_pose_cw']

    else:
        landmarks, keyframe_scale, kf_pose_cw, keyframe_undists = msgtraj.msg_unpack_to_array()

    m_pose = kf_pose_cw[kf_pose_cw[:, 0].argsort()]  # 按第'1'列排序
    m_pose = msgtraj.get_trajectory(m_pose[:, 2:])
    m_baseline = msgtraj.cal_baseline(m_pose)

    # adjust map orientation
    m_traj = m_pose[:, ::2]  # (82, 2)
    m_traj[:, 1] = -m_traj[:, 1]

    # loading blender data
    b_pose = blendertraj.csv_to_pose()
    b_traj = b_pose[:, 1:3]
    b_traj = blendertraj.rot_traj(b_traj, -np.pi * 2 / 4)  # (1537, 2)
    b_baseline = blendertraj.cal_baseline(b_pose[:, 1:4])

    if PLOT_TRAJ:
        plot_traj(b_traj-b_traj[0,:], m_traj)

    if PLOT_BASELINE:
        plot_baseline(b_baseline, m_baseline)

    plt.show()

if __name__ == '__main__':
    LOAD_MSGDATA = True
    PLOT_TRAJ = True
    PLOT_BASELINE = True
    main()
