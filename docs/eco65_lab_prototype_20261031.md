# ECO65 实验室原理样机（2026-10-31）

本轮使用真实 ECO65-B、真实吸具、12 个物理吸盘和原相机总成。箱体固定
150 × 100 × 100 mm，一排深；箱底从统一工位地面 Z=0 开始，不再使用单独
180 mm 箱垛支撑台。1:4 是设备布置的初始参考，并非整机等比例缩小声明。

**当前验收未完成。** 固定安装的四列四层候选共 16 箱；`batch03` 同一状态链已确认
12 箱完整抓放及出料，其中包括一箱箱底 Z=0 的最低层箱。该批因重复传输整套世界导致
阶段预算消耗而停止，保留成功前缀和失败记录。修正后的 `batch04` 已从完整库存冷启动，
但 GPU 服务器随后断开全部 SSH 会话，端口 12985 拒绝连接。最后可见请求是首箱
`ideal_outfeed-40` 的 STARTED，尚未取回返回结果。不能声称 16/16 或将不同批次相加。

本地可直接打开的完整记录包目前是 `batch02` 的 **10 箱成功前缀与失败诊断**。
后续 12 箱批次的原始记录仍在服务器；其导出和下载是否完成无法确认。
四列四层及厢体尺寸保留为已做代表任务与部分整栈验证的候选，没有宣布为最终验收布局。

## 基线与入口

- 工作分支：`feat/v0.6-eco65-moveit2-native-single-carton`。
- 实施前工作提交：`6636771f3a5d702467748063c1a9f6b27b430291`。
- 只读参考提交：`4d191ecab065420e4b70c9b266c87654996bd91f`。
- 新配置：`configs/workcells/eco65_lab_prototype_v2.yaml`。
- 四列四层实际候选的完整参数另存于
  `configs/workcells/eco65_lab_prototype_4c4l_fixed_candidate_v2.yaml`，内容与
  candidate03 的冻结配置逐项相同。原运行使用初始配置加 CLI 覆盖；重新生成
  模型会产生新身份，不能直接复用本轮关节轨迹。
- 场景生成：`tools/build_eco65_quarter_prototype.py`；名称保留最初缩尺入口兼容，
  默认配置已改为上述 100 mm 箱型的实验室样机。
- 连续任务：`tools/run_eco65_coupled_cycle.py --all-cartons` → `BatchTask` →
  `CoupledTask`，不使用历史七阶段计划或 FANUC 关节轨迹。
- 统一机构：`coupled_conveyor_state()`，同时生成原生世界、USD 和回放对象。
- 本轮冻结模型身份为 `realman_eco65 / ECO65-B / eco65_arm`，法兰 `link_6`，
  任务 TCP `eco65_task_tcp`；沿用实际法兰到吸具 TCP 变换（Z 平移约 142.750 mm）。
  模型、工具、接触轮廓及碰撞策略的完整指纹保存在快照 `native_model.init.identity`，
  12 个物理吸盘保留，未缩放连杆、工具或相机。标定另用探针尖端 TCP。
- 历史 `eco65_quarter_prototype_v1.yaml` 是已被后续用户要求替代的 40 箱、75 mm
  箱高试案，仅保留历史入口，不是本轮验收布局。

## 坐标、尺寸与有界候选

原点是初始箱垛前面中心的地面投影，+X 入厢，+Y 向左，+Z 向上。外部实验台
只能通过全工位统一的 `T_W_D` 抬升。列中心由列数自动居中生成；箱垛宽度为
`Nc*100+(Nc-1)*5` mm，高度为 `Nl*100` mm。

| 项目 | 初始参考 / 历史值 | 本轮实现 |
|---|---|---|
| 箱型 | 缩尺试案 150×100×75 mm | 用户指定 150×100×100 mm |
| 箱垛底部 | 旧场景约 180 mm | Z=0；不保留隐藏支撑台 |
| 列层候选 | 3×4 对照 | 3×4、4×4、5×4、3×5、4×5，有限候选，未搜索不算通过 |
| 横带有效面 | 参考 1:4 布置 | X=-225…-50，Y=-275…275 mm |
| 横带行程 | 严格参考缩尺下限 50 mm | 用户指定 100…525 mm，初态继承 331.182794 mm |
| 纵带 | 参考 1:4 布置 | 刚性 700×150 mm，Y 中心 -200 mm，远端带面 150 mm |
| 接缝 | 上端固定 XY、远端滑移 | 横带与纵带 Ymin=-275 mm；有效带面端点计算 |
| 底盘 | 参考 1:4 布置 | 525×375×150 mm，中心 (-487.5,87.5,75) mm |
| 基座起点 | 新坐标名义安装位 | (-487.5,37.5,225) mm，绕 Z 安装角 π |
| 厢体初值 | 1600×575×675 mm 内净尺寸 | 完整五面板，宽高按有限候选调整，入口 X=-800 mm 敞开 |
| 名义落差 | 参考 50 mm | 12.5 mm，实际落差由释放箱底与带面计算 |
| 设备 | ECO65、吸具、相机及实际安装件 | 比例 1.0，不缩放模型、TCP、关节范围或相机内参 |

固定位置候选仍须满足底盘完整承托。作业中没有实现或使用移动基座；预留的
150 mm 调位能力仅是配置说明，不能据此声称移动基座卸箱通过。

675 mm 原始厢高与真实相机总成冲突：相机最高点约 932.156 mm；计入原生
2.4 mm 净空至少需要 934.556 mm。当前选取有限候选表中的 1050 mm，并额外
检查折臂采集姿态。宽度对照中，四列右端完整周期的已接受原生路点设备包络
需要约 490.092 mm 对称内宽，五列左端对照需要约 634.654 mm；两者均包含
真实工具和 J1 桅杆。采用 675 mm 内宽覆盖已测试边界。这些是指定路点的
网格包络测量，不是全局最小厢体或连续扫掠证明。

厢体包含地板、左右壁、顶板和 +X 端壁；12.5 mm 板厚向内净空间之外布置。
回放隐藏面板只改变显示，不改变原生碰撞世界。

## 工程改造与工艺

剪叉重新采用横带三层 185 mm 杆、纵带四层 135 mm 杆；杆、销轴、滑轨、支座
由固定长度关系生成。低端固定导轨与随动滑车分离。100 mm 时纵带倾角为负，
不把整个机构向下平移。新增 400×150 mm 刚性出料托盘随低端滑车平移，及其
明确实体支架；解决高位纵带末端接近入口时，整箱尚未完全越过入口的承托问题。
这些是原理样机工程设计，不是供应商已制造机构或动力学认证。

顶吸没有箱底高度门槛，仍检查顶面暴露、完整密封、实际 FK、附件、完整路径
及环境碰撞。前吸、内侧吸和顶吸的合法模板共同参与有限候选调度。选中杯组
优先采用更多完整密封杯；未启用吸盘保留真实几何，不要求全部 12 杯密封。

HIGH=`zb-12.5 mm`、LOW=`zb-100 mm-12.5 mm` 从抓取前八角点箱底冻结，越界
直接剔除。顶吸抬升使用独立 `TOP_LIFTED_TRANSVERSE_RECEIVER`，规划真实 +Z
抬升与 -X 转运，不冒充 HIGH/LOW。横带在附着抽离前到位，升降时机器人 q 固定。
J1 使用已有自由双向 v4 合同，不限制单调方向，不改写角度或端点。

释放后箱体保持世界位姿和身份，名义下落时机器人停止；落带箱体参与工具退出
检查。随后 `IDEAL_OUTFEED` 按真实支持面以不大于 10 mm 的有限步长检查 -Y、-X
整箱包络，直到整个箱体越过入口平面，最后才 `IDEAL_RECEIVER_DRAIN`。
该出料为理想运动学假设，不代表物理输送成功。

100 mm 横带低于 150 mm 纵带远端，出料时箱体会沿支撑包络升高。实际运行
`batch02` 的第 11 箱暴露出仅按落带位置选择退出距离的问题：
`carton_r00_l01_c00 ↔ part_002_lip` 间隙 2.131 mm，小于 2.4 mm；
第二个更远退出候选的出料检查通过，但重复检查耗尽共享阶段预算，不能计为完成。
该批主动停止并保留 10 箱已接受前缀。修复后，真实工具全部实体相对整条出料箱体
包络计算优先的向上退出目标，随后仍规划真实 LIN 并执行全部原生出料检查。
没有增大阶段超时、降低采样密度或放宽碰撞间隙。`batch03` 从完整库存重新冷启动，
不导入或拼接 `batch02` 轨迹。

`batch03` 的 L01_C03 出料原生检查多次 SUCCESS（例如 48.013 秒），但后续清空事件
仍因同一绝对阶段预算耗尽未被接受。修正为 `HELD_WORLD_TARGET_POSES_V2`：固定的 q、
附件状态、机构和非目标世界只传输一次，每一个原有 ≤10 mm 箱体采样位姿仍执行原生
支持面、机器人、工具、环境碰撞检查。端点、姿态、方向、全箱越过入口和退出前置条件
仍逐项校验；保留旧完整请求合同兼容。失败回放按绑定世界与实际失败采样位姿重建。
此修正通过 Python 与 C++ 定向检查并已编译，新的整栈运行因上述 SSH 中断尚无最终结果。

原生落带调试曾复现 libccd 对近共面凸体的 EPA 断言：第二箱实际 FK 残余转角
约 1e-10 rad，箱底与横带触面时 worker 中止。接收表面改用实际凸体的分离平面
界检查已有 0.4 mm 接触容差；未证明则拒绝。其他对象对仍使用 FCL，无新增
碰撞豁免；没有关掉断言、移动箱体端点或删除实际轨迹点。

## 验证与证据

生成文件与私有资产遵循 `.gitignore`，证据根目录为
`outputs/lab_prototype_20261031/`。下列代表任务不能相加成为整栈完成数。

| 实际运行 | 同链完整出料数 | 状态与可用证据 |
|---|---:|---|
| batch01 | 1/16 | 第二箱触带时 FCL 断言；原请求保留 |
| batch02 | 10/16 | L01_C00 出料工具间隙不足，随后预算耗尽；本地完整 HTML 与原始记录 ZIP |
| batch03 | 12/16 | 包含 L00_C01 地面箱；为修正重复场景序列化而停止，原始完整记录尚在服务器 |
| batch04 | 未取回确认数 | 新 worker、新冷启动；首箱出料请求开始后服务器连接中断，结果未知 |

`batch02` 实际墙钟 2449.488 秒；接受轨迹机器人运动时间 646.143 秒，机构展示时间
3.853 秒，名义下落 0.505 秒，理想出料展示 94.742 秒。显示停留时间另计 13.650 秒。
`batch03` 第 12 箱回执的累计墙钟为 2726.106 秒；这不是整批结束时间。
未取回 `batch04` 墙钟和轨迹总时长，不用其它批次代替。

四列候选的选择依据是：比三列对照增加一列，已覆盖两端、顶层、中层和地面箱的实际完整
周期；尚未完成同链全库存验收。五列左边界也存在实际可行周期，不能称五列全局不可达。
五列完整库存、三列五层、四列五层、其它固定安装位及作业中基座移动均未运行。

- `candidate01`：3×4，厢体 1600×675×1050 mm，名义固定基座。
  `cycle04` 原生完成顶层中箱完整抓放、检查出料、下一箱实际附着。
- `candidate03`：4×4，箱垛 150×415×400 mm，同一固定基座与厢体。
  `boundary01` 原生完成右端 L03_C00 完整周期，再附着 L03_C01。
- `candidate04`：5×4，箱垛 150×520×400 mm，同一固定基座与厢体。
  `boundary02` 原生完成左端 L03_C04 完整周期，再附着 L03_C02。
  这说明五列边界存在可行周期，并不证明五列整栈已通过，也不能称其全局不可达。
- `batch01` 是 candidate03 的新冷启动整栈运行；第一箱完成，第二箱落带时
  遇到上述 FCL 断言。已接受前缀和失败请求完整保留，没有计入第二箱完成。
- `mechanism04.json`：100、150、200、300、400、500、525 mm 机构几何检查通过。
  `environment01.json`：100、150、300、525 mm 加入完整静态环境后检查通过。
- `browser_native01`：离线 HTML 在实际浏览器加载并检查 FK、状态、原生请求
  世界、失败对象对和终态数量；通过不等于物理执行。

独立抓面诊断使用 `tools/check_eco65_prototype_face_cycle.py`，库存未删改：
`front_diagnostic02` 生成前吸杯组后，初态提案与 `trailer_roof` 相交，8 个有限
IK 初态种子中仅一个得到数值解，该解又因工具 `part_000` 与横带相交而拒绝；
终止于 `NATIVE_HOME_CANDIDATES_EXHAUSTED`，没有进入抓放后缀。
`inner_diagnostic02` 的原右端箱内侧抓面报 `LATERAL_CHANNEL_BLOCKED`，故无合法
内侧候选。两者完成数为 0，不加入整栈统计；不将有限种子失败或当前侧移通道未打开
解释为该抓面的全局不可达。前吸状态检查的真实场景与姿态另有离线诊断页。

初始全伸直提案因工具与顶板相交被拒绝。正式任务采用本次原生 IK 和碰撞
检查接受的初始姿态，作为新运动学仿真的初态；没有宣称机器人从被拒绝提案
运动到该姿态。后续每段均从实际已接受末态连接。

### 新标定及观测的实际边界

`prepare05 → capture06 → solve06 → validate06` 使用原有探针尖端 TCP，新生成
9 个 FK/几何触点和 6 张实际渲染图，留出检查 PASS，最大留出点误差 1.155 mm。
未复用旧布局外参。RGB-D 检出当前可见顶层四列，未把被遮挡低层称为独立检测。

但是，所得顶面估计向下偏约 4.576 mm，超过新场景的 3 mm 共同地面一致性
条件。`observed07/ground_consistency_failure.json` 明确拒绝生成观测规划世界，
没有抬高、下移箱堆或放宽条件。新增第二训练板位的有界恢复
`prepare08/capture08/solve08` 使用 15 个新触点、9 张新图，其多观测一致性
12.732 mm / 1.206° 超过 5 mm / 1°，保留失败，不采用该外参。

因此，本轮原生卸箱是**冻结名义场景的规划验证**；尚未完成视觉估计驱动的
地面一致性闭环。标定观测是在停稳状态独立设置的仿真采集，未宣称存在连接
各触点的标定机器人轨迹，也没有物理接触测量。

所有结果保持 `planning_only=True`、`physical_execution=NOT_RUN`、
`execution_ready=false`、`KINEMATIC_REPLAY`。未调用硬件 SDK。

## 提交与本地交付入口

实现已推送到工作分支，参考分支未改动：

- `e952585254062fbef9462dbd704094841f281128`：地面箱堆、联动机构、完整厢体和检查出料。
- `78479c88bc85a826ed49ee1f7a6d8e2ca6d234ca`：离线回放、尺寸和新探针 TCP 观测流程。
- `7bde09c93b46cac345c2ecdea6427ac71119f70e`：按完整出料包络计算空载工具退出。
- `5d9c5bf526571c467070f74616c2564a589aad56`：大型离线 JSON 回放及实际抓面诊断。
- `269ab67f8932771b6f1ad1f43ed73beaf6f90602`：固定世界出料采样合同、完整检查与记录去重。

证据目录内的 `index.html` 汇总实际可用文件：
`batch02_json_viewer.html` 为同次运行的 10 箱轨迹、事件及失败请求；
`batch02_failure_replay.zip` 保存原始计划、完整请求返回和搜索 trace；
`L01_C00_outfeed_failure.html` 为定位碰撞的专门视图；
`front_failure_viewer.html` 显示前吸诊断；`calibration_review.html` 显示新采集图和标定结果；
`dimensions_candidate03_final.png` / `.svg` 为含完整厢体的尺寸图。
HTML 内嵌 Three.js、模型与数据，可离线打开，不依赖本机服务或远端资产路径。
本地 ZIP 全条目完整性检查通过；交付入口的所有链接存在，已在实际 Edge 浏览器打开并
检查页面。`delivery_checks.json` 与 `delivery_manifest.json` 保存检查结果和文件哈希。
`commands/` 保留实际构建、各批原生运行、探针准备、图像采集、解算和观测世界构建命令。

新 worker SHA256 为
`e18f657822f6ada859b2c581cdd2589f62b73e09f6daa22ec322f0f3d69dddb6`；
`native_build07_observed.json` 保存断线前实际编译/原生检查输出与源码哈希。
`remote_interruption.json` 区分已确认回执和最后一次未确认请求；不生成替代轨迹。

## 复现入口

在现有 Python 环境中设置 `PYTHONPATH=src:tools`（Windows 用分号），私有资产
路径保持原样。不升级依赖。

```bash
python tools/build_eco65_quarter_prototype.py \
  --source outputs/rear200_receiver100_20261023/scene/snapshot.json \
  --output outputs/NEW_RUN/scene --columns 4 --layers 4 \
  --inner-width .675 --inner-height 1.05 --target-id carton_r00_l03_c00
python tools/run_eco65_coupled_cycle.py \
  --snapshot outputs/NEW_RUN/scene/snapshot.json \
  --home-candidate outputs/NEW_RUN/scene/home_candidate.json \
  --worker-command "$ECO65_WORKER" --output outputs/NEW_RUN/batch \
  --all-cartons --task-seconds 7200 --carton-seconds 600 \
  --connection-seconds 100 --solver-seconds 6 --rpc-seconds 90 \
  --ik-seeds 8 --max-grasps 24 --search-trace
python tools/export_eco65_coupled_replay.py \
  --snapshot outputs/NEW_RUN/scene/snapshot.json \
  --plan outputs/NEW_RUN/batch/plan.json.gz --run outputs/NEW_RUN/batch \
  --output outputs/NEW_RUN/replay.html
```

输出目录必须新建。失败批次使用实际 `latest_plan.json.gz` 导出，标记未完成。
服务器实际命令及构建日志归档于证据目录；`worker.sh` 使用已安装的项目前缀
加载 OMPL 插件，保留 MoveIt/MTC/Pilz/OMPL 原生生成链。

实际原生构建（复用既有 ROS Humble chroot，不安装或升级依赖）：

```bash
chroot /root/autodl-tmp/m710-moveit2-20260922/rootfs /bin/bash -lc '
  source /opt/ros/humble/setup.bash
  cmake --build /work-eco65-20261015/build-coupled-20261020 -j2 \
    --target m710_moveit_worker eco65_cycle_test
  cmake --install /work-eco65-20261015/build-coupled-20261020
  /work-eco65-20261015/build-coupled-20261020/eco65_cycle_test'
export ECO65_WORKER='chroot /root/autodl-tmp/m710-moveit2-20260922/rootfs /usr/bin/env M710_MOVEIT_INSTALL_PREFIX=/work-eco65-20261015/install-coupled-20261020 /bin/bash /work-eco65-20261015/ros2/m710_moveit_backend/worker.sh'
```

实际构建 worker SHA256：
`23af0318e7899c45e9ba8a24de3beb1369dce8c96e9761846ba3633a35e520a5`。
源码与构建记录见 `native_build06.json` 和 `logs/lab_build06_20261031.log`。
关闭 trace 的原生启动/状态检查另存 `capture_check09`。

本轮 Python 定向检查：
`python -m pytest tests/test_eco65_lab_prototype.py tests/test_eco65_transverse_process.py -q`
为 **33 passed**。原生合同/近共面支持检查 PASS；它们是合成定向检查，不计入
抓放完成数。离线代表任务浏览器检查 `browser_native03` 为 **1289 passed**，
包括隐藏面板不改碰撞世界、出料时 q 固定、原生轨迹与世界状态连续。
曾额外选跑旧 `test_eco65_native.py` 的小范围用例：27 通过、1 失败，失败为
旧 fixture 缺少已有必需字段 `init.collision_policy`；未将历史全量回归作为交付
门槛，也未声称这些旧用例全部通过。

出料退出包络修正增加两例字面几何回归，
`tests/test_eco65_empty_withdrawal.py` 为 **4 passed**；显式抓面诊断过滤回归
`tests/test_eco65_face_diagnostic.py` 为 **1 passed**。
10 箱失败前缀的完整 HTML 原先超过浏览器检查的 120 秒限制；改用独立 JSON 数据块
解析，并在解析后移除数据节点，保留所有记录。`browser_batch02_json` 实际通过
**3475** 项检查，用时 **30.711 秒**，终态 world=6、attached=0、completed=10。
这只是失败前缀的 UI 检查，不是新一批整栈成功证据。

出料紧凑合同新增 6 项 C++ 定向校验，通过当前原生构建；
`PYTHONPATH=src:tools python -m pytest tests/test_eco65_coupled_state.py tests/test_eco65_coupled_replay_sharing.py tests/test_eco65_outfeed_protocol.py -q`
为 **16 passed**。这包含修正旧 mock 缺少任务记录字段后的连续候选测试。
所有测试仅证明其各自范围；尚未取回新合同实际首箱出料结果，更未完成新批全库存验收。
