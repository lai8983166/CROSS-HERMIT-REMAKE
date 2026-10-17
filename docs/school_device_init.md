# 原版设备初始化与真实32位接口

2026-10-17。本批从独立声明的scratch所属对象与隐藏窗口开始执行原413450，不改写原连续VM的owner_read检查点。

292来源：保留的原导入描述符5FD6A8与名称表确认d3d8.dll/Direct3DCreate8，原526C40经原IAT59246C跳转，4136D0传SDK220。413730依次尝试(type1,flags40)、(1,20)、(2,40)、(2,20)，4138A0以OR4形成实际flags44/24；原413850的窗口分支调用4138A0。尺寸、原52字节presentation、能力查询、后备缓冲区描述、22种偏好格式扫描及视口均有原指令来源；415F50字体初始化位于owner绑定40D970及队列初始化40DAB0之前。

ABI交叉参考使用Wine项目自身的[接口声明](https://raw.githubusercontent.com/wine-mirror/wine/master/include/d3d8.h)、[结构声明](https://raw.githubusercontent.com/wine-mirror/wine/master/include/d3d8types.h)和[能力结构](https://raw.githubusercontent.com/wine-mirror/wine/master/include/d3d8caps.h)。原二进制的调用字节、偏移及分支是本研究的行为依据，接口声明只用于核对桥接ABI。未将Direct3D9结构套用于Direct3D8。

本批计划让原指令驱动真实工厂/设备创建，逐一核对完整原owner、调用栈和真实接口输出，停在415F50第一条指令前。字体、管理器owner绑定、队列初始化和完整外层帧将保留为后继边界；所有平台指针仅在桥接进程存活期间有效。

293桥接：独立x86进程只先创建隐藏窗口，工厂与设备按请求实时创建。实际工厂/设备/表面vtable及方法地址随响应捕获；返回16字节显示模式、52字节presentation、212字节caps、32字节后备表面描述。实际视口设置成功，表面引用释放、device/factory最终Release0、隐藏窗口销毁均核对。八项来源及桥接测试通过，覆盖外来/过期指针、全屏、重复工厂、非法尺寸、Present和关闭后请求拒绝。该桥接验收尚不计原CPU已执行。
