import os
import sys
import subprocess
from pathlib import Path

input_folder = sys.argv[1]
output_folder = sys.argv[2]

os.makedirs(output_folder, exist_ok=True)

def get_duration(filename):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def split_and_encode(input_path, output_path, max_duration_sec=7200, use_gpu=False):
    duration = get_duration(input_path)
    num_parts = int(duration // max_duration_sec) + (1 if duration % max_duration_sec else 0)
    input_name = Path(input_path).stem

    for i in range(num_parts):
        start_time = i * max_duration_sec
        output_file = os.path.join(output_path, f'{input_name}_part_{i+1}.mp4')

        if use_gpu:
            codec = ['-c:v', 'h264_nvenc']
        else:
            codec = ['-c:v', 'libx264', '-preset', 'ultrafast']

        drawtext = (
            "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:"
            "text='@big_cock20':fontcolor=white:fontsize=30:"
            "box=1:boxcolor=black@0.5:boxborderw=5:x=w-tw-10:y=h-th-10"
        )

        command = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', input_path,
            '-t', str(max_duration_sec),
            '-vf', drawtext,
            *codec,
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',
            output_file
        ]

        subprocess.run(command)

# Process all .mp4 files in input_folder
for file in Path(input_folder).rglob("*.mp4"):
    split_and_encode(str(file), output_folder, use_gpu=False)
