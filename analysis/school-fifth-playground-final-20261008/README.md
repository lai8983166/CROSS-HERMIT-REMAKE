# 第五周剧情试玩验收 · 2026-10-08

变更 `add-fifth-week-story-playground` 四项全部完成，按原版执行、素材、模型/存档、图形化集成分别本地提交，随后补充一次提交修正跨Git检出的CRLF存档指纹兼容；没有push或更改原版SAV。保留本轮之前的源码、证据和截图。

当前默认试玩可由第四周编班/授课/MVP与两段剧情进入4/5，再点击“阅读第五周剧情”，阅读Chapter018的126页原版对话、大立绘与三人小头像，或确认跳过，最后到达职务室入口。重启恢复准确的页面和人物替换；兼容version1/2旧试玩存档。职务室本体、CH002和第五周学校初始化/编班仍待接入，入口摘要不代表原版职务室界面已经完成。

## 验证

| 范围 | 结果 | 记录 |
|---|---|---|
| 全部Godot模型 | 58套件、384项、零失败 | `model-final.log`（此前383项阶段日志保留） |
| Python新来源/素材及旧兼容 | 16项通过 | `python.log` |
| 第五周真实视口输入 | 157项、零失败 | `headless.log` |
| 第五周实际窗口/截图 | 169项、零失败，12张截图 | `rendered.log`、`verification.json` |
| 旧编班/结果/试玩导航 | 80 / 72 / 26项、零失败 | 对应 `test_school_playground_*.log` |
| 旧剧情/周到达/跨会话导航 | 76 / 51 / 22项、零失败 | 对应 `test_school_*.log` |
| OpenSpec严格校验 | 29项全部通过 | `spec-validation.json` |

`acceptance.json`记录上述测试、来源与截图的SHA-256及目视检查结论。日志固定LF，避免Windows checkout改变验收指纹。

## 截图检查

- `migrated_arrival.png`：version2到达存档迁移，课程成长保留，新增阅读按钮可见。
- `fifth_opening.png`：4/5日历、伊里安原立绘、原版背景与首段对白清晰。
- `fifth_body_pair.png`：奧吉爾/伊里安左右大立绘，当前说话者高亮，导航可见。
- `fifth_long_dialogue.png`：最长对白页完整，文字不挤压翻页按钮。
- `fifth_three_portraits.png`：后段三张SC人物图，无重叠或残留MC立绘。
- `fifth_restored_replacements.png`：重启后复原紐/瑪貝菈/娜芙忒卡、游标121和当前说话者。
- `fifth_skip_confirmation.png`：跳过确认清晰，取消保持内存与保存字节。
- `workroom_entry.png`：完整阅读后入口摘要，日期和成长保留，学校安排边界明确。
- `restored_workroom_entry.png`：重新启动恢复相同出口。
- `fifth_exit_battle_preview.png`：旧地图/精灵战斗预览及返回按钮仍可操作。
- `fifth_exit_after_battle.png`：返回后相同出口，战斗暂停已清除。
- `fifth_confirmed_skip_exit.png`：确认跳过也到达相同日期、成员和原版出口；阅读/跳过命令数量不同，仅内部revision不同。

## 来源与边界

同一CPU原版新局/课程/MVP/Chapter016/017/周交接后，真正CH001以4/5选择Chapter018，执行末尾的两个状态写入指令与END并请求8。准备齐全与按键/界面/淡入淡出等待四个案例见 `../school-fifth-week-v2-20261008.json`；输出规则不含固定期望完成快照。MC与SC图像依据源资源表、绘制裁剪和SC头部转换，文本严格CP950解码（第99条使用扩展字“裏”）。电影/音频/演出时序与原版职务室/学校任务本体尚未执行；不把隔离来源证据声明为实时游戏见证。

下一步从已验证pending8接入原版职务室初始化/操作、CH002和第五周学校启动，再让第五周编班与课程继续可玩。该变更保留未归档，可在适当时使用OpenSpec归档流程。

## 提交指纹复核与兼容补充

原第四周剧情JSON在Windows工作副本中仍为CRLF，Git存储的LF内容与之仅换行不同。本轮最终将导出器固定为显式LF，按已知两个完整哈希兼容原Windows存档；未改原对白、PNG或冻结旧存档。新增模型用例验证CRLF/LF的version2及已生成version3指纹迁移，任意其他目录哈希仍拒绝。补充全量58套件384项、Python16项重新通过；`rendered-lf-compat.log`记录修正后的真实窗口157项操作全部通过，原12张图的UI代码与布局未改。最终核对Git已提交字节与本机指纹一致，见`acceptance.json`。
