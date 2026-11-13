# 原 MAIN 与 GAME 构造接续：单次结果

2026-11-13，沿用当前原生所有者和原指令执行器，只做了一次有界无窗口原生预检。
原生运行3.641秒，169671条原指令、72次原平台叶、344条有应答的native请求。
**本轮组件验收拒绝，正式仍2/8。** 没有重复原生运行，没有进入场景、等待或结果消费。

## 已实际走通的范围

- 冷CRT/heap/TLS初始化后，从原WinMain入口49DD70执行到49DE23前；原MAIN构造、
  7A4A00发布、管理器32桶清零完成。停在窗口初始化之前。
- 保留WinMain挂起栈，以显式独立根进入原412C70工厂。原412CBD调用412E30，
  47648字节GAME对象完整构造后自然返回412CC2，继续到413450首指令前停止。
  真实GetDC(0)、QPC/QPF通过同一实际MAIN线程执行，GAME+B208保存实际DC。
- GAME全局7A49FC仍0，工厂输出仍A5哨兵；没有手填GAME、伪造窗口句柄或跳过设备初始化
  后声称发布成功。工厂未返回；这不是连续WinMain→GAME→场景。
- 在第三份独立栈上调用原412DD0(this,1)，原413150析构、413417 DeleteDC、
  原428AD0/HeapFree成功返回。两个挂起原栈保留，不改原全局来美化清理状态。

原字节、导入ABI、完整57项执行器状态、累计指令/写/内存摘要和活体116B PTD读回都记录
在本轮来源。它们是Unicorn中的原指令状态；Windows API由同一x86 helper所有者执行，
不是物理CPU直接运行整个游戏，也不是宿主特权/隐藏上下文导入或独立完整重放。
旧worker/TLS/队列代码保持原字节；本轮未创建worker，旧基类worker成功不能冒充本轮场景成功。

## 精确拒绝位置

同一TID8184、TEB003EA000的实际回执：

| 请求 | 原因/调用 | 返回 |
| --- | --- | --- |
| 272 | 原412E30中的GetDC(0) | DC=B6013707 |
| 296 | 原413417 DeleteDC(同一DC) | 1 |
| 344 | 预检追加ReleaseDC(0,同一DC) | 0 |

预检原先假设GetDC取得的DC经原DeleteDC后仍须由ReleaseDC成功释放，实际返回不符合该假设。
不能把ReleaseDC的0改为1，也不能凭DeleteDC返回1就补写一条缺失的对象失效证明。
本轮没有采集删除前后的GetObjectType/资源计数，故不宣称已证实泄漏或完整释放。

微软说明GetDC取得的公共DC应由同线程ReleaseDC释放，DeleteDC不用于这种来源；本轮保留
原游戏实际DeleteDC调用和结果，未替换API。参见[DeleteDC合同](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deletedc)
与[ReleaseDC合同](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-releasedc)。

失败时原GAME内存已释放，后续MAIN析构、PTD/TLS清理和正常Shutdown未执行。
外层Job终止helper，实际exit94、Job为空、父侧已跟踪句柄关闭且无清理错误；这只是有界
失败清理，不能计作原资源寿命验收。未超时。基础父端两个初始管道CloseHandle的BOOL
记录缺口与上一来源相同，不因handles_closed字段而宣称逐句柄完整证明。

## 后续准入与止损

本轮一次原生额度已经用完，禁止换输出名重跑相同配方。下一次先离线修正DC观察合同：
原DeleteDC调用保持，记录其前后对象类型与当前进程资源变化，将原调用与补充清理区分；
只有可核验的释放后状态才能销账。不能无条件把ReleaseDC=0等价为泄漏或成功。
先单独解决这个具体观察缺口，再允许后续MAIN/PTD正常清理；不要为复测重复游戏长前缀。

通往目标的真实依赖仍是GAME合法初始化/发布。451170构造内部4075E0/4077C0已经要求非零
GAME；只补字体无法进入场景。原450570工厂发布前还经过音频、设备及窗口初始化。
该依赖必须按现有原工厂证据解决；需要宿主窗口时先告知用户，不回到截图、TCG或全原机搬运。
首次451670→422360返回、453CB5消费、三次握手和两例新鲜原生完整重放均保持未完成。

## 保留与复现

- 来源：`analysis/terminal-scene-owner-preflight-v1-20261113.json.gz`。
- 独立现场复核：`analysis/terminal-scene-owner-independent-review-v1-20261113.json`。
- 构建/体积/退役清单：`analysis/terminal-scene-owner-closeout-v1-20261113.json`。
- 实现：`devtools/terminal_scene_construction.py`、`devtools/terminal_scene_native_extension.py`。
- 精确成功构建：`.venv-audit/terminal-scene-owner-build-v3-20261113/`；只有编译成功，运行未验收。

全部新增环境、日志、证据在F盘。未建游戏窗口、未读取像素、未发宿主输入，也未改分辨率、
任务栏或前台；GetDC只取得句柄。本轮没有执行桌面恢复测试，不把未操作说成已实测恢复。
冻结本轮采集实现和报告，后续修复必须新增版本，不能改写失败来源。
