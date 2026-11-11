# CR2 v4 helper全局读取合同修复

accepted=false。等待tcg-wait-native-v5/report.json实际出现且process_exited=true，并收到主Agent确认后才执行构建；未启动VM，未改任何v12/v3源码、对象、二进制或运行来源。

新增devtools/terminal_tcg_cr2_build_v4.py，固定新输出目录tcg-cr2-build-v4，存在即拒绝重跑。逐项重新散列v3编译器/库、原链接输入、新对象、配置及overlay；唯一重编译单元为target/i386/tcg/translate.c，链接按v3原命令只替换该对象及输出路径。

## 唯一语义修改及实际include证据

从v12认证的helper.h复制新overlay，唯一声明变化：

    DEF_HELPER_FLAGS_3(write_crN, TCG_CALL_NO_RWG, void, env, int, tl)
    DEF_HELPER_FLAGS_3(write_crN, 0, void, env, int, tl)

0保守允许helper读取及写入TCG globals，避免继续宣称NO_READ_GLOBALS；未改PF恢复挂点或任何事件序列逻辑。translate.c与emit.c.inc从认证v3 overlay原字节复制。编译命令最前插入 -iquote 指向新overlay/target/i386，确保exec/helper-proto.h、helper-gen.h及helper-info.c.inc内部的helper.h查找均命中新头。

编译器实际产生translate.c.o.d，脚本验证其含新helper.h路径，不含旧helper.h绝对或原相对路径；缺失或旧头同时出现则构建拒绝。进一步直接解析ELF64 LE符号表及helper_info_write_crN原始数据，而非只看源码文本：旧88-byte符号的x86_64 flags偏移28字节=1，新值=0，其他符号数据字节相等。

新helper.h：8085 bytes，SHA-256 fcdeaf439e2a327eba743f414d4270bfd6bedc5fe7f8bc91565e8b20779f446b。

## 对象和产物身份

旧translate对象742160 bytes，SHA-256 51960c74584ecbad5fa4118cb88371648b4f60d614db24605cc0a2c0264afff8。
新translate对象742160 bytes，SHA-256 4291ee9678395fdb92f7f34b038704d24b11221a4528252301bca37798a1d361。

全对象逐字节比较仅3字节不同：文件偏移186793和186897是编译期文件名字符串tcg-cr2-build-v3改为v4；306652是helper_info_write_crN flags由1变0。没有其它对象字节差异。

新binary：29,805,128 bytes，SHA-256 b89c94a303d66b6f65486c3a2b5195021876a21b6e7bf37deb8337d109e3f6fb。完整命令、父manifest、已退出gate身份、依赖文件、头文件及对象前后符号字节见tcg-cr2-build-v4/manifest.json。编译/链接日志为空，--version正常返回QEMU 11.1.0。构建后再次散列v3全部overlay、对象和binary，均与原manifest相等。

新增本地v4构建证据30,892,927 bytes，无额外备份；尚未清理v1/v2/v3派生产物。整轮总容量仍由主Agent汇总。新Git文件仅构建脚本与本报告。

## 验收范围

上述只证明修复确实进入编译/链接产物和旧来源保持不变，不证明运行时PC正确。主Agent需以v4独立执行overflow首MOV多指令TB反例、原normal微例及完整导出端点等价；v3失败来源保持原样，不追改其错误PC或验收结论。
