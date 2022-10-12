mode = 'mode'
name = 'name'
game = 'game'
data = 'data'
pack = 'pack'
color = 'color'
point = 'point'
index = 'index'
shake = 'shake'
speed = 'speed'
count = 'count'
armed = 'armed'
empty = 'empty'
switch = 'switch'
bullet = 'bullet'  # 子弹
differ = 'differ'
turbo = 'turbo'
trigger = 'trigger'
restrain = 'restrain'
strength = 'strength'
positive = 'positive'  # 肯定的
negative = 'negative'  # 否定的

# 检测数据
detect = {
    "3440:1440": {
        game: [  # 判断是否在游戏中
            {
                point: (236, 1344),  # 点的坐标, 血条左上角
                color: 0x00FFFFFF  # 点的颜色, 255, 255, 255
            },
            {
                point: (2692, 1372),  # 生存物品右下角
                color: 0x959595  # 149, 149, 149
            }
        ],
        pack: {  # 背包状态, 有无武器, 选择的武器
            point: (2900, 1372),  # 两把武器时, 1号武器上面边框分界线的上半部分, y+1 就是1号武器上面边框分界线的下半部分
            color: 0x808080,  # 无武器时, 灰色, 128, 128, 128
            '0x447bb4': 1,  # 轻型弹药武器, 子弹类型: 1/2/3/4/5/6/None(无武器)
            '0x839b54': 2,  # 重型弹药武器
            '0x3da084': 3,  # 能量弹药武器
            '0xce5f6e': 4,  # 狙击弹药武器
            '0xf339b': 5,  # 霰弹枪弹药武器
            '0x5302ff': 6,  # 空投武器
        },
        mode: {  # 武器模式, 全自动/半自动/单发/其他
            color: 0x00FFFFFF,
            '1': (3151, 1347),  # 全自动
            '2': (3171, 1351),  # 半自动
        },
        armed: {  # 是否持有武器(比如有武器但用拳头就是未持有武器)

        },
        empty: {  # 是否空弹夹(武器里子弹数为0)
            color: 0x00FFFFFF,
            '1': (3204, 1306),  # 十位数, 该点白色即非0, 非0则一定不空
            '2': (3229, 1294),  # 个位数, 该点白色即为0, 十位为0且个位为0为空
        },
        name: {  # 武器名称判断
            color: 0x00FFFFFF,
            '1': {  # 1号武器
                '1': [  # 轻型弹药武器
                    (2959, 1386),  # 1: RE-45 自动手枪
                    (2970, 1385),  # 2: 转换者冲锋枪
                    (2972, 1386),  # 3: R-301 卡宾枪
                    (2976, 1386),  # 4: R-99 冲锋枪
                    (2980, 1386),  # 5: P2020 手枪
                    (2980, 1384),  # 6: 喷火轻机枪
                    (2987, 1387),  # 7: G7 侦查枪
                    (3015, 1386),  # 8: CAR (轻型弹药)
                ],
                '2': [  # 重型弹药武器
                    (2957, 1385),  # 1: 赫姆洛克突击步枪
                    (2982, 1385),  # 2: 猎兽冲锋枪
                    (2990, 1393),  # 3: 平行步枪
                    (3004, 1386),  # 4: 30-30
                    (3015, 1386),  # 5: CAR (重型弹药)
                ],
                '3': [  # 能量弹药武器
                    (2955, 1386),  # 1: L-STAR 能量机枪
                    (2970, 1384),  # 2: 三重式狙击枪
                    (2981, 1385),  # 3: 电能冲锋枪
                    (2986, 1384),  # 4: 专注轻机枪
                    (2980, 1384),  # 5: 哈沃克步枪
                ],
                '4': [  # 狙击弹药武器
                    (2969, 1395),  # 1: 哨兵狙击步枪
                    (2999, 1382),  # 2: 充能步枪
                    (2992, 1385),  # 3: 辅助手枪
                    (3016, 1383),  # 4: 长弓
                ],
                '5': [  # 霰弹枪弹药武器
                    (2957, 1384),  # 1: 和平捍卫者霰弹枪
                    (2995, 1382),  # 2: 莫桑比克
                    (3005, 1386),  # 3: EVA-8
                ],
                '6': [  # 空投武器
                    (2958, 1384),  # 1: 克雷贝尔狙击枪
                    (2959, 1384),  # 2: 手感卓越的刀刃
                    (2983, 1384),  # 3: 敖犬霰弹枪
                    (3003, 1383),  # 4: 波塞克
                    (3014, 1383),  # 5: 暴走
                ]
            },
            '2': {
                differ: 195  # 直接用1的坐标, 横坐标右移195就可以了
            }
        },
        turbo: {  # 涡轮
            color: 0x00FFFFFF,
            '3': {
                differ: 2,  # 有涡轮和没涡轮的索引偏移
                '4': (3072, 1358),  # 专注轻机枪 涡轮检测位置
                '5': (3034, 1358),  # 哈沃克步枪 涡轮检测位置
            }
        },
        trigger: {  # 双发扳机
            color: 0x00FFFFFF,
            '1': {
                differ: 2,
                '7': (3072, 1358),  # G7 侦查枪 双发扳机检测位置
            },
            '5': {
                differ: 1,
                '3': (3034, 1358),  # EVA-8 双发扳机检测位置
            }
        }
    },
    "2560:1440": {

    },
    "2560:1080": {

    },
    "1920:1080": {

    }
}

# 武器数据
weapon = {
    '1': {  # 轻型弹药武器
        '1': {
            name: 'RE-45 自动手枪',  # 全程往右飘
            shake: {
                speed: 80,
                count: 10,
                strength: 5,
            },
            restrain: [
                [1, -2, 10, 80],  #
                [1, -2, 10, 80],
                [1, -2, 10, 80],
                [1, -4, 10, 80],
                [1, -6, 10, 80],
                [1, -7, 8, 80],  #
                [1, -7, 8, 80],
                [1, -7, 8, 80],
                [1, -7, 8, 80],
                [1, -7, 8, 80],
                [1, -1, 5, 80],  #
                [1, -1, 5, 80],
                [1, -1, 5, 80],
                [1, -1, 5, 80],
                [1, -1, 5, 80],
                [1, -1, 5, 80],  #
                [1, -1, 3, 80],
                [1, -1, 3, 80],
                [1, -1, 3, 80],
                [1, -5, 3, 80],
                [1, -5, 3, 80],  #
                [1, -5, 3, 80],
                [1, -5, 3, 80],
                [1, -5, 3, 80],
                [1, -5, 3, 80],
            ]
        },
        '2': {
            name: '转换者冲锋枪',
            shake: {
                speed: 100,
                count: 10,
                strength: 7,
            },
            restrain: [
                [1, 0, 15, 94],
                [1, 0, 15, 94],
                [1, 0, 15, 94],
                [1, 0, 15, 94],
                [1, 0, 15, 94],  #
                [1, 0, 15, 94],
                [1, 0, 15, 94],
                [1, 0, 10, 94],
                [1, 0, 10, 94],
                [1, 0, 10, 94],  #
                [1, -5, 5, 94],
                [1, -5, 5, 94],
                [1, -5, 5, 94],
                [1, 0, 5, 94],
                [1, 0, 5, 94],  #
                [1, 0, 5, 94],
                [1, 5, 5, 94],
                [1, 5, 5, 94],
                [1, 5, 5, 94],
                [1, 0, 5, 94],  #
                [1, 0, 5, 94],
                [1, 0, 5, 94],
                [1, 0, 5, 94],
                [1, 0, 5, 94],
                [1, 0, 5, 94],  #
                [1, 0, 5, 94],
                [1, 0, 0, 94],
            ]
        },
        '3': {
            name: 'R-301 卡宾枪',
            shake: {
                speed: 64,  # 74ms打一发子弹
                count: 6,  # 压制前6发
                strength: 5,  # 压制的力度(下移的像素)
            },
            restrain: [
                [1, -5, 10, 70],
                [1, 0, 10, 70],
                [1, -5, 10, 70],
                [1, -2, 10, 70],
                [1, 0, 10, 70],  #
                [1, 0, 5, 70],
                [1, 0, 0, 70],
                [1, -5, 0, 70],
                [1, -5, 5, 70],
                [1, 0, 0, 70],  #
                [1, 0, 0, 70],
                [1, 5, 10, 70],
                [1, 5, 5, 70],
                [1, 5, 0, 70],
                [1, 5, 0, 70],  #
                [1, 0, 0, 70],
                [1, 5, 0, 70],
                [1, 5, 10, 70],
                [1, 0, 10, 70],
                [1, -5, 0, 70],  #
                [1, -5, 0, 70],
                [1, -5, 0, 70],
                [1, -5, 0, 70],
                [1, -5, 0, 70],
                [1, 0, 0, 70],  #
                [1, 0, 0, 70],
                [1, 0, 0, 70],
                [1, 0, 0, 64],
            ]
        },
        '4': {
            name: 'R-99 冲锋枪',
            shake: {
                speed: 55.5,
                count: 13,
                strength: 8,
            },
            restrain: [
                [1, 0, 10, 48],
                [1, 0, 10, 48],
                [1, 0, 10, 48],
                [1, -5, 10, 48],
                [1, -5, 10, 48],  #
                [1, -5, 10, 48],
                [1, -5, 10, 48],
                [1, 0, 10, 48],
                [1, 0, 10, 48],
                [1, 0, 10, 48],  #
                [1, 5, 10, 48],
                [1, 5, 10, 48],
                [1, 5, 10, 48],
                [1, 0, 10, 48],
                [1, 0, 0, 48],  #
                [1, -5, 0, 48],
                [1, -10, 0, 48],
                [1, 0, 0, 48],
                [1, 0, 0, 48],
                [1, 5, 5, 48],  #
                [1, 10, 5, 48],
                [1, 10, 5, 48],
                [1, 5, 0, 48],
                [1, 0, 0, 48],
                [1, -5, 0, 48],  #
                [1, -5, 0, 48],
                [1, -5, 0, 48],
            ]
        },
        '5': {
            name: 'P2020 手枪',
            restrain: [
                [2, 1, 100],
            ]
        },
        '6': {
            name: '喷火轻机枪',
            shake: {
                speed: 110,
                count: 8,
                strength: 5,
            },
            restrain: [
                [1, 0, 20, 100],
                [1, 5, 15, 100],
                [1, 5, 15, 100],
                [1, 5, 15, 100],
                [1, 5, 10, 100],  #
                [1, 5, 10, 100],
                [1, -5, 10, 100],
                [1, -5, 0, 100],
                [1, -5, 0, 100],
                [1, -5, 0, 100],  #
                [1, 0, 0, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 5, 5, 100],
                [1, 10, 5, 100],  #
                [1, 10, 5, 100],
                [1, 5, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],  # 20
                [1, 0, 0, 100],
                [1, 0, 0, 100],
                [1, 0, 0, 100],
                [1, 0, 0, 100],
                [1, -5, 5, 100],  #
                [1, -5, 5, 100],
                [1, -5, 5, 100],
                [1, -5, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],  #
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],  #
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],  #
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],  #
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 5, 100],
                [1, 0, 0, 100],  #
            ]
        },
        '7': {
            name: 'G7 侦查枪',
        },
        '8': {
            name: 'CAR (轻型弹药)',
            shake: {
                speed: 64.5,
                count: 10,
                strength: 7,
            },
            restrain: [
                [1, 0, 10, 58],  #
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, 3, 10, 58],  #
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, -5, 10, 58],
                [1, -5, 10, 58],
                [1, -5, 5, 58],  #
                [1, -5, 10, 58],
                [1, -5, 0, 58],
                [1, 0, 0, 58],
                [1, 5, 0, 58],
                [1, 5, 3, 58],  #
                [1, 5, 3, 58],
                [1, -5, 3, 58],
                [1, -5, 3, 58],
                [1, -5, 3, 58],
                [1, 0, 0, 58],  #
                [1, 0, 0, 58],
                [1, 0, 0, 58],
                [1, 0, 3, 58],
                [1, 0, 3, 58],
                [1, 0, 3, 58],  #
                [1, 0, 3, 58],
            ]
        },
        '9': {
            name: 'G7 侦查枪 (双发扳机)',
            restrain: [
                [1, 0, 5, 20],
                [1, 0, 1, 0]
            ]
        },
    },
    '2': {  # 重型弹药武器
        '1': {
            name: '赫姆洛克突击步枪',
            shake: {
                speed: 50,
                count: 3,
                strength: 6,
            }
        },
        '2': {
            name: '猎兽冲锋枪',
            shake: {
                speed: 50,
                count: 5,
                strength: 6,
            }
        },
        '3': {
            name: '平行步枪',
            shake: {
                speed: 100,
                count: 5,
                strength: 5,
            },
            restrain: [
                [1, 0, 10, 100],  #
                [1, 5, 10, 100],
                [1, 5, 10, 100],
                [1, 5, 10, 100],
                [1, 5, 10, 100],
                [1, -5, 10, 100],  #
                [1, -5, 0, 100],
                [1, -5, 0, 100],
                [1, -5, 0, 100],
                [1, 0, 5, 100],
                [1, 5, 5, 100],  #
                [1, 5, 5, 100],
                [1, 5, 0, 100],
                [1, 5, 0, 100],
                [1, 0, 0, 100],
                [1, 5, 5, 100],  #
                [1, 5, 5, 100],
                [1, 5, 5, 100],
                [1, 0, 0, 100],
                [1, 0, 0, 100],
                [1, -5, 5, 100],  #
                [1, -5, 5, 100],
                [1, -5, 5, 100],
                [1, -0, 5, 100],
                [1, 5, 5, 100],
                [1, 5, 5, 100],  #
                [1, 5, 5, 100],
                [1, -5, -5, 100],
                [1, -5, 5, 100],
                [1, -5, 5, 100],
            ]
        },
        '4': {
            name: '30-30',
        },
        '5': {
            name: 'CAR (重型弹药)',
            shake: {
                speed: 58,
                count: 10,
                strength: 7,
            },
            restrain: [
                [1, 0, 10, 58],  #
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, 3, 10, 58],  #
                [1, 3, 10, 58],
                [1, 3, 10, 58],
                [1, -5, 10, 58],
                [1, -5, 10, 58],
                [1, -5, 5, 58],  #
                [1, -5, 10, 58],
                [1, -5, 0, 58],
                [1, 0, 0, 58],
                [1, 5, 0, 58],
                [1, 5, 3, 58],  #
                [1, 5, 3, 58],
                [1, -5, 3, 58],
                [1, -5, 3, 58],
                [1, -5, 3, 58],
                [1, 0, 0, 58],  #
                [1, 0, 0, 58],
                [1, 0, 0, 58],
                [1, 0, 3, 58],
                [1, 0, 3, 58],
                [1, 0, 3, 58],  #
                [1, 0, 3, 58],
            ]
        }
    },
    '3': {  # 能量弹药武器
        '1': {
            name: 'L-STAR 能量机枪',
            shake: {
                speed: 100,
                count: 10,
                strength: 5,
            },
            restrain: [
                [1, 12, 10, 100],
                [1, 12, 10, 100],
                [1, 10, 10, 100],
                [1, 0, 10, 100],
                [1, -10, 10, 100],  #
                [1, -10, 10, 100],
                [1, -10, 10, 100],
                [1, -10, 10, 100],
                [1, 0, 10, 100],
                [1, 0, 10, 100],  #
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],  #
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],  #
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],  #
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],
                [1, 0, 8, 100],  #
            ]
        },
        '2': {
            name: '三重式狙击枪',
        },
        '3': {
            name: '电能冲锋枪',
            shake: {
                speed: 83.3,
                count: 10,
                strength: 7,
            },
            restrain: [
                [1, -5, 15, 80],
                [1, 0, 15, 80],
                [1, 0, 15, 80],
                [1, 0, 15, 80],
                [1, 0, 15, 80],  #
                [1, -5, 10, 80],
                [1, -5, 10, 80],
                [1, -5, 10, 80],
                [1, 0, 10, 80],
                [1, 5, 10, 80],  #
                [1, 5, 5, 80],
                [1, 5, 5, 80],
                [1, 5, 5, 80],
                [1, 0, 5, 80],
                [1, 0, 5, 80],  #
                [1, 0, 5, 80],
                [1, 0, 0, 80],
                [1, 0, 0, 80],
                [1, 0, 0, 80],
                [1, 0, 0, 80],  #
                [1, 0, 0, 80],
                [1, 5, 0, 80],
                [1, 5, 0, 80],
                [1, 5, 0, 80],
                [1, 0, 0, 80],  #
                [1, 0, 0, 80],
            ]
        },
        '4': {
            name: '专注轻机枪',
            shake: {
                speed: 100,
                count: 10,
                strength: 7,
            }
        },
        '5': {
            name: '哈沃克步枪',
            shake: {
                speed: 100,
                count: 8,
                strength: 6,
            },
            restrain: [
                [1, 0, 0, 400],  # 延迟
                [1, -5, 10, 88],  # 1
                [1, -5, 15, 88],
                [1, 0, 15, 88],
                [1, 0, 15, 88],
                [1, 0, 15, 88],
                [1, 5, 10, 88],  #
                [1, 5, 10, 88],
                [1, 5, 10, 88],
                [1, 5, 10, 88],
                [1, -5, 5, 88],
                [1, -5, 0, 88],  # 1
                [1, -5, 0, 88],
                [1, -10, 0, 88],
                [1, -10, 0, 88],
                [1, -5, 0, 88],
                [1, 0, 5, 88],  #
                [1, 10, 5, 88],
                [1, 10, 5, 88],
                [1, 0, 0, 88],
                [1, 0, 0, 88],
                [1, 5, 10, 88],  # 1
                [1, 5, 10, 88],
                [1, 0, 10, 88],
                [1, 5, 10, 88],
                [1, 5, 10, 88],
                [1, 5, 10, 88],  #
                [1, 5, 5, 88],
                [1, 5, 5, 88],
                [1, 0, 5, 88],
                [1, 0, 0, 88],
                [1, 0, 0, 88],  # 1
                [1, 0, 0, 88],
                [1, 0, 5, 88],
                [1, 0, 5, 88],
                [1, 0, 5, 88],
                [1, 0, 5, 88],  #
            ]
        },
        '6': {
            name: '专注轻机枪 (涡轮)',
            shake: {
                speed: 100,
                count: 10,
                strength: 7,
            }
        },
        '7': {
            name: '哈沃克步枪 (涡轮)',
            shake: {
                speed: 100,
                count: 8,
                strength: 6,
            },
            restrain: [
                [1, -5, 10, 88],  # 1
                [1, -5, 15, 88],
                [1, 0, 15, 88],
                [1, 0, 15, 88],
                [1, 0, 15, 88],
                [1, 5, 10, 88],  #
                [1, 5, 10, 88],
                [1, 5, 10, 88],
                [1, 5, 10, 88],
                [1, -5, 5, 88],
                [1, -5, 0, 88],  # 1
                [1, -5, 0, 88],
                [1, -10, 0, 88],
                [1, -10, 0, 88],
                [1, -5, 0, 88],
                [1, 0, 5, 88],  #
                [1, 10, 5, 88],
                [1, 10, 5, 88],
                [1, 0, 0, 88],
                [1, 0, 0, 88],
                [1, 5, 10, 88],  # 1
                [1, 5, 10, 88],
                [1, 0, 10, 88],
                [1, 5, 10, 88],
                [1, 5, 10, 88],
                [1, 5, 10, 88],  #
                [1, 5, 5, 88],
                [1, 5, 5, 88],
                [1, 0, 5, 88],
                [1, 0, 0, 88],
                [1, 0, 0, 88],  # 1
                [1, 0, 0, 88],
                [1, 0, 5, 88],
                [1, 0, 5, 88],
                [1, 0, 5, 88],
                [1, 0, 5, 88],  #
            ]
        },
    },
    '4': {  # 狙击弹药武器
        '1': {
            name: '哨兵狙击步枪',
        },
        '2': {
            name: '充能步枪',
        },
        '3': {
            name: '辅助手枪',
        },
        '4': {
            name: '长弓',
        },
    },
    '5': {  # 霰弹弹药武器
        '1': {
            name: '和平捍卫者霰弹枪',
        },
        '2': {
            name: '莫桑比克',
        },
        '3': {
            name: 'EVA-8',
        },
        '4': {
            name: 'EVA-8 (双发扳机)',
        }
    },
    '6': {  # 空投武器
        '1': {
            name: '克雷贝尔狙击枪',
        },
        '2': {
            name: '手感卓越的刀刃',
        },
        '3': {
            name: '敖犬霰弹枪',
        },
        '4': {
            name: '波塞克',
        },
        '5': {
            name: '暴走',
            shake: {
                speed: 200,
                count: 8,
                strength: 2,
            }
        },
    }
}
