# Proposal

## Why

R3保留任务已自然请求SC004肖像，但历史CRT链节点缺失。实测冷.data及原堆/锁初始化已具来源，现在可以明确重建一个新CRT资源域，继续原读取及容器构造。

## What Changes

- 从已验冷.data执行原堆/锁初始化，限域投影到六个保留分支，保存所有旧游戏内存、CPU和原调用栈。
- 从自然IMAGE入口连续执行原文件打开、分配、读取、关闭和容器/向量构造，停在首次肖像纹理构造403BD0首指令前。
- 独立逐指令复核来源、完整状态、接口所有权和补充原函数资源清理；更新总规格事实并归档。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

无。实施现有reverse-engineering/completion要求，不改变要求；skip_specs用于有限研究及工具证据。

## Impact

新增保留CRT/肖像审计工具、测试、不可变证据和说明。沿用已有无窗口x86平台助手；不需要解锁，不新增GPU/窗口/输入，不改Godot。重建不等于恢复旧历史堆或同一原生寿命；R3/R6继续进行中。
