# 已授权的原版保持空格实验

状态：用户已明确允许computer-use JS API限制的例外，两个独立原版输入转换已通过；授权记录见 analysis/school-native-dialogue-authorization-v1-20261022.json。当前change仍为verify-native-dialogue-input，不另建change。

## 具体操作

目标仅限`.venv-audit/scene-callback-runtime/`中本工具启动并纳入自有Job的原版进程。工具在原opcode51确认门稳定1秒后，将原GUI和场景线程保持运行；独立线程调用一次扫描码空格按下，等待120ms，再发送松开。读取游戏实际输入、VM与真实时间，交接前后保留完整原线程/世界/脚本样本，最后正常关闭自有游戏。

启动前先检查实际输入桌面/锁屏状态；进入前及按下前检查Job成员、HWND/PID、CPP_CLASS与原MAIN、精确私有exe路径和前台HWND。不会为输入强行激活别的窗口。保持时长只允许80–250ms，正式实验120ms。按下后发生异常会尝试释放；发送失败不能计为成功。所有按下/松开返回和时间戳写入报告。

## 已有验证

9项测试仅使用惰性API，不向Windows提交输入。新handoff验证器只接受实际按下/松开、源VM越过确认PC、原输入查询、真实接口回执/时间关联及完整原生清理同时成立的输入转换；held-76-v4和held-77-v2已满足这些条件，失败历史原样保留。

## 授权后的复现命令

复现时必须使用全新的输出路径；下列fresh路径仅为示例。--held-input是明确的实验开关，不会由默认运行、超时或工具错误自动开启。

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_native_dialogue --scene 76 --held-input --notice .venv-audit/native-dialogue-held-76-ready.json --out analysis/fresh-held-76.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_native_dialogue_handoff_verification --report analysis/fresh-held-76.json.gz --require-transition --out analysis/fresh-held-76-proof.json
```

先核对76，再以77独立复现；不是只验证SendInput返回值。通过后更新已有任务、执行受影响集成检查、总规格同步和归档。本实验不改变R3保留执行连接及R4–R6的剩余要求。
