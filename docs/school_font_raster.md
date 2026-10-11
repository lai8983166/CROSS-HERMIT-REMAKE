# 原版字体、字形位图与文字计数（2026-10-12）

本轮使用真实Windows GDI创建字体、测量和绘制离屏DIB；不返回占位字体句柄或固定宽度。原版CreateFontA输入、实际主机ANSI代码页、选中字体和字形位图单列。字体高度0按系统默认选择，实际字体/文字结果受当前主机环境影响，不能据此宣称2002年系统上的字形完全相同。参见[Microsoft CreateFontA说明](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createfonta)与[TextOutA说明](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-textouta)。

适配器只创建本进程离屏资源，不更改系统代码页或字体设置。它检查32位句柄与有界32位顶向下DIB，记录资源选择并在结束时恢复、删除字体/位图/DC。测量上下文为明确声明的私有平台适配器，不声称此前原版图形上下文已启动。原Big5文本字节未经转码传给ANSI接口；Godot预览仍按CP950解码并保持可读原文。

Win64有时对GDI句柄符号扩展；适配器只接受零扩展或符号扩展的真实32位值。参见[Microsoft 32/64位句柄互操作说明](https://learn.microsoft.com/en-us/windows/win32/winprog64/interprocess-communication)。
