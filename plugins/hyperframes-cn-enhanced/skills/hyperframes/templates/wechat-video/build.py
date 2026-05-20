import argparse
import asyncio
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib import request

try:
    import edge_tts
except ImportError:
    edge_tts = None

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = Path(__file__).resolve().parent
RUNS_DIR = ROOT / "runs"


def run_command(args):
    return subprocess.run(args, capture_output=True, text=True, check=False)


def command_exists(command):
    return shutil.which(command) is not None


def slugify(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "wechat-video"


def parse_dotenv(path):
    values = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        values[key] = value
    return values


def load_dotenv_values():
    values = {}
    values.update(parse_dotenv(ROOT / ".env"))
    values.update(parse_dotenv(TEMPLATE_DIR / ".env"))
    for key in (
        "EDGE_TTS_VOICE",
        "EDGE_TTS_RATE",
        "EDGE_TTS_VOLUME",
        "EDGE_TTS_PITCH",
        "VIDEO_BRAND_TEXT",
        "VIDEO_SCENE_AUDIO_BUFFER",
        "VIDEO_MIN_SCENE_DURATION",
        "VIDEO_CN_FONT_PATH",
    ):
        if key in os.environ:
            values[key] = os.environ[key]
    return values


def parse_float(value, fallback):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def default_cn_font_path():
    candidates = [
        "/mnt/c/Windows/Fonts/NotoSansSC-VF.ttf",
        "/mnt/c/Windows/Fonts/msyh.ttc",
        "/mnt/c/Windows/Fonts/simsun.ttc",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return ""


def load_env_defaults():
    env = load_dotenv_values()
    return {
        "voice": env.get("EDGE_TTS_VOICE", "zh-CN-XiaoxiaoNeural"),
        "rate": env.get("EDGE_TTS_RATE", "+20%"),
        "volume": env.get("EDGE_TTS_VOLUME", "+0%"),
        "pitch": env.get("EDGE_TTS_PITCH", "+0Hz"),
        "brand_text": env.get("VIDEO_BRAND_TEXT", "").strip(),
        "scene_audio_buffer": parse_float(env.get("VIDEO_SCENE_AUDIO_BUFFER"), 0.35),
        "min_scene_duration": parse_float(env.get("VIDEO_MIN_SCENE_DURATION"), 4.5),
        "cn_font_path": env.get("VIDEO_CN_FONT_PATH", default_cn_font_path()).strip(),
    }


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def update_manifest(run_dir, **changes):
    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists():
        manifest = read_json(manifest_path)
    else:
        manifest = {}
    manifest.update(changes)
    manifest["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    write_json(manifest_path, manifest)


def preflight():
    checks = {
        "python": True,
        "edge_tts": edge_tts is not None,
        "ffprobe": command_exists("ffprobe"),
        "npx": command_exists("npx"),
    }
    missing = [name for name, ok in checks.items() if not ok]
    return checks, missing


def create_run_dir(slug):
    date = dt.datetime.now().strftime("%Y%m%d")
    run_dir = RUNS_DIR / f"wx-{date}-{slugify(slug)}"
    for child in ["img", "audio", "video"]:
        (run_dir / child).mkdir(parents=True, exist_ok=True)
    return run_dir


def parse_wechat_url(url):
    payload = json.dumps({"blogUrl": url}).encode("utf-8")
    req = request.Request(
        "https://ideaflow-article-to-markdown.hf.space/resolve/mark",
        data=payload,
        headers={
            "Referer": "https://ideaflow-article-to-markdown.hf.space/",
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["data"]["markdown"]


def load_article(args):
    if args.article:
        return Path(args.article).read_text(encoding="utf-8")
    if args.url:
        return parse_wechat_url(args.url)
    sample = TEMPLATE_DIR / "examples" / "article.sample.md"
    return sample.read_text(encoding="utf-8")


def extract_basic_scene_plan(article):
    title_match = re.search(r"^#\s+(.+)$", article, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "微信文章视频"
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", article) if p.strip()]
    body = [p for p in paragraphs if not p.startswith("#")]
    selected = body[:4] if body else [title]
    scene_types = ["cinema-title", "showcase", "infographic-grid", "kinetic-quote"]
    scenes = []
    for idx, text in enumerate(selected, start=1):
        scenes.append({
            "id": f"s{idx:02d}",
            "type": scene_types[(idx - 1) % len(scene_types)],
            "title": title if idx == 1 else text[:24],
            "visual_source": "generated layout",
            "key_points": [text[:80]],
            "narration_intent": "summarize the key point clearly",
        })
    return {"title": title, "slug": slugify(title), "format": "portrait", "scenes": scenes}


def create_narration(scene_plan, settings):
    segments = []
    for scene in scene_plan["scenes"]:
        key_point = scene["key_points"][0] if scene.get("key_points") else scene["title"]
        text = key_point.replace("\n", " ")
        segments.append({
            "scene_id": scene["id"],
            "filename": f"{scene['id']}.mp3",
            "text": text[:90],
        })
    return {"voice": settings["voice"], "rate": settings["rate"], "segments": segments}


def build_image_prompts(scene_plan):
    prompts = []
    for scene in scene_plan.get("scenes", []):
        image_prompt = scene.get("image_prompt")
        if not image_prompt:
            visual_source = scene.get("visual_source", "cinematic editorial background")
            title = scene.get("title", "")
            key_point = scene.get("key_points", [""])[0]
            image_prompt = (
                "Create a 1080x1920 vertical editorial background image for a Chinese short video. "
                f"Scene title: {title}. Key point: {key_point}. Visual direction: {visual_source}. "
                "No readable text, no logos, no watermark. Leave clean negative space for large Chinese headline overlays. "
                "High contrast, cinematic lighting, suitable for a fast News Flash financial/social video."
            )
        prompts.append({
            "scene_id": scene["id"],
            "filename": f"{scene['id']}.png",
            "prompt": image_prompt,
        })
    return prompts


def measure_audio(path):
    result = run_command(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return float(result.stdout.strip())


async def generate_audio(run_dir, narration, settings):
    if edge_tts is None:
        raise RuntimeError("edge-tts is not installed. Run: pip install edge-tts")
    results = []
    for segment in narration["segments"]:
        output = run_dir / "audio" / segment["filename"]
        voice = narration.get("voice", settings["voice"])
        rate = narration.get("rate", settings["rate"])
        metadata = {
            "scene_id": segment["scene_id"],
            "text": segment["text"],
            "voice": voice,
            "rate": rate,
            "volume": settings["volume"],
            "pitch": settings["pitch"],
        }
        sidecar = output.with_name(f"{output.name}.json")
        try:
            reusable = output.exists() and sidecar.exists() and read_json(sidecar) == metadata
        except json.JSONDecodeError:
            reusable = False
        if not reusable:
            tts = edge_tts.Communicate(
                segment["text"],
                voice,
                rate=rate,
                volume=settings["volume"],
                pitch=settings["pitch"],
            )
            await tts.save(str(output))
            write_json(sidecar, metadata)
        results.append({
            "scene_id": segment["scene_id"],
            "filename": segment["filename"],
            "audio_dur": round(measure_audio(output), 2),
        })
    return results


def build_timeline(audio_results, settings):
    current = 0.0
    timeline = []
    buffer = max(settings["scene_audio_buffer"], 0.0)
    min_scene = max(settings["min_scene_duration"], 0.0)
    for item in audio_results:
        duration = max(item["audio_dur"] + buffer, min_scene)
        timeline.append({
            "scene_id": item["scene_id"],
            "filename": item["filename"],
            "start": round(current, 2),
            "duration": round(duration, 2),
            "audio_dur": item["audio_dur"],
        })
        current += duration
    for idx in range(len(timeline) - 1):
        end = timeline[idx]["start"] + timeline[idx]["duration"]
        if end > timeline[idx + 1]["start"]:
            timeline[idx]["duration"] = round(timeline[idx + 1]["start"] - timeline[idx]["start"] - 0.01, 2)
    return timeline


def prepare_font(run_dir, settings):
    font_path = Path(settings.get("cn_font_path", ""))
    if not font_path.exists():
        return ""
    fonts_dir = run_dir / "video" / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    target = fonts_dir / font_path.name
    if not target.exists():
        shutil.copy2(font_path, target)
    font_format = "truetype"
    if target.suffix.lower() in {".ttc", ".otc"}:
        font_format = "truetype-collection"
    return (
        "@font-face {\n"
        "  font-family: \"HF Chinese\";\n"
        f"  src: url(\"fonts/{target.name}\") format(\"{font_format}\");\n"
        "  font-weight: 100 900;\n"
        "  font-style: normal;\n"
        "  font-display: swap;\n"
        "}\n"
    )


def image_src_for_scene(run_dir, scene):
    image = str(scene.get("image") or scene.get("image_path") or "").strip()
    if not image:
        return ""
    if image.startswith(("http://", "https://")):
        return image

    image_path = Path(image)
    if image_path.is_absolute():
        source = image_path
    else:
        source = run_dir / image_path
        if not source.exists():
            source = ROOT / image_path

    if source.exists() and source.is_file():
        img_dir = run_dir / "img"
        img_dir.mkdir(parents=True, exist_ok=True)
        target = img_dir / source.name
        if source.resolve() != target.resolve() and not target.exists():
            shutil.copy2(source, target)
        return f"../img/{target.name}"

    return image if image.startswith("../") else f"../{image}"


def render_templates(run_dir, scene_plan, timeline, settings):
    styles = (TEMPLATE_DIR / "video" / "styles.css.j2").read_text(encoding="utf-8")
    index_template = (TEMPLATE_DIR / "video" / "index.html.j2").read_text(encoding="utf-8")
    styles = styles.replace("{{FONT_FACE}}", prepare_font(run_dir, settings))
    total_duration = round(max(item["start"] + item["duration"] for item in timeline), 2)
    scene_html = []
    audio_html = []
    brand_text = settings["brand_text"]
    brand_html = ""
    if brand_text:
        brand_html = f'<div class="brand-bar"><span>{html.escape(brand_text, quote=True)}</span></div>'
    for scene, time_item in zip(scene_plan["scenes"], timeline):
        scene_id = html.escape(str(scene["id"]), quote=True)
        scene_type = html.escape(str(scene["type"]), quote=True)
        scene_title = html.escape(str(scene["title"]), quote=True)
        key_point = scene["key_points"][0] if scene.get("key_points") else ""
        scene_key_point = html.escape(str(key_point), quote=True)
        audio_src = html.escape(f"../audio/{time_item['filename']}", quote=True)
        audio_duration = round(min(time_item.get("audio_dur", time_item["duration"]) + 0.05, time_item["duration"]), 2)
        image_src = image_src_for_scene(run_dir, scene)
        image_html = ""
        image_class = ""
        if image_src:
            image_class = " scene-with-image"
            image_html = f'<img class="scene-bg-img" src="{html.escape(image_src, quote=True)}" alt="">'
        scene_html.append(
            f'<section id="{scene_id}" class="clip scene scene-{scene_type}{image_class}" '
            f'data-start="{time_item["start"]}" data-duration="{time_item["duration"]}" data-track-index="1">'
            f'{image_html}'
            f'{brand_html}'
            f'<div class="sc"><h1>{scene_title}</h1><p>{scene_key_point}</p></div></section>'
        )
        audio_html.append(
            f'<audio id="narr-{scene_id}" data-start="{time_item["start"]}" '
            f'data-duration="{audio_duration}" data-track-index="2" '
            f'src="{audio_src}" data-volume="1"></audio>'
        )
    transition_html = []
    for idx in range(len(timeline) - 1):
        next_start = timeline[idx + 1]["start"]
        duration = min(0.2, next_start)
        start = round(next_start - duration, 2)
        transition_html.append(
            f'<div id="transition-{timeline[idx]["scene_id"]}-{timeline[idx + 1]["scene_id"]}" '
            f'class="clip transition fade-transition" data-start="{start}" '
            f'data-duration="{duration}" data-track-index="15"></div>'
        )
    index_html = index_template.replace("{{TOTAL_DURATION}}", str(total_duration))
    index_html = index_html.replace("{{SCENES}}", "\n    ".join(scene_html + transition_html))
    index_html = index_html.replace("{{AUDIO_CLIPS}}", "\n  ".join(audio_html))
    (run_dir / "video" / "styles.css").write_text(styles, encoding="utf-8")
    (run_dir / "video" / "index.html").write_text(index_html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    parser.add_argument("--article")
    parser.add_argument("--scene-plan")
    parser.add_argument("--narration")
    parser.add_argument("--slug", default="wechat-video")
    args = parser.parse_args()

    settings = load_env_defaults()
    run_dir = create_run_dir(args.slug)
    checks, missing = preflight()
    update_manifest(run_dir, stage="preflight", checks=checks, edge_tts=settings)
    if missing:
        update_manifest(run_dir, stage="failed", error=f"Missing dependencies: {', '.join(missing)}")
        print(f"Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        return 1

    try:
        article = load_article(args)
        (run_dir / "article.md").write_text(article, encoding="utf-8")
        update_manifest(run_dir, stage="article_saved", source_url=args.url)

        if args.scene_plan:
            scene_plan = read_json(Path(args.scene_plan))
        else:
            scene_plan = extract_basic_scene_plan(article)
        write_json(run_dir / "scene-plan.json", scene_plan)
        update_manifest(run_dir, stage="scene_plan_written", scene_count=len(scene_plan["scenes"]))
        write_json(run_dir / "image-prompts.json", build_image_prompts(scene_plan))
        update_manifest(run_dir, image_prompt_count=len(scene_plan["scenes"]))

        if args.narration:
            narration = read_json(Path(args.narration))
        else:
            narration = create_narration(scene_plan, settings)
        write_json(run_dir / "narration.json", narration)
        update_manifest(run_dir, stage="narration_written")

        audio_results = asyncio.run(generate_audio(run_dir, narration, settings))
        timeline = build_timeline(audio_results, settings)
        write_json(run_dir / "timeline.json", timeline)
        update_manifest(run_dir, stage="timeline_written")

        render_templates(run_dir, scene_plan, timeline, settings)
        update_manifest(run_dir, stage="html_written", video_dir=str(run_dir / "video"))
        print(run_dir)
        return 0
    except Exception as exc:
        update_manifest(run_dir, stage="failed", error=str(exc))
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
