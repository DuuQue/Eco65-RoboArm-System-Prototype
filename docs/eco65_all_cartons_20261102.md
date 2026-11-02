# ECO65 全库存原生运行：2026-11-02

本次从完整 16 箱库存重新运行，实际完成 **16/16**；模式为 `FIXED_INSTALLATION`。
这是同一次运行、同一安装位及连续状态链的结果，没有拼接历史轨迹或完成数量。
任务状态 `COMPLETE_ALL_CARTONS`，终态箱体 world=0、attached=0、completed=16。

## 场景与实现身份

- 实现提交：`28be118d64c0e93365dc88e9acd167654389c1e1`。
- 只读参考：`4d191ecab065420e4b70c9b266c87654996bd91f`。
- worker SHA256：`e18f657822f6ada859b2c581cdd2589f62b73e09f6daa22ec322f0f3d69dddb6`。
- 快照：`ecda07724b2545524a17a99e714c95be5c54b4818f22a5182ba36ae5c4a47ff8`。
- 计划：`d153b483635a9e11662f84557ad20a0deb5a6816f44069b6654abd0801c6b6a9`。
- 配置：`configs/workcells/eco65_lab_prototype_4c4l_fixed_candidate_v2.yaml`。
- 单箱 150×100×100 mm，一排深、4 列×4 层；箱堆 150×415×400 mm，底层 Z=0。
- 固定基座 (−487.5,37.5,225) mm，绕 Z 安装角 π；真实 ECO65-B、吸具及全部 12 物理吸盘。
- 厢体内部 1600×675×1050 mm，地板、两侧壁、顶板、封闭端均参与规划；−X 入口敞开。
- 横带 550(Y)×175(X) mm，行程 100～525 mm；纵带 700×150 mm，远端高 150 mm。
- 横带接收后沿 −Y、−X 检查理想出料；400 mm 末端承接板保留真实支撑关系。

新服务器恢复了既有隔离环境。本次核对 228 个实现文件哈希和 worker 哈希，执行恢复环境中的原生定向合同检查；没有安装或升级依赖。

## 本次接受的完整流程

各箱完整后缀包括接近、接触、附着、抽离/转运、释放、名义接收、工具安全退出、检查理想出料和清空；后箱从前箱实际末态继续。
未启用杯的几何仍存在。顶吸没有 100 mm 高度门槛；本次采用的实际抓面和完整密封杯数如下。

| 顺序 | 目标 | 抓面 | 密封杯数 | 带高 mm | 实际落差 mm |
|---:|---|---|---:|---:|---:|
| 1 | carton_r00_l03_c00 | top | 6 | 300.000 | 12.500 |
| 2 | carton_r00_l03_c01 | top | 6 | 300.000 | 12.500 |
| 3 | carton_r00_l03_c02 | top | 6 | 300.000 | 12.500 |
| 4 | carton_r00_l03_c03 | top | 6 | 300.000 | 12.500 |
| 5 | carton_r00_l02_c01 | top | 6 | 200.000 | 12.500 |
| 6 | carton_r00_l02_c02 | top | 6 | 200.000 | 12.500 |
| 7 | carton_r00_l02_c00 | top | 6 | 200.000 | 12.500 |
| 8 | carton_r00_l02_c03 | top | 6 | 200.000 | 12.500 |
| 9 | carton_r00_l01_c01 | top | 6 | 100.000 | 12.500 |
| 10 | carton_r00_l01_c02 | top | 6 | 100.000 | 12.500 |
| 11 | carton_r00_l01_c00 | top | 6 | 100.000 | 12.500 |
| 12 | carton_r00_l01_c03 | top | 6 | 100.000 | 12.500 |
| 13 | carton_r00_l00_c01 | top | 6 | 100.000 | 12.500 |
| 14 | carton_r00_l00_c02 | top | 6 | 100.000 | 12.500 |
| 15 | carton_r00_l00_c00 | top | 6 | 100.000 | 12.500 |
| 16 | carton_r00_l00_c03 | top | 6 | 100.000 | 12.500 |

## 时间与检查范围

- 实际规划墙钟：2620.919 s。
- 接受轨迹的机器人运动时间：1182.044 s。
- 机构展示时间：3.853 s。
- 名义下落时间：0.808 s。
- 理想出料时间：151.308 s。
- 额外事件展示停顿：22.400 s。
- 离线浏览器结果：`PASS`，5038 项实际页面检查。

上述运动/展示时间不等于实体设备节拍。规划、碰撞、实际 FK 吸盘密封、附件所有权和请求父状态来自本次原生记录；原生失败候选及搜索 trace 一并保留。
本次有 80 个机器人运动段、4 个外部轴记录和 95 个事件；16 次附着、释放、名义接收、检查理想出料及清空均齐全。
实际 J1 正向累计 4.746267 rad、负向累计 4.321895 rad，使用无方向硬约束策略；报告中的旧 reverse 字段为非适用计数，不是单调性成功的依据。
505 次原生调用中 384 次 SUCCESS、1 次 READY；118 次有限 IK 求解失败、2 次状态拒绝均为未采用候选。两次状态拒绝分别为 `part_000 ↔ trailer_roof` 和 `link_2 ↔ prototype_chassis` 相交；保存于 `state_rejections.json` 及原始请求包。没有失败的整箱后缀被记为完成。
`envelope01.json` 仅量测本次接受轨迹离散点的实际碰撞网格包络，不称为全局最小厢体或额外连续扫掠证明。

## 交付与复现

本地交付目录：`outputs/receiver_all_20261102/`。

- `index.html`：结果、尺寸图及回放入口。
- `run01_replay.html`：自包含离线三维回放，无需服务或远端资产。
- `run01_replay.zip`：HTML、内嵌数据、快照、计划、原生请求/返回、搜索 trace、逐箱完成回执及来源记录。
- `run01_result.json`、`run01_replay.json`、`browser_run01/checks.json`：结果和检查证据。
- `commands/run01_command.sh`：实际运行命令。
- `delivery_checks.json`、`delivery_manifest.json`：离线包完整性及交付文件 SHA256。

HTML SHA256：`f3612caa43a410970afb85e123c02347a234028762dd2599f6c73581c87d6aaa`。
完整记录 ZIP SHA256：`673b85c103a181cf2757b1eb92d4382762c9866e51b36a91cc76c904568bc85f`。
本地与服务器哈希一致，ZIP 全条目 CRC 检查通过；交付入口链接检查通过。
生成的回放、快照和私有几何按既有规则忽略，不提交到公共 Git 仓库。

复用原有环境和 worker，运行参数为 `--all-cartons --carton-seconds 600 --task-seconds 7200 --connection-seconds 100 --solver-seconds 6 --rpc-seconds 90 --ik-seeds 8 --max-grasps 24 --search-trace`。
快照与初态取 `outputs/lab_prototype_20261031/candidate03/`；复现必须使用新输出目录，不能覆盖本次记录。
导出使用 `tools/export_eco65_coupled_replay.py`，实际浏览器检查使用 `tools/check_eco65_coupled_replay_browser.py`；具体命令随交付保存。

## 明确边界

本次使用冻结的名义场景。已有探针 TCP 标定的留出检查通过，但视觉对地面绑定残差 −4.576 mm 超出 3 mm 阈值，未把该观测作为本次规划输入，也不声称视觉闭环成功。
理想接收和检查理想出料不是物理输送验证。`planning_only=True`、`physical_execution=NOT_RUN`、`execution_ready=false`。
没有扩展到 5 列完整卸箱、更多层、移动基座、动力学或硬件执行；不将有限搜索结果解释为全局可达性结论。
历史中断 batch04 的 1 箱回执已恢复并单独归档；不计入本次 16/16。
