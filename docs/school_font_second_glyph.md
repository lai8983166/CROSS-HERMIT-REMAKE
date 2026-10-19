# 原版第二轮字形与像素上传

2026-10-19，继续独立、明确声明空缓存初态的启动实验。连续 VM 仍为40E2D0 / PC224 / wait1、manager owner0；继承缓存缺失边界保持，未修改 Godot 或原存档。

350 来源：第二字体沿同一原401491循环处理ASCII32至126，共95次尺寸查询、95次实际绘制和380个浮点UV字段写入；随后原401660执行65536个32位DIB读取、16位转换和纹理写入，规则仍是蓝色高4位为alpha，alpha0写0，否则写(alpha<<12)|FFF。换行和UV使用实际原尺寸查询值，不用首个字体的固定宽度代替。

351 GDI平台：新x86助手单独保存第二字体的字符计数、画笔位置、待绘制状态和前后DIB快照。首个字体的状态和原清理记录不重置。辅助GdiFlush/快照明确不是原版调用。354设备平台另设第二锁、pitch、bits、初始缓冲和上传状态；真正第二UnlockRect后只读读回整张第二纹理，再真实只读读回首张纹理，核对首张内容完全保持。中止锁的补充Unlock与两张纹理/首个VB/两个token全部清理，六项平台测试通过。

像素边界调查：v1原执行报告中，两例均在(x111,y28)出现超出尺寸查询单元格的一个白色像素，归属字符w。不能直接把尺寸查询的前进宽度当成墨迹宽度。v2助手在前后快照中增加实际GetCharABCWidthsA辅助查询；w得到A0/B7/C−1，前进宽度A+B+C仍为6，墨迹宽度为7。依据[微软API说明](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getcharabcwidthsa)，负C表示字形向右伸出。验证逐字要求ABC总和等于原查询宽度，并检查单元格与实际横向墨迹范围之外的全部像素保持；没有硬加容差、裁切像素或改写原UV。v1源码/助手/平台报告/三个原执行报告及日志保留，新增[调查证据](../analysis/school-font-second-glyph-ink-investigation-20261019.json)记录原假设被实际数据推翻。

352 映射退休：到达第二401491后，先核对首个字体三次实际GDI删除和GetObjectA已无法取得旧DIB，再核对旧DIB完整262144字节、所有guard及完整映射表。只解除旧DIB的那块审计映射，完整buffer证据进入retired_regions；首张纹理影子继续映射，CPU/所有对象/owner/image/SEH/接口保持。退休没有执行原版指令或平台调用，也没有再次释放主机资源。

353 原字形：同一CPU自然执行全部95测量/绘制对，真实第二DIB快照与动态布局、ABC墨迹、380个原UV写入、完整1656字节对象/填充/保护区及190次原栈检查逐项核对，停401660。旧DIB退休证据和仍活跃的首张纹理影子保持。

355 原像素：在第二DIB真实地址映射新的guard缓冲，再映射真实第二LockRect返回的目标地址，拒绝与仍存活范围重叠，不搬移接口。两个案例中退休后的地址可按新DIB身份使用。原机器码完成65536个有序读取和65536个有序写入，所有16位结果、pitch填充、边界、局部变量、调用栈与CPU均核对；真实上传、第二只读读回与首张纹理完整只读读回全部一致。停4017B6，第二原GDI清理、VB、两个状态块和415F50完整返回尚未执行；临时第二GDI资源由助手补充清理，不能冒充原清理。

356 验收：A5/640×480、CC/1024×768两例；19项本批来源/平台/退休/原执行测试加16项直接父链，共35项相关回归，包含三个原执行/退休阶段各两例新鲜重放；30项严格规格通过。篡改测试覆盖退休映射/证据/CPU/释放权限、实际GDI/ABC/布局/UV/原返回、所有旧新像素guard、两张真实纹理读回、完整访问顺序、像素循环局部量和未执行清理边界。16,251个既有文件、十项存档规则和九份私有VM检查点保持，工作SHA及Git blob逐项核对。七个计划阶段和一次ABC辅助检查改进分别本地提交，共八次，不push；356/356只是已列任务数。

证据：[来源](../analysis/school-font-second-glyph-source-v1-20261019.json)、[GDI平台v2](../analysis/school-font-second-glyph-gdi-v2-20261019.json)、[像素平台](../analysis/school-font-second-glyph-device-v1-20261019.json)、[映射退休v2](../analysis/school-font-second-glyph-retirement-v2-20261019.json)、[原字形v2](../analysis/school-font-second-glyph-raster-v2-20261019.json)、[原上传v2](../analysis/school-font-second-glyph-upload-v2-20261019.json)、[回归](../analysis/school-font-second-glyph-regression-20261019.log)、[严格规格](../analysis/school-font-second-glyph-strict-20261019.log)、[保留检查](../analysis/school-font-second-glyph-preservation-20261019.json)、[验收](../analysis/school-font-second-glyph-acceptance-20261019.json)。

下一步执行第二个字体的原清理、VB与状态块，验证两槽循环结束及415F50完整返回。随后仍需manager/队列、真实上游初始化和缺失缓存堆与连续VM衔接，再推进外层调度、绘制和后续游戏逻辑。
