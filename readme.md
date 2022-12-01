
### 链接

[CSDN Python Pubg 武器自动识别与压枪 全过程记录](https://blog.csdn.net/mrathena/article/details/128129079)

[CSDN Python Apex 武器自动识别与压枪 全过程记录](https://blog.csdn.net/mrathena/article/details/126918389)

[CSDN Python Apex YOLO V5 6.2 目标检测 全过程记录](https://blog.csdn.net/mrathena/article/details/126860226)

[百度网盘 罗技键鼠驱动](https://pan.baidu.com/s/1VkE2FQrNEOOkW6tCOLZ-kw?pwd=yh3s)

### 说明

半成品

已完成项: 背包识别, 武器识别, 配件识别, 射击模式识别, 角色姿态识别, 剩余弹药识别, 游戏内键鼠操作, 自动识别与压枪主循环逻辑

未完成项: 自动识别当前激活的主武器, 是1号还是2号, 可以稍微修改下主逻辑, 用按1/2手动指定激活武器来代替自动识别

适配了 3440×1440 分辨率

压枪数据来自于 [GitHub PUBGRecognizeAndGunpress](https://github.com/Cjy-CN/PUBGRecognizeAndGunpress), 没有做精修(其实是不会), 勉强能用, 可调整初始化参数中的 ADS 来修改基准倍率

### 依赖

```
mss
pywin32
pynput
pyinstaller
opencv-python
```

### 打包

```
pyinstaller pubg.py -p cfg.py -p structure.py -p toolkit.py -p mouse.device.lgs.dll
-F: 打包成一个 exe 文件
-w: 运行不显示黑框
```
