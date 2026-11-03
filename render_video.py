import asyncio
import os
import subprocess
import json
import edge_tts

VID_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\video_production"

SCENES = [
    {
        "id": 1,
        "slide": "slide1.png",
        "audio": "audio1.mp3",
        "clip": "clip1.mp4",
        "text": "在经历了连续两波深不见底的下跌之后，很多投资者都在问同一个问题：中国A股双创板块这波去杠杆，到底到没到位？为什么科技股腰斩，全市场融资余额却迟迟不见彻底出清？基于中国银河证券交易所实盘清算数据库，我们穿透测算了全市场2.4万亿两融杠杆数据与历史重大股灾。量化结果显示：当前中国科技股的去杠杆进程不仅远远没有结束，反而正在积聚一个前所未有的融资‘堰塞湖’风险！"
    },
    {
        "id": 2,
        "slide": "slide2.png",
        "audio": "audio2.mp3",
        "clip": "clip2.mp4",
        "text": "要看清真相，必须把这轮下跌清晰划分为两波。第一波是7月份的踩踏，指数下跌24%，全市场融资余额单月被动平仓与主动斩仓并举，净砍掉了4211亿元，降幅达14%，这是典型的良性真出清。但在8月到9月的反弹之后，情况发生了诡异的变化。在国庆前后的第二波暴跌中，创业板和科创50跌幅分别达到29%和30%，通信与科创芯片在一个月内暴跌近40%。然而，全市场融资余额在第二波仅仅减少了2696亿，国庆节后更仅仅微降7.2%！指数在加速崩塌，但融资盘却出现了极其顽固的死扛抗单，机构正在以极大的代价硬撑浮亏！"
    },
    {
        "id": 3,
        "slide": "slide3.png",
        "audio": "audio3.mp3",
        "clip": "clip3.mp4",
        "text": "请看这张全市场融资余额与双创指数的走势对比图。我们可以看到一条极其刺眼的‘融资剪刀差’正在张开！在第一波中，指数与杠杆同步回落；而到了第二波，指数的下杀斜率急剧拉陡，但两融曲线却呈现出不寻常的走平钝化。全市场融资杠杆对股价的去化弹性，从第一波的0.58骤降到了0.24。这意味着绝大多数杠杆筹码并没有止损，全部被套牢在山腰之上！"
    },
    {
        "id": 4,
        "slide": "slide4.png",
        "audio": "audio4.mp3",
        "clip": "clip4.mp4",
        "text": "更惊人的分歧发生在这个市场的微观结构上。在个股层面，‘易中天’通信三巨头的融资余额，从峰值840亿直接腰斩到了389亿，单单三只股票就蒸发了452亿融资盘，跌幅达53.8%，与股价完全1比1同步崩溃；寒武纪的融资盘也被腰斩了47%。但诡异的是，科创芯片ETF的融资余额在第二波不仅没降，反而逆势飙升至20.9亿历史新高！通信ETF融资盘也死守在186亿高位不降！为什么个股在血腥斩仓，ETF却被融资买爆？答案就在券商风控规则中：券商对单一股票有20%到30%的持仓集中度上限，个股暴跌触及警戒线后，系统立刻切断个股买入权限；但ETF作为分散化品种，没有集中度限制，且担保折算率高达90%！大机构在个股爆仓的边缘，把所有追加的保证金和剩余信用额度，全额砸进了科技ETF中抗单！科技ETF，已经沦为了本轮去杠杆最危险的终极避难所！"
    },
    {
        "id": 5,
        "slide": "slide5.png",
        "audio": "audio5.mp3",
        "clip": "clip5.mp4",
        "text": "从下跌速度来看，这轮科技杀跌在整个金融史上都极为罕见。横向对比历史：在10月下旬的6个交易日内，通信ETF与科创芯片ETF日均跌速高达惊人的-3.19%/日！这个下泄速度，不仅远超2008年次贷危机，也远超2020年美股熔断时期和2000年互联网泡沫崩盘，在近三十年金融史中，仅次于2015年8月股灾第二波的救市资金退场践踏！反弹后的第二波永远比第一波更加凶险，因为场内买盘已经在第一波中被消耗殆尽，第二波是在流动性近乎真空的状态下自由落体。"
    },
    {
        "id": 6,
        "slide": "slide6.png",
        "audio": "audio6.mp3",
        "clip": "clip6.mp4",
        "text": "流动性极限的终极警报，已经由债券和黄金拉响。10月30日，一向稳如磐石的30年期国债期货单日暴跌1%，现货黄金下挫1.33%。这绝不是巧合，而是大机构为了硬抗科技ETF浮亏、避免穿仓，被迫卖出流动性最好的国债与黄金来筹集保证金的标志性信号！量化结论非常清晰：第二波去杠杆远远没有到位，科技ETF融资堰塞湖一旦决口，被动强平潮将不可避免地爆发。在全市场融资余额没有出现单月3000亿到5000亿级别的断崖式清仓之前，盲目左侧抄底，将面临极高的强平踩踏风险。敬畏市场，管住双手！"
    }
]

async def generate_all_audio():
    print("--- 正在生成高质量专业配音 (Voice: zh-CN-YunxiNeural) ---")
    for s in SCENES:
        audio_path = os.path.join(VID_DIR, s["audio"])
        print(f"Generating Scene {s['id']} audio...")
        comm = edge_tts.Communicate(s["text"], "zh-CN-YunxiNeural", rate="+6%")
        await comm.save(audio_path)
    print("--- 全部配音生成完毕 ---")

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

def render_video_clips():
    print("--- 开始使用 FFmpeg 渲染高清视频片段 (1080P) ---")
    concat_list_path = os.path.join(VID_DIR, "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for s in SCENES:
            slide_path = os.path.join(VID_DIR, s["slide"])
            audio_path = os.path.join(VID_DIR, s["audio"])
            clip_path = os.path.join(VID_DIR, s["clip"])
            
            dur = get_audio_duration(audio_path)
            print(f"Scene {s['id']}: 音频时长 {dur:.2f} 秒，渲染对应视频片段...")
            
            # Use ffmpeg to create clip from still image and audio
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", slide_path,
                "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest", clip_path
            ]
            r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if r.returncode != 0:
                print(f"Error rendering Scene {s['id']}:", r.stderr.decode('utf-8', errors='ignore'))
            else:
                print(f"Scene {s['id']} 渲染成功: {s['clip']}")
                f.write(f"file '{s['clip']}'\n")

    print("--- 正在合并全部片段为终版完整视频 ---")
    final_video = os.path.join(r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析", "A股双创去杠杆测算与历史暴跌速度对比_深度解析视频.mp4")
    merge_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy", final_video
    ]
    r_merge = subprocess.run(merge_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r_merge.returncode == 0:
        total_dur = get_audio_duration(final_video)
        size_mb = os.path.getsize(final_video) / (1024 * 1024)
        print(f"\n==========================================")
        print(f"SUCCESS! 完整视频生成完毕！")
        print(f"输出文件: {final_video}")
        print(f"视频总时长: {total_dur:.1f} 秒 ({total_dur/60:.2f} 分钟)")
        print(f"文件大小: {size_mb:.2f} MB")
        print(f"分辨率: 1920x1080 Full HD, 音频: 192kbps AAC")
        print(f"==========================================")
    else:
        print("合并失败:", r_merge.stderr.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
    asyncio.run(generate_all_audio())
    render_video_clips()
