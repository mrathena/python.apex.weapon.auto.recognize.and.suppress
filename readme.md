
# 链接

[CSDN Python Apex 武器自动识别与压枪 全过程记录](https://blog.csdn.net/mrathena/article/details/126918389)

[CSDN Python Apex YOLO V5 6.2 目标检测 全过程记录](https://blog.csdn.net/mrathena/article/details/126860226)

[CSDN Python Pubg 武器自动识别与压枪 全过程记录](https://blog.csdn.net/mrathena/article/details/128129079)

[百度网盘 罗技键鼠驱动](https://pan.baidu.com/s/1VkE2FQrNEOOkW6tCOLZ-kw?pwd=yh3s)

# 说明

已完成项: 武器激活识别, 武器名称识别, 射击模式识别, 剩余弹药识别, 部分配件识别, 游戏内键鼠操作, 自动识别与压枪主循环逻辑, 压枪平稳不抖动

未完成项: 检测是否具持枪, 这个通过游戏界面无法判断

适配了 3440×1440 分辨率

并没有考虑配件对压枪的影响(好像也没什么影响), 压枪数据也都是大概调了下, 将就能用的水平

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
