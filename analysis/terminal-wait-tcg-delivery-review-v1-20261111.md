# TCG 交付链独立复核（2026-11-11）

结论：当前受测 TCG + WinRM 控制组合没有满足有界自动化控制准入；应停止该交互路径。本轮没有进入客体小块部署、计划任务注册/启动或资格probe执行，故没有实际输入隔离和D3D8资格结果，不能判断D3D8不兼容，也不能推广为TCG架构一般不可用。正式验收仍为2/8，本复核不增加验收项。

## 结果与归因

| 案例 | 实际证据 | 允许结论 |
|---|---|---|
| v13 | service-ready阶段100秒结束；readiness错误先为TypeError，继而FileExistsError。delivery_v1将send_message的bytes直接JSON序列化，并把保存失败捕获为传输重试；v2修正原字节base64回执。 | 本地实现/记录故障；不归因客体、TCG硬件或图形。 |
| v14 | minimal-native chunk0为准确TCG-Q14-4f39edc3加CRLF；chunk1为空输出、done=true、exit_code=0。没有command清理成功回执，旧实现将cleanup计入同一30秒阶段。 | 命令确已成功返回；后续cleanup预算缺口，不得写成native命令未返回。 |
| v15 | minimal-native completed为12.047秒；result为12.594秒、准确nonce输出、exit0、command_cleaned=true。minimal-powershell只有request/owned，无输出块或完成回执；active-stage为60秒，stage-timeout指向该阶段。 | native返回加清理已通过。12.594秒是含cleanup的总耗时，cleanup增量约0.547秒；极小PowerShell未在本次预算内完成，客体执行状态未知。 |
| v16 | minimal-native仅request，无owned_id；delivery记录WinRMOperationTimeoutError。delivery_v4共享Protocol在Command创建前仍带Receive用的5秒operation_timeout；v5按阶段恢复创建预算。 | 控制实现配置缺陷参与失败；不得作为TCG或D3D失败证据。shell_closed有记录，不代表未获owned_id命令的原生清理已验证。 |
| v17 | native completed为45.406秒，result为47.578秒、准确TCG-Q17-4f39edc6加CRLF、exit0、command_cleaned=true；cleanup增量约2.172秒。actual-uuid chunk0文本含专用UUID，但done=false、exit_code=-1；40秒watchdog结束，没有completed/result或该命令cleanup成功回执。 | native最小命令确已返回且清理；UUID只有部分数据返回，不能把匹配文本当作命令完成或完整身份门槛通过。当前有界控制链未获准继续部署。 |

v15与v17的控制超时配置不同，12.594/47.578秒只是各自命令加cleanup的实测总耗时，不构成严格等价性能比较，不能把差异归因于TCG。拒绝当前准入的依据是完整控制链及身份命令生命周期未闭合，不推断TCG硬件一般性能或D3D兼容性。小块传输只在Windows宿主本地解析试验通过，客体并未执行；本轮三个交付门槛仅达到最小命令返回加清理，未达到客体小块部署及资格probe执行。

所有现存原始chunk的stdout/stderr均重新base64解码并核对SHA256；v15/v17准确nonce输出另与预期字节核对。v17部分UUID匹配626D1A20-6383-4CD3-85D5-6C9831D6F941，但这不补足完成/清理缺口。没有block请求、register-task请求、start-task请求和probe.json；不得把宿主cmd解析器试验或内存Task XML解析试验算作客体部署或probe运行。

## 生命周期和清理边界

| 案例 | VM总秒数 | 监督worker退出 | VM/sidecar及宿主Job |
|---|---:|---|---|
| v13 | 281.636 | exit124、remote unknown | VM与sidecar process_exited=true；sidecar及监督Job active=0 |
| v14 | 243.812 | exit124、remote unknown | 同上 |
| v15 | 351.337 | exit124、remote unknown | 同上 |
| v16 | 297.958 | exit0但response.ok=false | 同上 |
| v17 | 370.296 | exit124、remote unknown | 同上 |

各VM回执accepted=false、errors=[]、parent_size_mtime_unchanged=true。size/mtime核对不是完整父盘字节保全证明；监督器的invalid worker response对应watchdog直接退出、没有最终JSON，并非客体命令成功。v16外层remote observed只表示失败报告被收到，不能算业务通过。

VM/sidecar退出与宿主Job清空有实际回执；它们不等于此前客体原生命令逐一完成或正常清理。只对v15/v17已有result的minimal-native承认command cleanup；v14的cleanup及v15 PowerShell/v17 UUID命令清理没有通过证据。没有计划任务注册证据，亦没有任务删除或probe自身资源释放的验收证据；不使用VM退出替代这些结论。本轮未取得完整host标签输入观察或HAL D3D8调用现场。

## 保留与后续处理

v13/v14叶盘已有各自退役清单，记录原bytes/SHA及替代来源；不再把被删盘报告为可获取。v15/v16叶盘由主Agent按授权记录退役，保留源码、原始小回执和必要摘要；v17保留为本轮唯一必要失败叶盘并压缩。本文核对时v17原disk.qcow2仍存在，76,218,368 bytes，原SHA256为8db8c8d5a2f68df77047ce2002214d0d328d127f688c003c55b8fadbb9719b0e；最终压缩、删除完成状态及磁盘/Git体积以主Agent生成的保留清单为准，本文不提前宣称已完成。旧v10来源不在本次退役范围。

已明确停止新增VM与该交互路线。今后若选择其它隔离控制方案，仍须先满足最小完整命令返回、独立清理及有界身份查询，再做部署、输入与原HAL D3D8资格；本次结果不降低这些门槛。本复核只离线读证据并写本文件，未启动VM或原生任务，未修改冻结源码。

## 关键证据身份

路径相对 .venv-audit/native-worker/；摘要不替代原字节。

| 文件 | bytes | SHA256 |
|---|---:|---|
| tcg-wait-native-v13/report.json | 2898 | e9045bc8a66050ddcc01600eca4a116860d4206e9c812fd1029f55863f7403dc |
| tcg-wait-native-v13/sidecar.json | 1982 | ed9290d537e113ee3068dc7bd06c43eb0a6daa9314ac35348fe459ccb9a1f109 |
| tcg-wait-native-v13/supervision.json | 313 | 589742579cb25f8d599723b31e6af795194cc664dca6a4a201b8e15c869a4a7b |
| tcg-wait-native-v14/report.json | 2904 | 2adad8eb856ed43158ca01e3892ff83909fa79fc1724e54900b5685cb72716ee |
| tcg-wait-native-v14/sidecar.json | 1970 | faa91232bfed5effaef7cb1b269c9d0f9628239e30d1acd986041e30b071e074 |
| tcg-wait-native-v14/supervision.json | 324 | 715d19ab8bbf7675fe1cf8837e35e7ac7e21098cb06cb64d83e0da82542591cf |
| tcg-wait-native-v15/report.json | 2899 | b9dd8413f3ac40c1da45381697573e0e7f55d92f18341e4a1278d1e54418db8b |
| tcg-wait-native-v15/sidecar.json | 1982 | d114808d8fd062bd4ef4465f0d2f8f63bbf2a14717d0e9c02005f6207a664e25 |
| tcg-wait-native-v15/supervision.json | 325 | c5b753dcadd7c84fc2f25eac74695a0c080811316e2fb796451f36778f839024 |
| tcg-wait-native-v16/report.json | 2899 | 42fa86c4f0e31f4cc0e9cdf95b27f7d99898f80f6c31a70680b57e0ba3c1d7c1 |
| tcg-wait-native-v16/sidecar.json | 1982 | 73bb5ae40e354f4d3c5e4d3c145ce7d3120619fcdfddd05f151d13e1d9fe979a |
| tcg-wait-native-v16/supervision.json | 477 | 84521cbf57947cf158dae913e81802cf62e87663598039ad16472e64ccf6fd9d |
| tcg-wait-native-v17/report.json | 2899 | 60b5869a6e00ee83b65c5f259448056eaf3161293ad748323dd15f6b30cbdce4 |
| tcg-wait-native-v17/sidecar.json | 1981 | 64e285d3229d7f6a1d0eecd994c9794cbe3ca0959fcfeca0bd7883128d4805c3 |
| tcg-wait-native-v17/supervision.json | 325 | aa91d8311b37ddb32ab13d2eee8b6e6d1647da0caa5ff1d137ce20de49bc1638 |
| tcg-wait-native-v15/minimal-native-result.json | 275 | d5c7ac195e436bddc717f2677c2e02479e25932e375721556c1d9cb002d380ae |
| tcg-wait-native-v17/minimal-native-result.json | 274 | 886617d656f4389dbc465b4c0226fce1b068e9bddcc9efde49ee934c5f458427 |
| tcg-wait-native-v17/actual-uuid-chunk-0.json | 331 | c18171144c0532e34075c0cbabc552b81dcce7d29bc07d8327da9e78589788b7 |
