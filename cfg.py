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
switch = 'switch'
bullet = 'bullet'  # 子弹
differ = 'differ'
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
                    (2955, 1386),  # 1: L-STAR能量机枪
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
                    (2983, 1384),  # 2: 敖犬霰弹枪
                    (3003, 1383),  # 3: 波塞克
                    (3014, 1383),  # 4: 暴走
                ]
            },
            '2': {
                differ: 195  # 直接用1的坐标, 横坐标右移195就可以了
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
            }
        },
        '2': {
            name: '转换者冲锋枪',
            shake: {
                speed: 100,
                count: 10,
                strength: 7,
            }
        },
        '3': {
            name: 'R-301 卡宾枪',
            shake: {
                speed: 74,  # 74ms打一发子弹
                count: 6,  # 压制前6发
                strength: 5,  # 压制的力度(下移的像素)
            },
            restrain: {
                speed: 74,

            }
        },
        '4': {
            name: 'R-99 冲锋枪',
            shake: {
                speed: 55.5,
                count: 13,
                strength: 8,
            }
        },
        '5': {
            name: 'P2020 手枪',
        },
        '6': {
            name: '喷火轻机枪',
            shake: {
                speed: 111,
                count: 8,
                strength: 5,
            }
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
            }
        }
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
            }
        },
        '4': {
            name: '30-30',
        },
        '5': {
            name: 'CAR (重型弹药)',
            shake: {
                speed: 64.5,
                count: 10,
                strength: 7,
            }
        }
    },
    '3': {  # 能量弹药武器
        '1': {
            name: 'L-STAR能量机枪',
            shake: {
                speed: 100,
                count: 10,
                strength: 5,
            }
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
            }
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
            }
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
    },
    '6': {  # 空投武器
        '1': {
            name: '克雷贝尔狙击枪',
        },
        '2': {
            name: '敖犬霰弹枪',
        },
        '3': {
            name: '波塞克',
        },
        '4': {
            name: '暴走',
            shake: {
                speed: 200,
                count: 8,
                strength: 2,
            }
        },
    }
}
