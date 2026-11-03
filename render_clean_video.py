import os
import subprocess

VID_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\video_production"
SLIDES_DIR = os.path.join(VID_DIR, "dynamic_slides")
SRC_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析"
AUDIO_FILE = os.path.join(VID_DIR, "机构死扛杠杆.m4a")
CONCAT_TXT = os.path.join(SLIDES_DIR, "dynamic_slides_timeline.txt")

OUT_VIDEO = os.path.join(SRC_DIR, "A股双创去杠杆测算_高频卡点对谈视频_无字幕纯净版.mp4")
OUT_SRT = os.path.join(SRC_DIR, "A股双创去杠杆测算_高频卡点对谈视频_无字幕纯净版.srt")
SRC_SRT = os.path.join(SRC_DIR, "A股双创去杠杆测算_NotebookLM对谈精编视频.srt")

# Copy/ensure matching subtitle file name
if os.path.exists(SRC_SRT):
    with open(SRC_SRT, "r", encoding="utf-8") as f_in:
        content = f_in.read()
    with open(OUT_SRT, "w", encoding="utf-8") as f_out:
        f_out.write(content)
    print("SRT copied to:", OUT_SRT)

cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", CONCAT_TXT,
    "-i", AUDIO_FILE,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "328.96",
    OUT_VIDEO
]

print("Rendering clean video without subtitles...")
r = subprocess.run(cmd, cwd=SLIDES_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if r.returncode == 0:
    sz = os.path.getsize(OUT_VIDEO) / (1024 * 1024)
    print(f"\n==========================================")
    print(f"SUCCESS! 无字幕纯净版视频渲染完毕！")
    print(f"视频路径: {OUT_VIDEO}")
    print(f"字幕路径: {OUT_SRT}")
    print(f"文件大小: {sz:.2f} MB")
    print(f"==========================================")
else:
    print("Error rendering clean video:", r.stderr[:1000])
