# HyperFrames CN Enhanced

面向中文短视频生产的 HyperFrames 增强技能包。它在 HyperFrames HTML 视频创作能力之上，补充了中文旁白、微信公众号文章转视频、信息流快消视觉风格、生成式背景图、本地图片资产、可恢复模板工程等工作流说明与脚手架。

这个仓库不是一个传统应用项目，没有前端源码树、服务端入口或本地构建产物。它主要交付两类内容：

- `skill/`：技能源码与维护入口，包含 `SKILL.md`、参考文档、模板和示例。
- `plugins/hyperframes-cn-enhanced/`：Codex 本地插件打包目录，用于把技能作为本地插件安装或分发。

## 目录

- [项目定位](#项目定位)
- [核心能力](#核心能力)
- [仓库结构](#仓库结构)
- [安装与接入](#安装与接入)
- [快速开始](#快速开始)
- [技能工作流](#技能工作流)
- [微信公众号文章转视频模板](#微信公众号文章转视频模板)
- [环境变量](#环境变量)
- [验证与质量检查](#验证与质量检查)
- [维护指南](#维护指南)
- [常见问题](#常见问题)

## 项目定位

HyperFrames 的核心理念是：HTML 是视频的源文件。一个视频 composition 通常由以下部分组成：

- HTML：通过 `data-*` 属性描述 clip、scene、track、duration 和 media。
- CSS：负责视觉风格、版式、背景图、字幕、数据卡片和图文层级。
- GSAP timeline：负责入场、退场、转场、强调动画和节奏控制。
- HyperFrames CLI：负责 lint、inspect、validate、preview、render 等验证和渲染工作。

本仓库专注于中文内容创作场景，尤其是：

- 将微信公众号文章解析为适合短视频传播的场景结构。
- 使用 `edge-tts` 生成中文逐场景旁白。
- 按真实音频时长计算 timeline，减少黑屏、音频截断和 track 重叠。
- 为财经、科技、AI、资讯类内容提供信息流快消视觉方案。
- 用模板保存文章、场景规划、旁白、音频、timeline、HTML 和 manifest，便于失败后恢复。

## 核心能力

| 能力 | 说明 | 主要文件 |
| --- | --- | --- |
| HyperFrames composition 规则 | 约束 `data-duration`、`data-track-index`、`window.__timelines`、媒体播放、GSAP 时间线等关键规则 | [`skill/SKILL.md`](skill/SKILL.md) |
| 中文 TTS 工作流 | 逐场景拆分旁白，使用 `edge-tts` 生成 MP3，用 `ffprobe` 测量时长后生成 timeline | [`skill/references/tts-workflow.md`](skill/references/tts-workflow.md), [`skill/references/external-tts.md`](skill/references/external-tts.md) |
| 微信文章转视频 | 解析 `mp.weixin.qq.com` 文章，提取图片、标题、引用、数据点，规划 10-14 个短视频场景 | [`skill/references/wechat-article-video.md`](skill/references/wechat-article-video.md) |
| 信息流快消视觉 | 使用生成式背景图、强对比标题、三段式信息布局、数据卡片和图表表达 | [`skill/references/news-flash-images.md`](skill/references/news-flash-images.md) |
| 可恢复模板 | 自动生成 run 目录，保存 article、scene-plan、narration、timeline、audio、video 和 manifest | [`skill/templates/wechat-video/`](skill/templates/wechat-video/) |
| Codex 插件打包 | 通过 `.codex-plugin/plugin.json` 暴露本地插件元数据、能力描述、默认提示词和技能路径 | [`plugins/hyperframes-cn-enhanced/.codex-plugin/plugin.json`](plugins/hyperframes-cn-enhanced/.codex-plugin/plugin.json) |

## 仓库结构

```text
.
├── AGENTS.md
├── README.md
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── plugins/
│   └── hyperframes-cn-enhanced/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── hyperframes/
│               ├── SKILL.md
│               ├── references/
│               ├── templates/
│               ├── palettes/
│               └── scripts/
└── skill/
    ├── .env.example
    ├── SKILL.md
    ├── references/
    │   ├── external-tts.md
    │   ├── news-flash-images.md
    │   ├── tts-workflow.md
    │   └── wechat-article-video.md
    └── templates/
        └── wechat-video/
            ├── README.md
            ├── build.py
            ├── examples/
            ├── prompts/
            └── video/
```

### 关键目录说明

- [`skill/SKILL.md`](skill/SKILL.md)：技能主入口。这里应放最核心、最高频、非协商的规则，例如 composition 结构、timeline contract、layout before animation、媒体元素限制等。
- [`skill/references/`](skill/references/)：扩展参考文档。适合存放某一类任务的完整工作流，避免主技能文件过长。
- [`skill/templates/wechat-video/`](skill/templates/wechat-video/)：微信公众号文章转视频模板。包含构建脚本、prompt 模板、Jinja 风格 HTML/CSS 模板和示例输入。
- [`plugins/hyperframes-cn-enhanced/`](plugins/hyperframes-cn-enhanced/)：本地插件分发形态。发布或安装插件时使用这里的 `.codex-plugin/plugin.json` 和 `skills/`。
- [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json)：本地 marketplace 配置，声明 `hyperframes-cn-enhanced` 插件的位置和安装策略。

维护时建议优先修改 `skill/`，确认内容正确后再同步到 `plugins/hyperframes-cn-enhanced/skills/hyperframes/`。这样可以把“源码维护入口”和“插件打包产物”区分开。

## 安装与接入

### 方式一：作为 Codex 本地插件使用

仓库已经包含本地插件描述文件：

```text
plugins/hyperframes-cn-enhanced/.codex-plugin/plugin.json
```

插件元数据包括：

- 插件名：`hyperframes-cn-enhanced`
- 版本：`0.1.0`
- 分类：`Design`
- 技能路径：`./skills/`
- 主要能力：中文短视频、微信公众号文章转视频、`edge-tts` 旁白、News Flash 视觉、可恢复模板。

在支持本地插件 marketplace 的 Codex 环境中，可使用 [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) 指向本仓库内的本地插件目录。

### 方式二：作为独立技能维护

如果只需要维护技能内容，可以直接使用 [`skill/`](skill/) 目录作为技能源：

```text
skill/
├── SKILL.md
├── references/
└── templates/
```

这种方式适合开发和审阅技能文本。需要发布为插件时，再同步到 `plugins/hyperframes-cn-enhanced/skills/hyperframes/`。

## 快速开始

### 1. 查看技能主入口

```bash
sed -n '1,220p' skill/SKILL.md
```

重点关注：

- `data-*` 属性约定
- root composition 的 `data-duration`
- `window.__timelines` 注册
- video/audio 拆分规则
- layout before animation
- GSAP 可动画属性限制

### 2. 准备 TTS 环境

```bash
pip install edge-tts
edge-tts --list-voices
```

如果需要测量音频时长和验证最终视频音轨，还需要安装 FFmpeg，并确保 `ffprobe` 可用：

```bash
ffprobe -version
```

### 3. 复制环境变量示例

```bash
cp skill/.env.example skill/templates/wechat-video/.env
```

常用默认值：

```env
EDGE_TTS_VOICE=zh-CN-XiaoxiaoNeural
EDGE_TTS_RATE=+20%
EDGE_TTS_VOLUME=+0%
EDGE_TTS_PITCH=+0Hz
```

背景图默认使用 Codex 生图能力生成，并保存为本地 `img/` 资产。

### 4. 运行模板 smoke test

从仓库根目录执行：

```bash
python skill/templates/wechat-video/build.py \
  --article skill/templates/wechat-video/examples/article.sample.md \
  --slug sample
```

脚本会在 `skill/runs/wx-YYYYMMDD-sample/` 下生成：

```text
article.md
manifest.json
scene-plan.json
narration.json
timeline.json
img/
audio/
video/index.html
video/styles.css
```

### 5. 验证生成的 HyperFrames 项目

进入生成的 run 目录后执行：

```bash
npx hyperframes lint video
npx hyperframes inspect video --timeout 30000
npx hyperframes render video
ffprobe renders/output.mp4
```

目标结果：

- `lint` 无结构性错误。
- `inspect` 无关键布局溢出。
- 渲染出的 MP4 同时包含视频流和音频流。

## 技能工作流

### 1. 视觉身份与设计系统

创建新视频前，应先确认视觉身份：

1. 如果 composition 项目内存在 `design.md` 或 `DESIGN.md`，优先使用其中的品牌色、字体和限制。
2. 如果用户已经指定风格或情绪，选择最贴近的视觉 preset。
3. 如果没有任何设计输入，应先询问主题、明暗模式、品牌色和字体偏好。

不要在未确认视觉身份时随手使用 `#333`、`#3b82f6`、`Roboto` 等默认值。

### 2. Prompt expansion

除单场景作品和微小修改外，创建 composition 前应做 prompt expansion，把用户意图、视觉身份、节奏、场景结构和输出约束整理成一致的中间规格。这样后续写 HTML、生成旁白、找图和调动画时不会各走各的。

### 3. 场景规划

规划时需要先回答：

- 观众要经历什么信息路径？
- 哪些场景是快节奏信息点，哪些场景需要停留？
- 哪些 clip 是主视觉、哪些是音频、哪些是 overlay 或 transition？
- 最后一段音频结束时间是否被总时长覆盖？
- 是否有文章截图、数据、引用、对比结论需要被单独表现？

### 4. Layout before animation

先把每个场景的“最可见帧”写成静态 HTML/CSS，再添加 GSAP。

推荐容器模式：

```css
.scene-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 80px 48px;
  gap: 24px;
  box-sizing: border-box;
}
```

原则：

- 内容容器用 `width: 100%`、`height: 100%` 和 padding 控制安全边距。
- 不要用绝对定位硬塞正文容器。
- 顶部有 brand bar 时，内容容器的 `padding-top` 至少应能避开它。
- `gsap.from()` 或 `fromTo()` 只描述元素如何进入静态终点。

### 5. Timeline contract

必须满足：

- 所有 timeline 都使用 `{ paused: true }`。
- 每个 composition timeline 注册到 `window.__timelines["<composition-id>"]`。
- root composition 必须显式写 `data-duration`。
- clip 使用 `data-track-index`，不要使用 `data-layer`。
- duration 来自 `data-duration`，不要靠空 tween 撑时长。
- 不要在 `async`、`setTimeout`、Promise 回调里构建 timeline。

### 6. 音视频规则

视频元素必须静音，音频必须单独作为 `<audio>` clip：

```html
<video
  id="el-v"
  data-start="0"
  data-duration="30"
  data-track-index="0"
  src="video.mp4"
  muted
  playsinline
></video>

<audio
  id="el-a"
  data-start="0"
  data-duration="30"
  data-track-index="2"
  src="video.mp4"
  data-volume="1"
></audio>
```

不要调用 `play()`、`pause()` 或手动 seek，媒体播放由 HyperFrames 框架控制。

## 微信公众号文章转视频模板

模板目录：

```text
skill/templates/wechat-video/
```

它适合把微信公众号文章或本地 Markdown 文章转成竖屏短视频工程。

### 输入方式

```bash
# 使用本地文章
python skill/templates/wechat-video/build.py \
  --article path/to/article.md \
  --slug my-topic

# 使用微信公众号文章 URL
python skill/templates/wechat-video/build.py \
  --url "https://mp.weixin.qq.com/..." \
  --slug my-topic

# 使用人工审阅过的场景计划和旁白稿
python skill/templates/wechat-video/build.py \
  --article path/to/article.md \
  --scene-plan path/to/scene-plan.json \
  --narration path/to/narration.json \
  --slug my-topic
```

当未提供 `--scene-plan` 或 `--narration` 时，脚本会从文章生成一个最小 smoke-test 草稿。正式生产时，应先由 Agent 或人工生成并审阅：

- `scene-plan.json`
- `narration.json`

### 输出目录

每次运行写入：

```text
skill/runs/wx-YYYYMMDD-<slug>/
├── article.md
├── manifest.json
├── scene-plan.json
├── narration.json
├── timeline.json
├── img/
├── audio/
└── video/
    ├── index.html
    └── styles.css
```

`manifest.json` 会记录当前阶段、依赖检查、TTS 设置和错误信息，便于失败后恢复。

### scene-plan.json 格式

```json
{
  "title": "short video title",
  "slug": "short-lowercase-slug",
  "format": "portrait",
  "scenes": [
    {
      "id": "s01",
      "type": "cinema-title",
      "title": "scene title",
      "visual_source": "generated image or article image or generated layout",
      "key_points": ["one concrete point"],
      "narration_intent": "what the voiceover should explain"
    }
  ]
}
```

推荐场景类型：

- `cinema-title`：片头、章节转场、收尾。
- `showcase`：展示文章截图或关键图片，图片必须完整显示。
- `infographic-grid`：展示统计数字、比例、结论矩阵。
- `comparison-bars`：展示模型、产品、方案、指标对比。
- `kinetic-quote`：展示文章核心观点或结论。

典型文章建议 10-14 个场景，并混合至少 4 种场景类型。不要连续重复同一种场景类型，避免做成单调图片轮播。

### narration.json 格式

```json
{
  "voice": "zh-CN-XiaoxiaoNeural",
  "rate": "+20%",
  "segments": [
    {
      "scene_id": "s01",
      "filename": "s01.mp3",
      "text": "短视频旁白，一到两句话。"
    }
  ]
}
```

规则：

- 每个场景一个旁白段落。
- 旁白要短，不要靠长句解释所有细节。
- 不根据字数估算最终时长。
- 生成音频后必须用 `ffprobe` 测量真实时长。

### timeline 计算规则

模板默认使用：

```python
scene_duration = max(actual_audio_dur + 2.0, 6.0)
```

含义：

- 每个场景至少 6 秒。
- 在真实音频时长后留 2 秒 buffer，给入场、停顿和转场留空间。
- 不裁剪音频来适配场景，应该延长场景或缩短文本后重新生成音频。

## 环境变量

示例文件：

- [`skill/.env.example`](skill/.env.example)
- [`skill/templates/wechat-video/.env.example`](skill/templates/wechat-video/.env.example)

支持的变量：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `EDGE_TTS_VOICE` | `zh-CN-XiaoxiaoNeural` | edge-tts 语音 |
| `EDGE_TTS_RATE` | `+20%` | 语速偏移 |
| `EDGE_TTS_VOLUME` | `+0%` | 音量偏移 |
| `EDGE_TTS_PITCH` | `+0Hz` | 音高偏移 |

模板的环境变量加载优先级：

1. `skill/.env`
2. `skill/templates/wechat-video/.env`
3. 当前进程环境变量

进程环境变量优先级最高。

## 验证与质量检查

本仓库没有本地 build 命令，也没有提交的自动化测试套件。Markdown 变更主要通过人工阅读和链接检查验证。

对模板生成的 HyperFrames composition，应在生成的 run 目录中执行：

```bash
npx hyperframes lint video
npx hyperframes validate video
npx hyperframes inspect video --timeout 30000
npx hyperframes render video
ffprobe renders/output.mp4
```

### 检查重点

- root composition 是否有正确的 `data-duration`。
- 最后一个场景结束时间是否覆盖最后一段音频结束时间。
- 同一 `data-track-index` 上的 clip 是否重叠。
- `<audio>` 是否位于 root composition div 外部。
- 文章截图是否使用 `object-fit: contain`，避免裁切文字。
- `window.__timelines` 是否同步注册。
- 是否有隐藏场景导致 `inspect` 报无意义 overflow。
- 渲染 MP4 是否同时有视频流和音频流。

### 常见命令

```bash
# 检查 Markdown 链接目标是否存在，可按需手动核对
find . -maxdepth 4 -type f | sort

# 检查模板 smoke test
python skill/templates/wechat-video/build.py \
  --article skill/templates/wechat-video/examples/article.sample.md \
  --slug sample

# 检查生成视频工程
cd skill/runs/wx-YYYYMMDD-sample
npx hyperframes lint video
npx hyperframes inspect video --timeout 30000
```

## 维护指南

### 文档分层

建议按以下原则放置内容：

- 高频、核心、容易出错的规则放在 [`skill/SKILL.md`](skill/SKILL.md)。
- 任务型长流程放在 [`skill/references/`](skill/references/)。
- 可运行脚手架放在 [`skill/templates/`](skill/templates/)。
- 插件安装和分发元数据放在 [`plugins/hyperframes-cn-enhanced/.codex-plugin/plugin.json`](plugins/hyperframes-cn-enhanced/.codex-plugin/plugin.json)。

### 命名规范

- `skill/references/` 下使用 lowercase kebab-case，例如 `wechat-article-video.md`。
- 模板输出目录使用日期和 slug，例如 `wx-20260520-my-topic`。
- 音频文件按场景命名，例如 `s01.mp3`、`s02.mp3`。
- 场景 ID 使用稳定短 ID，例如 `s01`、`s02`。

### 修改主技能文件时

修改 [`skill/SKILL.md`](skill/SKILL.md) 前先确认是否只是某个细分场景的长说明。如果是，优先放到 `references/` 并在主技能里链接。

保留 front matter：

```yaml
---
name: hyperframes
description: ...
---
```

不要破坏 `name` 和 `description`，它们会影响技能发现和触发。

### 修改模板时

涉及 [`skill/templates/wechat-video/build.py`](skill/templates/wechat-video/build.py) 时，至少跑一次 sample：

```bash
python skill/templates/wechat-video/build.py \
  --article skill/templates/wechat-video/examples/article.sample.md \
  --slug sample
```

如果变更影响 HTML/CSS 模板，还应在生成目录中执行：

```bash
npx hyperframes lint video
npx hyperframes inspect video --timeout 30000
```

### 同步插件目录

如果 `skill/` 是源目录，`plugins/hyperframes-cn-enhanced/skills/hyperframes/` 是打包目录，那么发布前需要同步两者。同步后检查：

- `SKILL.md` 是否一致。
- `references/` 是否包含新增文档。
- `templates/` 是否包含新增或修改的模板文件。
- `.env.example` 是否同步。
- `plugin.json` 的描述和默认提示词是否仍然准确。

## 常见问题

### 这个仓库能直接运行一个网站或应用吗？

不能。它不是应用源码仓库，而是 HyperFrames 技能包和模板仓库。可运行的内容主要是 `skill/templates/wechat-video/build.py`，它会生成 HyperFrames composition 项目。

### 为什么要逐场景生成音频，而不是一个完整旁白文件？

逐场景音频更容易对齐动画、转场和画面节奏。每段音频有独立的 `data-start` 和 `data-duration`，lint 也更容易发现 track 重叠。如果用一个连续旁白文件，后续任何场景调整都会牵动全局时间轴。

### 渲染后没有声音怎么办？

优先检查：

1. `<audio>` 是否在 root composition div 外部。
2. `data-duration` 是否是明确秒数，而不是 `"auto"`。
3. `data-track-index` 是否合理，旁白通常使用 `2`。
4. `ffprobe renders/output.mp4` 是否显示音频流。

### 为什么文章截图不能用 `object-fit: cover`？

微信公众号文章截图通常包含正文、表格、对比图或 UI 截图。`cover` 会裁切边缘，导致文字不可读。文章图片展示应使用 `object-fit: contain`，再通过背景、阴影、overlay 和排版增强视觉效果。

### 出现 `overlapping_clips_same_track` 怎么办？

同一 track 上两个 clip 的时间发生重叠。常见原因是浮点边界，例如前一个 clip 结束于 `63.15`，后一个也从 `63.15` 开始。可将后一个 start 增加 `0.01`，或将前一个 duration 减少 `0.01`。

### 最后一段视频黑屏是什么原因？

通常是 root composition 的 `data-duration` 小于最后一个场景或最后一段音频的结束时间。总时长应按以下思路计算：

```python
total_duration = max(last_audio_end, last_scene_end) + 1.0
```

## 许可证

插件元数据声明许可证为 Apache-2.0。实际发布时请确保仓库根目录包含对应 LICENSE 文件，或在发布说明中补充许可证文本。
