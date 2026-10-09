# 场景资源与交互地图预览验收（2026-10-09）

`add-fifth-week-school-planning`完成27/27；本轮新增四个阶段，不等于完整游戏已完成。规划7d7cd6b、原版场景装载28763ea、独立导出94f7022、图形预览b235c38均已本地提交，无push。

同一实际学校隔离CPU完成MAP05贴图、缩略图、雾层和VPT装载：48页256×256、172×128缩略图/雾层、八段VPT和456项偏移重定位。三种就绪队伍成功，两种未就绪分支无装载；全部8次文件句柄闭合。独立来源逐像素/指针/SHA核对，完整雾层上传副本保持一致。GPU和独立图形引导仍是声明边界，自然链停在467EB0单位素材重置之前，原版角色、当前学生记录、MVP、日期和gate保留。

第五周出发准备的「查看本关地图」打开当前2048×1536原图，支持拖动、滚轮/按钮缩放、显示全图、窗口适配、Esc/按钮返回。查看没有追加存档命令、改变队伍或解锁战斗，未就绪/未知场景拒绝。单位、敌人、事件、站位与实际本周战斗尚未接入。默认学校和旧独立MAP01战斗示例继续分开。

| 验证 | 结果 | 证据 |
|---|---|---|
| Godot完整模型 | 62套件409项，0失败 | [model.log](model.log) |
| Python来源/导出兼容 | 55项，0失败 | [source.log](source.log) |
| 地图窗口离屏/实际渲染 | 92/100项，0失败 | [最终输入](../school-scene-preview-headless-v9-20261009.log)、[最终渲染](../school-scene-preview-render-v3-20261009.log) |
| 原出发窗口兼容 | 155/165项，0失败 | [输入](departure-headless.log)、[渲染](departure-render.log) |
| OpenSpec严格全部 | 30项，0失败 | [openspec.log](openspec.log) |
| 最终视觉检查 | 18张逐一检查，1024×768/1280×800 | [地图全图](../school-scene-preview-ui-v3-20261009/map_fit.png)、[宽窗口](../school-scene-preview-ui-v3-20261009/map_wide.png)、[原出发页](../school-scene-departure-ui-v1-20261009/departure_initial.png) |

存档version4十项规则/剧情SHA均与b7391cc逐字节一致，version1/2/3兼容由模型重放覆盖。历史报告、源规则、地图与旧截图逐字节对照e821897；旧UI源码本轮明确增加入口，不列入“未改”声明。范围及精确清单见[acceptance.json](acceptance.json)，本轮文件长度/SHA见[verification.json](verification.json)。

最终UI证据仅采用preview-v3八张和departure-v1十张；早期失败日志与preview-v1/v2截图保留为诊断。修正目录尺寸float/int比较和测试滚轮释放序列，未删去失败断言。原版回放不是真人实机见证，也不写原版SAV。Godot源码项目运行已验证；独立导出包未验证，现有Image文件读取仍输出导出提示。

下一步：单位/字体/效果素材预备、当前/敌人工作体、t0005 VM及双方出场/事件；随后才接学校阵容的图形战斗与完整战后链。[来源边界](../../docs/school_scene_resources.md)、[操作说明](../../docs/school_playground.md)、[审计§107](../../docs/battle_return_audit.md)。
