# 本地原始证据与 Git 历史迁移

2026-10-28，仅处理远端 `db9a52ef9fbdde4f561c4585e93a4ceb0708de58` 之后尚未推送的42个提交。该远端提交及其祖先保持原样；每个本地提交的作者、提交者、时间、说明和非迁移文件内容均保留。

## 原件位置与校验

12个新加入且至少10 MiB的终局原始来源报告不再存为普通Git对象。原件仍在项目的原 `analysis/` 路径，现有来源、独立验证和保全脚本可以继续直接读取。

完整清单在 `analysis/local-evidence-migration-v1-20261028.json`，逐文件记录字节数、SHA-256、原Git blob ID、本地路径和外部备份位置，并附42个旧、新提交的对应关系。

```bash
.venv-audit/Scripts/python.exe -X utf8 tools/verify_local_evidence.py
```

新克隆不会自动带有这些本地原件。先从清单指向的备份恢复到原相对路径，然后安装本地忽略规则并校验：

```bash
.venv-audit/Scripts/python.exe -X utf8 tools/verify_local_evidence.py --install-excludes
```

不要用空文件或重新生成的近似数据替代已封存证据。该选项仅向当前仓库的 `.git/info/exclude` 追加缺少的规则，不修改全局Git配置或已经冻结的 `.gitignore`；重复执行不会重复追加。

## 独立备份

项目旁的 `../chaomofa-local-evidence/20261028-cc93acf8/` 保存：

- `files/analysis/`：全部12份原始文件的逐字节副本。
- `original-main.bundle`：迁移前main的完整、自包含Git历史，已通过bundle校验。
- `plan.json`、`backup-complete.json`：迁移分界、原引用、原件哈希和备份结果。
- `rewrite-complete.json`、`publish-prepared.json`、`verification-complete-v2.json`：逐提交重建、发布方案和最终核对记录。
- `publication-correction-v2.json`：保留冻结 `.gitignore`、改用本地排除规则的兼容修正。
- `original-index`、`original-gitignore`、`original-local-exclude`：迁移前的索引与忽略规则。

可以通过以下命令在另一个目录查看完整旧历史：

```bash
git clone ../chaomofa-local-evidence/20261028-cc93acf8/original-main.bundle ../chaomofa-before-evidence-migration
```

该备份目录位于Git工作区之外。不要把bundle或原始大报告再提交回代码仓库。

## 历史验收记录的含义

既有验收JSON、报告、存档、私有检查点及其SHA-256不改写。旧记录中的提交ID和“worktree/index/HEAD字节相等”描述对应当时封存的原历史，可从bundle及提交映射追溯。它们不是迁移后这些本地大报告仍被Git追踪的声明。

迁移后按两部分核对：代码、小报告等版本文件继续按Git对象验证；清单中的大证据按本地文件大小、SHA-256和原Git blob ID验证。对新change仍保留必要的完整原生重放和独立验收，不因为改变存储位置降低验证标准。

## 后续提交

本地 `.git/info/exclude` 排除终局全量来源报告和大型诊断的新产物；安装方式见上文。`.gitignore` 保持早期封存的原字节，以兼容既有保全脚本。生成文件照常使用新名字保存在本地，代码仓库记录复现代码、小型报告及路径/大小/SHA清单。提交前按AGENTS.md检查对象体积。

迁移未清理本地旧对象或reflog，也不修改Codex私有引用，因此本地`.git`不会立即缩小。普通main推送只包含新提交链可达且远端缺少的对象；不要使用mirror把私有引用一起推送。

本次不执行push。远端分界保持不变，新的main仍以该提交为祖先，不需要强制推送来替换远端历史。

迁移后的既有终局保全审计已通过：固定父65项及递归原资产、存档、私有检查点和历史资料保持原字节。结果另存于备份目录的 `project-preservation-v2.json`。
