# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def main():
    draw1setup()
    draw2encrypt()
    draw3register()
    draw4authorize()
    draw5transform()
    draw6dec1()
    draw7dec2()


def draw1setup():
    input_data = {'x': [5, 10, 15, 20, 25],
                  'y1': [0.13083, 0.2476, 0.365, 0.4813, 0.6004],
                  'y2': [0.3158, 0.3158, 0.3158, 0.3155, 0.3158],
                  'y3': [0.0577, 0.0988, 0.1403, 0.1815, 0.2234],
                  'y4': [0.0679, 0.1085, 0.151, 0.1936, 0.2359],
                  'y5': [0.0594, 0.1011, 0.1431, 0.1851, 0.2274],
                  'boxs': [14, 16, 130, 160],
                  'box2anchor': (0.8, 0.05, 0.3, 0.5),
                  'loc': [3, 1],
                  'str': 'Setup Algorithm',
                  'dir': '../doc/draw1setup.png'}
    proc(input_data)


def draw2encrypt():
    input_data = {'x': [5, 10, 15, 20, 25],
                  'y1': [0.1723, 0.3322, 0.4978, 0.6524, 0.8242],
                  'y2': [0.0532, 0.0886, 0.1023, 0.1585, 0.1939],
                  'y3': [0.0711, 0.1261, 0.1836, 0.2399, 0.298],
                  'y4': [0.0462, 0.0746, 0.1027, 0.1305, 0.1589],
                  'y5': [0.0411, 0.0686, 0.0962, 0.124, 0.1516],
                  'boxs': [9, 11, 60, 100],
                  'box2anchor': (0.8, 0.5, 0.3, 0.6),
                  'loc': [4, 2],
                  'str': 'Encrypt Algorithm',
                  'dir': '../doc/draw2encrypt.png'}
    proc(input_data)


def draw3register():
    input_data = {'x': [5, 10, 15, 20, 25],
                  'y1': [0.178, 0.3535, 0.5273, 0.6993, 0.8929],
                  'y2': [0.0448, 0.0732, 0.1013, 0.1292, 0.1575],
                  'y3': [0.0057, 0.0057, 0.0056, 0.0056, 0.0056],
                  'y4': [0.0462, 0.0746, 0.1027, 0.1306, 0.1589],
                  'y5': [0.046, 0.073, 0.1012, 0.13, 0.1575],
                  'boxs': [9, 11, 72, 75],
                  'box2anchor': (0.8, 0.4, 0.3, 0.6),
                  'loc': [4, 2],
                  'str': 'Register Algorithm',
                  'dir': '../doc/draw3register.png'}
    proc(input_data)


def draw4authorize():
    input_data = {'x': [5, 10, 15, 20, 25],
                  'y1': [0.5788, 1.1445, 1.7016, 2.2825, 2.8529],
                  'y2': [0.074, 0.1233, 0.1719, 0.2213, 0.2647],
                  'y3': [0.01594, 0.0163, 0.01675, 0.0173, 0.0177],
                  'y4': [0.06592, 0.1079, 0.1509, 0.1919, 0.2353],
                  'y5': [0.07696, 0.1067, 0.1356, 0.1664, 0.1958],
                  'boxs': [19, 21, 155, 235],
                  'box2anchor': (0.8, 0.3, 0.3, 0.6),
                  'loc': [4, 2],
                  'str': 'Authorize Algorithm',
                  'dir': '../doc/draw4authorize.png'}
    proc(input_data)


def draw5transform():
    input_data = {'x': [5, 10, 15, 20, 25],
                  'y1': [0.0747, 0.1427, 0.2107, 0.2788, 0.3666],
                  'y2': [0.0287, 0.0493, 0.0698, 0.0904, 0.111],
                  'y3': [0.0096, 0.0098, 0.0101, 0.0104, 0.0107],
                  'y4': [0.0107, 0.0113, 0.0118, 0.0124, 0.013],
                  'y5': [0.0108, 0.0115, 0.0123, 0.013, 0.0135],
                  'boxs': [14, 16, 9, 13],
                  'box2anchor': (0.8, 0.4, 0.3, 0.6),
                  'loc': [4, 2],
                  'str': 'Transform Algorithm',
                  'dir': '../doc/draw5transform.png'}
    proc(input_data)


def draw6dec1():
    input_data = {'x': [5, 10, 15, 20, 25],
                  'y1': [0.1496, 0.2857, 0.4221, 0.5584, 0.6941],
                  'y2': [0.0267, 0.0473, 0.0678, 0.0883, 0.109],
                  'y3': [0.011, 0.0018, 0.0107, 0.025, 0.039],
                  'y4': [0.0107, 0.0113, 0.0118, 0.0123, 0.013],
                  'y5': [0.0109, 0.0116, 0.0121, 0.0126, 0.0132],
                  'boxs': [14, 16, 10, 12.5],
                  'box2anchor': (0.8, 0.3, 0.3, 0.6),
                  'loc': [4, 2],
                  'str': 'Decrypt_Original Algorithm',
                  'dir': '../doc/draw6dec1.png'}
    proc(input_data)


def draw7dec2():
    input_data = {'x': [5, 10, 15, 20, 25],
                  'y1': [0.1557, 0.2919, 0.4283, 0.5646, 0.7003],
                  'y2': [0.0332, 0.0602, 0.0872, 0.1142, 0.1412],
                  'y3': [0.0165, 0.024, 0.031, 0.038, 0.0450],
                  'y4': [0.0169, 0.0175, 0.0181, 0.0187, 0.0192],
                  'y5': [0.018, 0.0186, 0.0191, 0.0197, 0.0203],
                  'boxs': [14, 16, 15, 33],
                  'box2anchor': (0.8, 0.3, 0.3, 0.6),
                  'loc': [4, 2],
                  'str': 'Decrypt_Transformed Algorithm',
                  'dir': '../doc/draw7dec2.png'}
    proc(input_data)


def proc(input_data):
    for i in range(5):
        input_data['y1'][i] = input_data['y1'][i] * 1000
        input_data['y2'][i] = input_data['y2'][i] * 1000
        input_data['y3'][i] = input_data['y3'][i] * 1000
        input_data['y4'][i] = input_data['y4'][i] * 1000
        input_data['y5'][i] = input_data['y5'][i] * 1000

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    ax.plot(input_data['x'], input_data['y1'], color='k', linestyle='--', linewidth=1,
            marker='o', markersize=5,
            markeredgecolor='black', markerfacecolor='C0')

    ax.plot(input_data['x'], input_data['y2'], color='g', linestyle='--', linewidth=1,
            marker='s', markersize=5,
            markeredgecolor='black', markerfacecolor='C3')

    ax.plot(input_data['x'], input_data['y3'], color='r', linestyle='--', linewidth=1,
            marker='D', markersize=5,
            markeredgecolor='black', markerfacecolor='C2')

    ax.plot(input_data['x'], input_data['y4'], color='c', linestyle='--', linewidth=1,
            marker='d', markersize=5,
            markeredgecolor='black', markerfacecolor='C4')

    ax.plot(input_data['x'], input_data['y5'], color='k', linestyle='--', linewidth=1,
            marker='p', markersize=5,
            markeredgecolor='black', markerfacecolor='C6')

    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 13,
             }

    font3 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 12,
             }

    plt.title(input_data['str'], font2)
    plt.xlabel('The Number of Identities/Attributes n (Vector Length)', font3)
    plt.ylabel('Time Consumption (ms)', font2)

    ax.legend(labels=["ST", "GSB+", "DZQ+", 'MR-BPRE', 'VF-PPBA'], ncol=1, fontsize = 12)

    axins = inset_axes(ax, width="40%", height="30%", loc='lower left',
                       bbox_to_anchor=input_data['box2anchor'],
                       bbox_transform=ax.transAxes)

    axins.plot(input_data['x'], input_data['y1'], color='k', linestyle='--', linewidth=1,
               marker='o', markersize=5,
               markeredgecolor='black', markerfacecolor='C0')

    axins.plot(input_data['x'], input_data['y2'], color='g', linestyle='--', linewidth=1,
               marker='s', markersize=5,
               markeredgecolor='black', markerfacecolor='C3')

    axins.plot(input_data['x'], input_data['y3'], color='r', linestyle='--', linewidth=1,
               marker='D', markersize=5,
               markeredgecolor='black', markerfacecolor='C2')

    axins.plot(input_data['x'], input_data['y4'], color='c', linestyle='--', linewidth=1,
               marker='d', markersize=5,
               markeredgecolor='black', markerfacecolor='C4')

    axins.plot(input_data['x'], input_data['y5'], color='k', linestyle='--', linewidth=1,
               marker='p', markersize=5,
               markeredgecolor='black', markerfacecolor='C6')

    axins.set_xlim(input_data['boxs'][0], input_data['boxs'][1])
    axins.set_ylim(input_data['boxs'][2], input_data['boxs'][3])
    mark_inset(ax, axins, loc1=input_data['loc'][0], loc2=input_data['loc'][1], fc="none", ec='k', lw=1)

    # plt.show()
    plt.savefig(input_data['dir'])


if __name__ == "__main__":
    main()
