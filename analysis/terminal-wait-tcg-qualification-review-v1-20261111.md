# TCG 客体资格尝试独立复核（2026-11-11）

结论：本轮未取得客体输入隔离或 HAL D3D8 资格通过证据，未执行游戏，不能算作完整逆向验收。实际停在部署/控制通道阶段；qualification.json 为 accepted:false、game_executed:false，没有 guest、host_observation 或 verification。v12 目录只有 start.ps1，无 start 的 issued/send/owned/请求回执，且无 probe.json；现有证据不支持称 probe 已启动。这里“未通过”表示资格未执行完成，不是已观察到 D3D8 不兼容。

## 核对结果

| 来源 | 实际观察与限定 |
|---|---|
| v10/report.json | 819.261 秒，process_exited=true，errors=[]，accepted=false；QMP quit 有响应。 |
| v11/report.json | 885.358 秒，process_exited=true，errors=[]，accepted=false；QMP quit 有响应。 |
| v11/shell-enumeration.json | 1.469 秒查询完成；存在一个 Owner 为 CHAOMOFA-WORKER\Administrator 的 shell，不能称当时 shell 已清空。 |
| v12/open-ready-response.json | 47.172 秒取得 owned shell；监督回执 errors=[]、Job active=0、exit=0、remote_completion=observed、response.ok=true，符合 completed 合同。只证明 shell 创建。 |
| v12/channel-send-prepare-* | 45.703 秒 WinRMOperationTimeoutError，remote_completion=unknown、response.ok=false；Job active=0 和宿主 exit=0 不改变远端 Send 未知状态，不证明部署完成或未发生。 |
| v12/qualification.json、channel-close-* | 编排因 Send 失败退出；独立 close 回执符合 completed 合同，仅证明该 WinRM shell 的关闭请求完成。没有计划任务删除证据。 |
| v12/direct inventory | 第一次 receive 50.641 秒远端未知；后一次 38.578 秒宿主超时、exit=124、Job active=0。inventory-cancel-response.json 为 cleaned=true 且符合 completed；这是自有 WinRM command 清理回执，不是资格或计划任务清理。 |
| v12/direct prepare | receive 的运输/监督完成，但客体命令 done=true、status_code=1，stderr 为 The command line is too long.（末尾CRLF）。不能把外层 response.ok=true 当作部署成功。其 command cleanup 回执完成。 |
| v12/report.json | 797.245 秒 process_exited=true；errors 包含 900s/96MiB budget 及 ConnectionRefusedError。overlay=100,728,832 bytes，超过 96 MiB=100,663,296 bytes；时间尚未到900秒，体积触发与回执相符。没有成功 QMP quit 回执，不能称客体优雅关机。 |
| v12/sidecar.json | stop_requested=true、process_exited=true、host_job_active_after=0、errors=[]；只证明该网络 sidecar 的结束。 |

v10/v11/v12 均记录宿主输入操作为0、2 vCPU/4G配置、父来源size/mtime未改变；这些是启动器范围内的记录，不是本轮带随机标签的双端输入观察结果，也不是完整父文件字节保全证明。

已逐字节核对 direct prepare stderr：31 bytes，保存的 .bin 与回执 base64 解码一致，SHA-256 为 712f89f4976302078a5046faca78c00b32aaf1aa6c5f6455945d776ff60eafb5。两个空的 direct-*-response.json 不是有效回执，应引用对应分阶段回执，不补写为成功。

## 清理与后续门槛

VM进程退出、sidecar结束、WinRM shell/command清理、计划任务删除和probe自身资源释放是不同结论。本轮前几类各有上述有限证据；计划任务是否由未知prepare创建、是否删除、probe资源清理均未证实。VM已退出意味着该VM不再执行，但不证明磁盘内任务配置被删除。不得把宿主Job active=0扩大为客体任务完成。

下一步先在同一已认证隔离客体走通最小固定内容回执、完成状态与自有command清理，再测有界小块传输、逐块长度/SHA与最终文件SHA。部署应分块落盘后做最终身份核对，避免重复发送大stdin或再次把完整压缩脚本塞进命令行。每一步保存原始输出；未知变更不重发。部署、console与短设备门槛未过前，不启动长采集或宣称输入/D3D8合格。

本复核仅离线读取证据；未启动VM、游戏、probe或宿主输入。未修改冻结来源和旧回执，仅新增本文件。Git体积与全量本地证据清单由主Agent统一结算。

## 本次读取关键来源身份

路径相对 .venv-audit/native-worker/；以下摘要用于定位现存证据，不替代原字节。

| 文件 | bytes | SHA-256 |
|---|---:|---|
| tcg-wait-native-v10/report.json | 2897 | 45600ba25713155d7f2a7579b9fc16db8965b1165509b78aa91fd4a21f576d0f |
| tcg-wait-native-v11/report.json | 2899 | 8666a7afd0caa5afd2e44dc091002b720639e0041f3b98f5fcce084f96bb7ec9 |
| tcg-wait-native-v12/report.json | 2941 | 9ef7d52c785aba9a73923ce18c8e00e06b4114cabd76783c27ff6ca59d3d1330 |
| tcg-wait-native-v11/shell-enumeration.json | 682 | b8ceba5cecb0de966adc916c4dd4b7d710f4ad342751ae51435a0d6fcc21885e |
| tcg-wait-native-v12/open-ready-response.json | 377 | d9717aa6f66962cd21c81f7fafe7ea19ed5d3afae78ee453663c89e5d5753ea3 |
| tcg-wait-native-v12/qualification.json | 191 | 0d8a42b81ad1ffeeca65f233e55e110f132e1da2c09c7b1a7aa8f1cdb7417614 |
| tcg-wait-native-v12/channel-send-prepare-1794390291295972500.json | 438 | a7beaa16827839ac14b13e356921ed070190dac2ed3405fd31560d45c55e5202 |
| tcg-wait-native-v12/direct-response-receive-direct-prepare-1794390618777981100.json | 773 | 8640c41deb683fae7b403912786e7d8e50e671c895ec446aed09641b75e38ddf |
| tcg-wait-native-v12/direct-prepare-stderr.bin | 31 | 712f89f4976302078a5046faca78c00b32aaf1aa6c5f6455945d776ff60eafb5 |
| tcg-wait-native-v12/sidecar.json | 1981 | 4bacc4150b51891687ddfb943f31766e9e61a154c1e9f88fdf5c10da20a99dbd |
| tcg-wait-native-v12/inventory-cancel-response.json | 344 | e6a334fc72bf6916dcaa0a30153a76d305e2c121ee788fa0491467b252b96171 |
