import os
import subprocess

VID_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\video_production"
SLIDES_DIR = os.path.join(VID_DIR, "dynamic_slides")
SRC_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析"
AUDIO_FILE = os.path.join(VID_DIR, "机构死扛杠杆.m4a")
SRT_FILE = os.path.join(SRC_DIR, "A股双创去杠杆测算_NotebookLM对谈精编视频.srt")
OUT_VIDEO = os.path.join(SRC_DIR, "A股双创去杠杆测算_高频卡点对谈精编视频.mp4")

# Timeline of 27 slides, total exactly 328.96s
timeline = [
    ("slide_01.png", 12.0),
    ("slide_02.png", 12.0),
    ("slide_03.png", 12.0),
    ("slide_04.png", 12.0),
    ("slide_05.png", 10.0),
    ("slide_06.png", 16.0),
    ("slide_07.png", 12.0),
    ("slide_08.png", 12.0),
    ("slide_09.png", 10.0),
    ("slide_10.png", 12.0),
    ("slide_11.png", 12.0),
    ("slide_12.png", 12.0),
    ("slide_13.png", 13.0),
    ("slide_14.png", 10.0),
    ("slide_15.png", 11.0),
    ("slide_16.png", 14.0),
    ("slide_17.png", 12.0),
    ("slide_18.png", 12.0),
    ("slide_19.png", 12.0),
    ("slide_20.png", 12.0),
    ("slide_21.png", 12.0),
    ("slide_22.png", 12.0),
    ("slide_23.png", 12.0),
    ("slide_24.png", 12.0),
    ("slide_25.png", 14.0),
    ("slide_26.png", 12.0),
    ("slide_27.png", 14.96),
]

concat_txt_path = os.path.join(SLIDES_DIR, "dynamic_slides_timeline.txt")
with open(concat_txt_path, "w", encoding="utf-8") as f:
    f.write("ffconcat version 1.0\n")
    for img, dur in timeline:
        f.write(f"file '{img}'\n")
        f.write(f"duration {dur}\n")
    # Last image repeated per ffconcat specification
    f.write(f"file '{timeline[-1][0]}'\n")

print("dynamic_slides_timeline.txt written successfully.")

# Subtitle path for ffmpeg on Windows: escape colon and backslashes
srt_escaped = SRT_FILE.replace("\\", "/").replace(":", "\\:")

sub_filter = (
    f"subtitles=filename='{srt_escaped}':"
    "force_style='FontName=Microsoft YaHei,FontSize=23,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2.5,Shadow=1,MarginV=30'"
)

cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_txt_path,
    "-i", AUDIO_FILE,
    "-vf", sub_filter,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "328.96",
    OUT_VIDEO
]

print("Rendering high-frequency dynamic video with hardcoded subtitles...")
r = subprocess.run(cmd, cwd=SLIDES_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if r.returncode == 0:
    sz = os.path.getsize(OUT_VIDEO) / (1024 * 1024)
    print(f"\n==========================================")
    print(f"SUCCESS! 终版高频卡点视频渲染完毕！")
    print(f"输出路径: {OUT_VIDEO}")
    print(f"文件大小: {sz:.2f} MB")
    print(f"==========================================")
else:
    print("Error rendering video:")
    print(r.stderr[:1000])
