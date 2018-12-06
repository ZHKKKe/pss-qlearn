import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


FILE_NAME = 'record.txt'
SMOOTH_EPISODE = 1000

if __name__ == '__main__':
    plt.clf()
    plt.xlabel('eposide')
    plt.ylabel('score')
    plt.xlim(-1000, 11000)
    plt.ylim(-100, 2000)
    plt.grid(True)
    with open(FILE_NAME, 'r') as f:
        content = f.readlines()

    x = []
    y = []
    means = []
    tmp_value = []
    mean_idx = 0
    idx = 0
    for c in content:
        if idx > 10000:
            break
        idx += 1
        c_list = c.split(' ')
        x.append(c_list[0])
        yvalue = int(c_list[1].split('\n')[0])
        y.append(yvalue)

        tmp_value.append(yvalue)
        mean_idx += 1

        if (mean_idx % SMOOTH_EPISODE == 0 and mean_idx != 0) or mean_idx == (len(content) - 1):
            means.append(np.mean(tmp_value))
            tmp_value = []
    

    mean_x_idx = [_ * SMOOTH_EPISODE for _ in range(1, len(means) + 1)]
    plt.plot(mean_x_idx, means, c='#F39019', linewidth='3')
    plt.scatter(x, y, c='#51A7F9', marker='o', s=15, alpha=0.9)
    plt.savefig(FILE_NAME.split('.')[0] + '.pdf', format='pdf', bbox_inches='tight')

    plt.show()
    plt.close()
