
# 说明

通过监听键鼠来触发武器自动识别, 将自动识别武器和加载压枪数据的操作分散在常规操作中. 按下左键开火时, 执行对应的压枪数据

功能说明
- 已完成项: 全自动, 武器名称识别, 射击模式识别, 剩余弹药识别, 部分配件识别, 游戏内键鼠操作, 自动识别与压枪主循环逻辑, 压枪顺滑平稳不抖动
- 未完成项
  - 检测是否持枪, 这个通过游戏界面无法判断, 暂时不考虑. 没有这个判断则可能出现在不该压枪时执行压枪的情况
  - 单发武器变自动连发, 如P2020这把手枪, 我希望能实现按下左键时能不停触发左键点击的效果, 让其变成全自动, 但是还未实现

数据说明, 可自行精修
- 压枪数据都是简单调了下, 并没有精修, 大多处于将就能用的水平, R301 的数据相对来说算是比较准的了, 当然距离一条线还差得远
- 专注因为射击间隔不稳定, 所以暂时没有测, 也就没有对应的压枪数据
- 暴走也没有数据, 因为以前暴走用的是抖枪术, 这次也懒得再测了, 需要的自己测测, 大致能用就行

按键说明, 可自行修改适合自己的键位
- 结束程序: End
- 开关切换: 鼠标侧上键
- 武器识别: 鼠标右键按下/1/2/E/Tab

适配说明, 目前仅适配了 3440×1440 分辨率下无边框窗口模式, 其他分辨率可自行适配

源码说明
- logitech.driver.dll: 大佬封装的可以直接调用罗技驱动的库
- cfg.py: 数据, 包括检测数据和武器数据
- toolkit.py: 工具包, 包括截图工具, 屏幕工具, 游戏内检测功能封装等
- apex.py: 自动识别与压枪主程序
  - 参数: ads: 基本可以认为是游戏内的鼠标灵敏度, 通过调整该参数并测试效果, 在压枪效果达到最好时, ads 值就是合适的值

# 环境准备

```shell
conda create -n apex python=3.9.13  # 3.9.15, ctypes.CDLL 不能使用相对路径, 什么玩意儿
conda remove -n apex --all
conda install pywin32  # pip 的能用但有红线
pip install -r requitements.txt
pip install mss pynput pywin32 pyinstaller python-opencv
```

## 操纵键鼠

大多FPS游戏都屏蔽了操作鼠标的Win函数, 要想在游戏中用代码操作鼠标, 需要一些特殊的办法, 其中罗技驱动算是最简单方便的了

代码直接控制罗技驱动向操作系统(游戏)发送鼠标命令, 达到了模拟鼠标操作的效果, 这种方式是鼠标无关的, 任何鼠标都可以实现

我们不会直接调用罗技驱动, 但是有大佬已经搭过桥了, 有现成的调用驱动的dll, 只是需要安装指定版本的罗技驱动配合才行

### 驱动安装和系统设置

> [百度网盘 罗技键鼠驱动](https://pan.baidu.com/s/1VkE2FQrNEOOkW6tCOLZ-kw?pwd=yh3s)

罗技驱动分 LGS (老) 和 GHub (新), LGS 的话, 需要使用 9.02.65 版本的, GHub 的话, 需要使用 2021.11 之前的, 二者自选其一即可

装好驱动后, 无需重启电脑. hosts 文件添加 `127.0.0.1 updates.ghub.logitechg.com` 防止更新. 在 hosts 文件 右键-属性-安全 里给当前用户授予完全访问权限后, 就可以修改保存了

另外需要确保 控制面板-鼠标-指针选项 中下面两个设置
- 提高指针精确度 选项去掉, 不然会造成实际移动距离变大
- 选择指针移动速度 要在正中间, 靠右会导致实际移动距离过大, 靠左会导致指针移动距离过小

### 代码

大佬封装的 `logitech.driver.dll` 没有文档, 下面是某老哥列出的该库里面的方法, 具体用法参考 `测试.罗技.py`

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/20221204.131618.213.png)

## 键鼠监听

> [Pynput 说明](https://pypi.org/project/pynput/)

注意调试回调方法的时候, 不要打断点, 不然会卡死IO, 导致鼠标键盘失效

回调方法如果返回 False, 监听线程就会自动结束, 所以不要随便返回 False

键盘的特殊按键采用 `keyboard.Key.tab` 这种写法，普通按键用 `keyboard.KeyCode.from_char('c')` 这种写法, 有些键不知道该怎么写, 可以 `print(key)` 查看信息

> 钩子函数本身是阻塞的。也就是说钩子函数在执行的过程中，用户正常的键盘/鼠标操作是无法输入的。所以在钩子函数里面必须写成有限的操作（即O(1)时间复杂度的代码），也就是说像背包内配件及枪械识别，还有下文会讲到的鼠标压枪这类时间开销比较大或者持续时间长的操作，都不适合写在钩子函数里面。这也解释了为什么在检测到Tab（打开背包）、鼠标左键按下时，为什么只是改变信号量，然后把这些任务丢给别的进程去做的原因。

# 核心逻辑

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/33b6e9800ab06923ab0ebd36dc12f9cd_07fb8b78dafd413e9b42740b7bf0b7c9.png)

## 是否在游戏内

获取顶层窗口标题, 判断其名称是否包含 [Apex Legends] 字符

## 是否在对局中

找几个只有在对战中才会存在的特征点取色判断, 如血条左上角和生存物品框左下角

Pubg 的 UI 大部分都是透明的, 点的颜色会受到背景的干扰. Apex 的 UI 有很多地方都是稳定且固定的颜色, 取色判断法会很方便

## 获取武器索引 无武器/一号武器/二号武器

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/8b61e8800704303f84fdaff0d4ca1443_f996d5e517b54f1b9292e76c6447d50a.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/8f2b618171de7c49e00775404d2b1f04_84a13f65b07343deb5f9fd4be2f4bb6c.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/08544682aebd95723453033db62e4c6a_369ff03d5009485fa5d4fbf268b7d02e.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/312031ed08fee89c73bfe3e76ab3e91b_0605638c35ba470e90d93e10d79f2884.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/e941129fb3646482995cde4c33ee51ec_1040d8042c0645d9a165fc10db5bc769.png)

假设白线交点是 A, 交点下移一个像素是 B, 则有如下结论
- A 是灰色: 没有武器
- A 与 B 同色: 当前激活了一号武器
- A 与 B 异色: 当前激活了二号武器

## 识别武器名称 纯白点计数法

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/和平.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/R301.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/平行.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/滋崩.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/哈沃克.png)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/克雷贝尔.png)

需要先获取到武器索引, 如果是无武器不识别名称, 如果是一号二号则需要截取对应位置的名称图片, 做进一步识别

武器名称上纯白色点的个数是有限且固定的, 提前截图并统计好所有武器的纯白色点个数, 识别时一对比就能判断当前武器名称了

即使出现武器名称截图中纯白点个数相同的情况, 只需在有冲突的武器名称上找一个纯白点, 确保该点在其他冲突武器上不是纯白, 以此区分即可

## 如何判断武器模式 全自动/连发/单发

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/img.png)

需要压枪的只有全自动和半自动两种模式的武器, 单发不需要压枪(想把单发武器做成自动连发), 喷子和狙不需要压枪

所以需要找一个能区分三种模式的稳定点, 且这个点不能受和平和三重的特殊标记影响

找不到的话, 退而求其次, 找三个能区分这三种模式的点, 遍历判断也将就能用

## 判断弹夹是否打空

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/82a519f523e1b530a68ec0d6a7868fa0_25b3c3ef8f3c45c88509e9112b789033.png)

弹夹中子弹数大多为两位数, 所以只需确认十位不为0, 即可认为不空, 十位为0且个位为0, 即可认为空
- 十位的点, 在数字正中间即可, 1-9都是纯白色, 0是灰色. 注意, 这个灰色不是固定颜色, 会随着背景改变而改变
- 个位的点, 在数字0中间斜线的最左端, 这个点是纯白色, 且其他1-9时, 这个点都不是纯白色

L-STAR 这把枪弹夹机制和其他枪不一样, 这里不考虑

## 判断配件是否存在 涡轮/双发扳机/火力全开状态(暴雷)

![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/1670138745397109000.jpg)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/1670138766440992600.jpg)
![](https://github.com/mrathena/python.apex.weapon.auto.recognize.and.suppress/blob/master/readme/1670138852349917400.jpg)

部分武器的射击间隔或激发模式受到某些武器配件的影响, 先根据识别到的武器名称判断是否需要进行配件检测, 需要的话再到对应位置看下配件是否存在即可, 配件上有固定的纯白色点

## 判断是否持有武器

暂无法判断, 持有武器和收起武器和持有投掷物求生物品等情况, 没有能明确区分的办法

## 按键逻辑

- 结束程序, End键释放
- 切换开关, 鼠标侧上键按下
- 识别武器
  - 鼠标右键按下时(瞄准模式). 和游戏内原本的按键功能不冲突
  - 1(切换一号武器) / 2(切换二号武器) E(交互/更换武器) / Tab(关闭背包) 键释放时

识别武器涉及截图和数次屏幕取点操作, 耗时相对比较长(60毫秒左右), 不应该放在键鼠监听的钩子函数内, 否则可能在游戏中感觉到键鼠卡顿. 通常只在钩子函数内触发信号量改变, 在其他进程中完成识别流程

# 调整压枪参数

参考源码中的 `测试.武器射击间隔.py` 先测出武器的射击间隔(毫秒). 

具体就是, 通过假设一个射击间隔, 并逐渐调整这个值, 直到弹夹打空正好发生大幅位移, 这个值基本就差不多了. 然后到代码中测试, 看子弹打完时日志是否正好打印到最后一颗子弹

调鼠标参数时, 先调纵向再调横向, 按顺序逐个调, 因为前面的一个变动, 对后面的影响可能户非常大, 很可能导致下面的白调了

也可以找一些压枪宏, 直接抽出其中的武器压枪数据来用

# 依赖

```
mss
pynput
pywin32
pyinstaller
opencv-python
```

# 打包

```
pyinstaller apex.py -p cfg.py -p toolkit.py -p mouse.device.lgs.dll
-F: 打包成一个 exe 文件
-w: 运行不显示黑框
```

# 扩展

## Python Pubg 武器自动识别与压枪

> [GitHub python.pubg.weapon.auto.recognize.and.suppress](https://github.com/mrathena/python.pubg.weapon.auto.recognize.and.suppress)

## 拓展 目标检测 与 自瞄, 彻底告别压枪

> [CSDN Python Apex YOLO V5 6.2 目标检测与自瞄 全过程记录](https://blog.csdn.net/mrathena/article/details/126860226)

因为没有计算机视觉相关方向的专业知识, 所以做出来的东西, 有一定效果, 但是还有很多不足

不同的游戏, 都需要准备大量精准的数据集做训练, 才能取得比较好的效果

# 拓展 通用型人体骨骼检测 与 自瞄, 训练一次, FPS 游戏通用

> [【亦】警惕AI外挂！我写了一个枪枪爆头的视觉AI，又亲手“杀死”了它](https://www.bilibili.com/video/BV1Lq4y1M7E2/)

> [YOLO V7 keypoint 人体关键点检测](https://xugaoxiang.com/2022/07/21/yolov7/)

大多数 FPS 游戏中要检测的目标都为人形, 可以训练一个 通用型人体骨骼检测模型, 在类似游戏中应该有不错的效果
