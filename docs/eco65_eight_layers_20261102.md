# ECO65 八层尝试（2026-11-02）

本次按用户要求，将已完成 4 列 × 4 层的场景扩为 **4 列 × 8 层，共 32 箱**，只尝试新增 L04–L07 的 16 箱。原有 L00–L03 全部保留原 ID、尺寸、位姿及支撑关系。没有把历史 16/16 与本次结果相加。

## 场景和实现

- 原工作基线：`b3fc308eb878c7cd4a3f71ec71086a03629b260a`。
- 只读参考：`4d191ecab065420e4b70c9b266c87654996bd91f`；本轮未修改参考分支。
- 八层/指定库存合同：`83a3eaf096ebd0e1f099c3eb67d3945757938341`。
- 原生合同测试修正：`a7caa0684f03e8b1beaa893b9b8d5f286ba30cbb`。
- 实际初始带高、无接受初态时的失败记录：`bf19a8417c431c964a52836a0bafe38694b2cf8d`。
- 前移安装位及阶梯承托：`5e19b5be45c382d23108ce195f375f9166c1469f`。
- 本次构建 worker SHA256：`ca6245026986f3f58c38ceb7e9ba5c4b4a9b18e3bfc537d4a0fe23cb403da625`。

单箱固定 150×100×100 mm；箱堆 X=0…150、Y=−207.5…207.5、Z=0…800 mm。底层直接位于地面。厢体内部 1600×675×1050 mm，保留地板、侧壁、顶板、封闭端及敞开入口的碰撞几何。

横带有效 550(Y)×175(X) mm，行程 100…525 mm；纵带 700×150 mm，远端带高 150 mm。机器人、工具、全部 12 个物理吸盘均未缩放。没有新增碰撞豁免、顶吸高度门槛或 J1 方向硬约束。

新增 `--all-cartons --target-layers 4 5 6 7`。选择范围只约束待卸目标，不删减世界对象。`SELECTED_CARTONS_DRAINED` 的成功条件要求指定集合全部完成、非指定库存保持原位、无附着箱体；Python 和原生连续任务合同均识别该目标。查看器明确区分指定库存和全部库存。

## 原安装位实际结果

配置：`configs/workcells/eco65_lab_prototype_4c8l_fixed_candidate_v2.yaml`。

基座固定在 (−487.5,37.5,225) mm、安装 yaw=π。重新生成 32 箱世界，采用上一运行的空载末 q 和实际 H=100 mm，重新进行本次原生状态/FK 检查。没有导入历史运动段。

| 运行 | 首目标 | 范围 | 规划墙钟 s | 本次完成 |
|---|---|---|---:|---:|
| run03 | L07_C00 | 新增 16 箱连续任务 | 513.339 | 0/16 |
| run04 | L07_C01 | 独立 180 s 首目标诊断 | 180.438 | 0 |
| run05 | L07_C02 | 独立 180 s 首目标诊断 | 180.447 | 0 |
| run06 | L07_C03 | 独立 180 s 首目标诊断 | 180.889 | 0 |

主运行结束为 `FIRST_CARTON_OR_CONTINUATION_BOUNDED_CANDIDATES_EXHAUSTED`。实际接受初态，但没有接受机器人运动、升降或附着事件；终态箱体 world=32、attached=0、completed=0。接受轨迹机器人时间和机构时间均为 0。

主运行生成 296 个合法接触几何候选，资源上限选取 24 个，三种升带同步位置共 72 个组合全部尝试。其余 272 个接触几何候选不在本轮搜索范围内。414 次原生调用中：READY 1、SUCCESS 5（状态检查和 FK）、升降拒绝 24、接触 IK 失败 384。其余三个首目标诊断均因绝对预算停止，不能称为穷尽所有候选。

具体原因：

1. 保持原空载 q 升至 525 mm 的候选被 `link_5 ↔ conveyor_transverse_prototype_belt` 相交拒绝。
2. 先接近/接触再升带的候选没有取得合格的最高层接触 IK。
3. 最高层箱底为 700 mm，普通前吸公式对应 H_high=687.5、H_low=587.5 mm，均超过机构 525 mm 上限。没有 clamp 或改写落差。

最高层顶吸仍允许生成；`TOP_LIFTED_TRANSVERSE_RECEIVER` 候选带高 525 mm、释放箱底 712.5 mm、候选落差 187.5 mm，**未实际接受或释放**。没有把该候选值报告为实际 12.5 mm 落差。L04–L06 未进入完整抓放搜索，其顶面仍被上层箱遮挡。以上不是全局不可达证明。

初始化环境问题另存：run01 的新碰撞资源未复制至 chroot 导致 `COLLISION_GEOMETRY_MISSING:base_link`；补齐资源后，run02 使用旧 q 却未继承实际带高，出现 `part_000 ↔ 横带` 碰撞。随后改为 H=100 mm；同时修复无接受初态时失败 checkpoint 序列化。上述初始化失败均不计为卸箱尝试成功。

## 前移 200 mm 的新安装位

用户追加要求后，沿 +X 前移 200 mm，基座改为 **(−287.5,37.5,225) mm**。箱堆、厢体、底盘、横纵带保持原位；这是不同固定安装位的新仿真，不是已执行的基座移动。

新配置：`configs/workcells/eco65_lab_prototype_4c8l_forward200_v2.yaml`。

140×140 mm 上安装板前缘位于 X=−217.5 mm，比原底盘前缘 −225 mm 超出 7.5 mm。新增阶梯承托：140×140×60 mm 下支座中心 (−295,37.5,180) mm，完整落在底盘上；140×140×15 mm 上安装板中心 (−287.5,37.5,217.5) mm。上下件接面 Z=210 mm，机器人安装面仍为 Z=225 mm。两实体进入统一世界、碰撞和导出。它是新增工程几何，不宣称完成结构承载验证。

旧 q 平移到新安装位时被 `link_5 ↔ carton_r00_l04_c02` 相交拒绝。有限初始化扫描取得 J1=−3 rad、其余关节保持原值的空载状态，原生状态/FK 检查通过。此状态用于独立新仿真；没有声称旧姿态到新姿态的运动或基座移动已经执行。

run03 的 `--initial-mode inherited_state` 在此用于锁定所提供的新仿真 q、禁止初始化时另选姿态；候选文件注明 `CURRENT_NATIVE_EMPTY_INITIAL_STATE_SCAN`。旧通用字段的 `EXACT_SUPPLIED_PREVIOUS_TERMINAL_Q` 名称不应解释为跨安装位的已执行连接，实际没有这样的运动。

前移后的主运行 run03 仍为 **0/16**，终态 world=32、attached=0、completed=0，无接受机器人段、机构段或事件。规划墙钟 **525.511 s**，接受机器人运动及机构时间均为 0。生成 296 个接触几何候选，本轮选取 24 个并尝试全部 72 个同步组合；272 个未选候选没有搜索。原生 414 次调用：READY 1、SUCCESS 5（状态/FK）、升降拒绝 24、接触 IK 失败 384。

| 运行 | 首目标 | 范围 | 墙钟 s | 完成 |
|---|---|---|---:|---:|
| run01 | L07_C00 | 原姿态初始化拒绝 | 24.003 | 无接受初态 |
| run02 | L07_C00 | 初始化回退 IK 失败 | 26.002 | 无接受初态 |
| run03 | L07_C00 | 新空载初态的新增 16 箱任务 | 525.511 | 0/16 |
| run04 | L07_C01 | 独立 180 s 首目标诊断 | 180.448 | 0 |
| run05 | L07_C02 | 独立 180 s 首目标诊断 | 180.569 | 0 |
| run06 | L07_C03 | 独立 180 s 首目标诊断 | 180.553 | 0 |

主运行提前升带分支被 `part_000 ↔ conveyor_longitudinal_prototype_belt` 相交拒绝；先接近/接触再升带分支未找到最高层接触 IK。三个独立首目标诊断也未完成，分别受绝对预算限制；不将它们和主运行合并计数。

额外检查新安装座与全行程机构的实际凸体，发现**独立于机器人姿态的工程干涉**：在 217.5、220、225、230 mm 带高样本处，`robot_mount_plate` 同时与横带带体和 `eco65_transverse_relief_frame` 有共同内部点，共 8 条记录。检查使用统一状态函数的真实凸体面约束，正的共同内切球半径证明实体交集；不是 AABB 重叠，也不把该半径当作 FCL 穿透深度。其他未采样高度不声称扫掠验证。

因此，虽然下支座完整落在底盘上，这个 +X 200 mm 安装方案**没有通过全行程机构适配**。上安装板前缘伸入横带区域 7.5 mm，不能仅靠换机器人 q 消除。未移动横带、截短真实机器人、删掉上安装板或新增豁免来制造通过。需要另行协调安装板/机器人底部与横带升降包络；本轮不擅自改变用户指定的设备位置。

这项实体检查属于新增定向几何诊断；已完成原生调用按原请求保留，不把后算几何诊断写成原生返回。提交 `60d0da5326025d53a73c7684598d91e775abc20c` 增加对应检查及专用查看器面板，明确“非原生运动请求”，能定位准确高度和两个实体，不添加伪造 RRT 或运动。

前移交付目录：`outputs/forward200_20261102/`。`index.html` 为结果入口；`failure_viewer.html` 显示主运行原生失败；`installation_viewer.html` 显示安装板干涉；`run01…06_replay.zip` 保存各次原生记录；初态扫描、命令和日志在 `auxiliary_evidence.tar.gz`。`dimensions_checked.png` 使用已检查空载姿态；最初的 `dimensions.png` 保留已被拒绝的旧姿态，仅作对照。

部分已关闭的导出文件经 SHA256 校验迁至服务器另一文件系统，并在原路径保留符号链接；原生记录未删除。对应 relocation 清单随交付保存。HTML 的文字/初始视角修正版另存为查看入口，嵌入原始数据不变，来源哈希在 `viewer_derivatives.json` 中记录。

## 定向验证与复现

本轮相关 Python 检查：25 passed（`test_eco65_selected_layers.py`、`test_eco65_coupled_state.py`、`test_eco65_coupled_replay_sharing.py`）。其中包括保留安装板干涉的负例。原生 `eco65_cycle_test` PASS，覆盖新增指定库存目标。未运行历史全量回归。

原安装位四份 HTML 均实际用 Chrome 离线打开，分别通过 624 项检查；失败默认入口额外通过 624 项检查并目视核对碰撞对象。该 PASS 表示失败记录/模型/请求场景显示一致，不是任务完成。

前移主运行页面实际离线检查通过 627 项；安装板干涉入口通过 1388 项，实际截图核对准确的高度、实体 ID、32 箱世界以及“非原生运动请求”标识。几何检查结果为 `INTERFERENCE_FOUND`，不会因浏览器检查 PASS 而变成机构通过。

原安装位交付：`outputs/upper_layers_20261102/`，包含原生请求与返回 ZIP、真实失败搜索记录、四次结果、尺寸图和 `failure_viewer.html`。四个记录 ZIP 的全部条目 CRC 及与服务器 SHA256 一致性通过。大型生成文件和私有几何按规则忽略，不进入公共 Git。

复现使用仓库原有环境：

```bash
export PYTHONPATH=src:tools OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6:/usr/lib/x86_64-linux-gnu/libgcc_s.so.1
P=/root/autodl-tmp/envs/isaacsim-clean/bin/python
W='chroot /root/autodl-tmp/m710-moveit2-20260922/rootfs /usr/bin/env M710_MOVEIT_INSTALL_PREFIX=/work-eco65-20261015/install-coupled-20261020 /bin/bash /work-eco65-20261015/ros2/m710_moveit_backend/worker.sh'
# 先用 build_eco65_quarter_prototype.py 建立新输出目录，并将生成模型复制到 chroot 同相对路径。
$P tools/run_eco65_coupled_cycle.py --snapshot "$SCENE/snapshot.json" \
  --home-candidate "$HOME_CANDIDATE" --worker-command "$W" --output "$NEW_RUN" \
  --initial-mode inherited_state --all-cartons --target-layers 4 5 6 7 \
  --carton-seconds 600 --task-seconds 7200 --connection-seconds 100 \
  --solver-seconds 6 --rpc-seconds 90 --ik-seeds 8 --max-grasps 24 --search-trace
$P tools/export_eco65_coupled_replay.py --snapshot "$SCENE/snapshot.json" \
  --plan "$NEW_RUN/latest_plan.json.gz" --run "$NEW_RUN" --output "$NEW_REPLAY.html"
```

实际构建、初态、诊断与导出命令随各交付目录 `commands/` 保存。新运行必须使用新输出路径；失败计划采用 `latest_plan.json.gz`，完整成功才采用 `plan.json.gz`。

使用冻结名义场景，不声称本次新布局完成视觉闭环标定。`planning_only=True`、`physical_execution=NOT_RUN`、`execution_ready=false`；无 SDK、无硬件、无动力学输送验证。
