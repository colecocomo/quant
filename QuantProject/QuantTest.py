# -*- coding: utf-8 -*-
"""
Created on Mar. 12 11:15:39 2018

@author: cole
"""

import numpy as np
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

"""
simple advanced plot
"""
# 生成测试数据
x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
y_cos, y_sin = np.cos(x), np.sin(x)

# 生成画布, 并设定标题
plt.figure(figsize=(8, 6), dpi=80)
plt.title("curve")
plt.grid(True)

# 画图的另外一种方式
ax_1 = plt.subplot(111)
ax_1.plot(x, y_cos, color="blue", linewidth=2.0, linestyle="--", label="left cos")
ax_1.legend(loc="upper left", shadow=True)

# 设置Y轴(左边)
ax_1.set_ylabel("left cos y")
ax_1.set_ylim(-1.0, 1.0)
ax_1.set_yticks(np.linspace(-1, 1, 9, endpoint=True))

# 画图的另外一种方式
ax_2 = ax_1.twinx()
ax_2.plot(x, y_sin, color="green", linewidth=2.0, linestyle="-", label="right sin")
ax_2.legend(loc="upper right", shadow=True)

# 设置Y轴(右边)
ax_2.set_ylabel("right sin y")
ax_2.set_ylim(-2.0, 2.0)
ax_2.set_yticks(np.linspace(-2, 2, 9, endpoint=True))

# 设置X轴(共同)
ax_1.set_xlabel("x")
ax_1.set_xlim(-4.0, 4.0)
ax_1.set_xticks(np.linspace(-4, 4, 9, endpoint=True))

# 图形显示
plt.show()


