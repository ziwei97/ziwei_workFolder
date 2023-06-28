import matplotlib.pyplot as plt

# 设置 A4 纸的尺寸
width, height = 11.69,8.27  # 单位为英寸
dpi = 300  # 设置绘图的 DPI 值

# 创建画布
fig = plt.figure(figsize=(width, height), dpi=dpi)

# 绘制长方形
rectangle = plt.Rectangle((0, 0), width, height, facecolor=(1, 1, 1))

# 添加长方形到画布
ax = fig.add_subplot(111)
ax.add_patch(rectangle)

# 设置坐标轴范围和标签
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_xticks([])
ax.set_yticks([])

# 显示绘制结果
plt.show()
