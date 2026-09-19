# DxAnim 单位动画运行时链

本页记录 2026-09-19 已由反汇编和 A0A/B1A 原始字节黄金样例固定的结论。完整容器字段见
[`docs/formats.md`](../formats.md) §10。

## 解码链

1. 块0～3都是动画程序表，每条指令固定10字节，首字节低两位为 opcode。
2. opcode0 的 bytes2..5 保存四个描述符低8位，bytes6..7 的四个半字节保存对应高4位；
   `0xfff` 表示空层，bytes8..9 是该画面的持续 tick。
3. 描述符索引块4的10字节记录，得到最终 BMP 帧、局部 x/y、原始绘制属性和 draw group。
4. opcode1 创建块3子动画；子实例继承镜像并累积偏移，与父实例在同一 tick 绘制。
5. opcode2 的音效副作用在离线导出时跳过；opcode3 保留重复次数、跳转方向和终止语义。

导出器将解释结果压缩为：

```json
{
  "id": 11,
  "loop_from": 0,
  "steps": [{
    "duration_ticks": 8,
    "layers": [{
      "frame": 244,
      "x": 0,
      "y": -40,
      "flip_x": false,
      "flip_y": false,
      "descriptor": 569
    }]
  }]
}
```

`layers` 已按原版绘制调用顺序排列。官方资源使用 schema v2；Godot 读取器仍接受旧
`{frame,dur}` 单层记录，供既有 Mod 过渡。

## 移动动作与八方向

移动调用方传入动作号 `no=3`。表项的动画号直接对应块0 #11～#15；第二字节低两位是
水平/垂直镜像标志，不是块号，也不存在旧文档中的“动画号 +5”。
原版角度查表 `0x618D80/0x618DA4` 固定了罗盘关系：0° 为 d6/E，之后每45°依次为
d3/SE、d2/S、d1/SW、d4/W、d7/NW、d8/N、d9/NE；d5 是中心位。

| 罗盘方向 | 原版 dir | 块0动画 | flags |
|---|---:|---:|---:|
| W | 4 | 13 | 0 |
| E | 6 | 13 | 1（水平镜像） |
| NW | 7 | 12 | 0 |
| NE | 9 | 12 | 1（水平镜像） |
| S | 2 | 15 | 0 |
| N | 8 | 11 | 0 |
| SW | 1 | 14 | 0 |
| SE | 3 | 14 | 1（水平镜像） |

## 黄金样例

- A0A #11～#15 最终帧：`244..249`、`238..243`、`232..237`、`226..231`、`220..225`。
- B1A #11～#15 最终帧：`224..229`、`218..223`、`212..217`、`206..211`、`200..205`。
- 01E #21：最终时间线包含父层 40/41 与紫色斩击层 4/5 的并发画面。
- 01E #28：最终帧为 `18,19,20,21,22,6`。

## 复现与验证

在仓库根目录使用带 Pillow 与 NumPy 的 Python 运行：

```powershell
python tools/unit_anim_export.py
python tools/fx_export.py
python -m unittest discover -s tools/tests -p "test_*.py" -v
```

导出验证要求：10个单位档均有八方向 MOVE；所有 layer 帧号均小于对应 `frame_count`；
A0A/B1A 与 01E 黄金链逐项相等。解释器对截断指令、越界描述符和不收敛控制流报错，不生成
部分正确的 JSON。

运行 `python tools/render_walk_comparison.py` 会先比较 A0A/B1A 的原始 BIN 解释结果与运行时
JSON，再生成 [`analysis/dxanim_walk_comparison.png`](../../analysis/dxanim_walk_comparison.png)。
图中16个方向行均为六步循环，标题同时列出 block0 动画号、镜像 flags 和 `raw=runtime` 结论。
