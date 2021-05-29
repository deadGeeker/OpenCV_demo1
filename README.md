# 前期准备：
---
### 安装将要用到的模块
+ + sudo -H python3 -m pip install opencv-python==4.2.0.34 numpy==1.18.5
### 在 IPython 中运行下面命令读取两张图片
+ + %run args.py --image images/pepper.jpg --image images/cup.jpg

---

# 使用边缘检测算子检测出图片中的边缘
---
+ + -将彩色图片转换为灰度图
+ + -使用 cv2.canny 函数检测出图片中的边缘
+ + edge = cv2.Canny(cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY), 60, 150)
+ + cv2.imwrite("edge.jpg", edge)
---

# 使用 cv2.findContours 来找出图片中的轮廓
---
+ + -cv2.findContours 有两个返回值 contours 和 h。
+ + -contours 是一个列表，其中每一个元素对应检测到的轮廓，
+ + -另一个 h 表示检测到的轮廓所对应的属性
+ + contours, h = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
---

# 使用 copy 方法拷贝一个 image1 的副本，因为绘图操作会修改图片
---
+ + drawc = image1.copy()
---

# 使用 cv2.drawContours 函数进行绘图
---
+ + drawc = cv2.drawContours(drawc, contours, -1, (255, 0, 0), 2)
+ + cv2.imwrite("contour.jpg", drawc)
---


# 分割物体
---
+ + -使用 np.zeros 创建一个尺寸和通道数同原始图片一样的黑色图片 mask
+ + mask = np.zeros(image1.shape, dtype = "uint8")

+ + -使用 cv2.drawContours 在 mask 上绘制我们检测到的轮廓
+ + mask = cv2.drawContours(mask, contours, 1, (255,255,255), -1)
+ + cv2.imwrite("mask.jpg", mask)

+ + -使用按位运算对原始图片和 mask 进行 and 操作
+ + divide = cv2.bitwise_and(mask, image1)
+ + cv2.imwrite("divide.jpg", divide)
---

# 裁剪和图片合并
---
+ + -从 divide 中裁剪出辣椒
+ + -使用 cv2.boundingRect 函数获得这个辣椒最小的外接矩形的坐标
+ + (x, y, w, h) = cv2.boundingRect(contours[1])

+ + -知道了坐标就可以使用切片方法裁剪出这个辣椒
+ + cut_pepper = divide[y:y + h, x:x + w]
+ + cv2.imwrite("cutpepper.jpg", cut_pepper)

+ + -同样使用切片方法将 mask 上绘制的轮廓裁剪下来
+ + cut_mask = mask[y:y + h, x:x + w]
+ + cv2.imwrite("cut_mask.jpg", cut_mask)

+ + -使用按位 not 运算将被白色填充的轮廓区域变成黑色，将其他区域变成白色
+ + cut_not = cv2.bitwise_not(cut_mask)
+ + cv2.imwrite("cut_not.jpg", cut_not)

+ + -将裁剪出来的辣椒合并到其他图片中，
+ + -首先在读取的第二张图片中使用切片方法选择一个尺寸
+ + -和裁剪下来的辣椒图片的尺寸一样的区域
+ + cut_image2 = image2[50:50 + h, 50:50 + w]
+ + cv2.imwrite("cut_image2.jpg", cut_image2)

+ + -将裁剪出来的区域和 cut_not 进行按位 and 操作
+ + cut_image2 = cv2.bitwise_and(cut_not, cut_image2)
+ + cv2.imwrite("cut_image2.jpg", cut_image2)

+ + -将 cut_image2 与 cut_pepper 进行按位 or 运算
+ + cut_image2 = cv2.bitwise_or(cut_pepper, cut_image2)
+ + cv2.imwrite("cut_image2.jpg", cut_image2)

+ + -将操作后的区域用切片方法替换原始图像的区域，最后保存图片
+ + image2[50:50 + h, 50:50 + w] = cut_image2[:,:]
+ + cv2.imwrite("merge.jpg", image2)
---
