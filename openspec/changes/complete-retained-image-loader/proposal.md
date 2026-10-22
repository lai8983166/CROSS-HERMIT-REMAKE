# Proposal

## Why

R3六个保留分支已由原代码读完SC004并构造记录，但IMAGE尚停在首个纹理入口。利用已验原生纹理契约，在新CRT资源有效寿命内执行原像素复制、文件缓冲释放和加载器自然返回，可补齐这一连续资源链。

## What Changes

- 在新有效CRT域内复现已验前缀，再连续执行403BD0至4CC0D2自然返回；游戏、CRT和memcpy函数全部执行原代码。
- 四次纹理接口仅回放已固定原生回执，核对完整262144字节/512行；不复用失效原生指针，不声称新增GPU上传。
- 明确执行原容器析构清理及原堆锁销毁，独立核对六分支完整CPU/内存、所有权、统计和正常退出。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

无。实施reverse-engineering/completion既有要求，新增研究证据；skip_specs保持规格要求不变。

## Impact

新增审计工具、测试、证据与说明；既有工具与证据不改。无需交互桌面、新窗口、新GPU或输入。原handler动画/外层世界、全CRT历史和Godot另计，R3/R6保持进行中。
