import os
import subprocess

VID_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\video_production"
AUDIO_FILE = os.path.join(VID_DIR, "机构死扛杠杆.m4a")
OUT_VIDEO = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\A股双创去杠杆测算_NotebookLM对谈精编视频.mp4"

# Timeline mapping from the 328.96s audio:
# 00:00 - 01:05 (65.0s): 开篇跳伞比喻 + 7月第一波真出清 (Slide 1: 封面大图)
# 01:05 - 01:38 (33.0s): 3.1 & 3.2 两波量化矩阵对比与弹性0.24 (Slide 2: 两波走势对比图 chart4)
# 01:38 - 02:20 (42.0s): 3.4节 33只半导体设备ETF全量验证 (Slide 3: 全市场剪刀差走势图 chart1)
# 02:20 - 03:38 (78.0s): 第6节 易中天腰斩 vs ETF创20.9亿新高与风控乾坤大挪移 (Slide 4: 个股vs ETF背离图 chart5)
# 03:38 - 04:16 (38.0s): 第4节 历史暴跌速度天梯，比美股熔断猛一倍 (Slide 5: 历史速度对比图 chart2)
# 04:16 - 05:28.96 (72.96s): 第5节 30年国债暴跌1%+黄金下挫，到没到位与悬念收尾 (Slide 6: 国债黄金流动性穿透图 chart3)

timeline = [
    ("slide1.png", 65.0),
    ("slide2.png", 33.0),
    ("slide3.png", 42.0),
    ("slide4.png", 78.0),
    ("slide5.png", 38.0),
    ("slide6.png", 73.0),
]

concat_txt_path = os.path.join(VID_DIR, "slides_timeline.txt")
with open(concat_txt_path, "w", encoding="utf-8") as f:
    f.write("ffconcat version 1.0\n")
    for img, dur in timeline:
        f.write(f"file '{img}'\n")
        f.write(f"duration {dur}\n")
    # Last image must be repeated per ffconcat spec
    f.write(f"file '{timeline[-1][0]}'\n")

print("slides_timeline.txt written.")

# Build ffmpeg command
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_txt_path,
    "-i", AUDIO_FILE,
    "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    OUT_VIDEO
]

print("Rendering video...")
r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if r.returncode == 0:
    sz = os.path.getsize(OUT_VIDEO) / (1024 * 1024)
    print(f"Render SUCCESS! Video size: {sz:.2f} MB")
    print(f"Saved to: {OUT_VIDEO}")
else:
    print("Error rendering video:", r.stderr)
