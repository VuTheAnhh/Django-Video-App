import subprocess
import os
import json
from django.conf import settings

def format_duration(value):
    """
    Format thời lượng video (giây) thành định dạng hh:mm:ss.
    """
    try:
        value = int(value) 
        hours = value // 3600
        minutes = (value % 3600) // 60
        seconds = value % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    except (ValueError, TypeError):
        return value

def video_encode(instance):
    try:
        # obj = Video.objects.filter(status="Pending").first()
        obj = instance
        if obj:
            obj.status = "Processing"
            obj.is_running = True
            obj.save()
            input_video_path = obj.video_file.path

            output_directory = os.path.join(os.path.dirname(input_video_path), f'hls_output_{obj.slug}')
            os.makedirs(output_directory, exist_ok=True)
            output_filename = os.path.splitext(os.path.basename(input_video_path))[0] + "_hls.m3u8"
            output_hls_path = os.path.join(output_directory, output_filename)
            output_thumbnail_path = os.path.join(output_directory, os.path.splitext(os.path.basename(input_video_path))[0] + "thumbnail.jpg")
            relative_output_thumbnail_path = os.path.relpath(output_thumbnail_path, settings.MEDIA_ROOT)
            print(relative_output_thumbnail_path)
            cmd_duration = [
                "ffprobe", 
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_streams",
                input_video_path
            ]

            result = subprocess.run(cmd_duration, shell=False, check=True, stdout=subprocess.PIPE)

            ouput_json = json.loads(result.stdout)
            video_length = None

            for stream in ouput_json["streams"]:
                if stream["codec_type"] == "video":
                    video_length = float(stream["duration"])
                    break
            print(video_length)

            cmd_thumbnail = [
                "ffmpeg",
                "-i",
                input_video_path,
                "-ss",
                "2",
                "-vframes",
                "1",
                "-q:v",
                "2",
                output_thumbnail_path,
            ]

            subprocess.run(cmd_thumbnail, check=True)

            cmd = []
            if obj.deep_encode:
                cmd = [
                    'ffmpeg',
                    '-i', input_video_path,   # Đầu vào
                    '-c:v', 'copy',            # Codec video: h264
                    '-c:a', 'aac',             # Codec âm thanh: aac
                    '-strict', 'experimental', # Cho phép codec experimental
                    '-b:a', '192k',            # Bitrate âm thanh
                    '-ac', '1',                # Mono audio
                    '-ar', '8000',             # Tần số lấy mẫu âm thanh
                    '-r', '25',                # Tỉ lệ khung hình
                    '-hls_time', '5',          # Thời gian mỗi file .ts
                    '-hls_list_size', '0',     # Không giới hạn số lượng file trong danh sách HLS
                    '-hls_base_url', '{{ dynamic_path }}/', # Đường dẫn cơ sở cho các file .ts
                    '-movflags', '+faststart',# Flags để video streaming nhanh chóng
                    '-y',                      # Tự động ghi đè file nếu tồn tại
                    output_hls_path 
                ]

            else:
                cmd = [
                        'ffmpeg',
                        '-i', input_video_path,
                        '-c:v', 'copy',
                        '-c:a', 'copy',
                        '-hls_time', '5',
                        '-hls_list_size', '0',
                        "-hls_base_url", "{{ dynamic_path }}/",
                        "-movflags", "+faststart",
                        '-y',
                        output_hls_path
                ]

            subprocess.run(cmd, check=True)

            obj.hls = output_hls_path
            obj.thumbnail = output_thumbnail_path
            obj.duration = format_duration(video_length)
            obj.status = "Completed"
            obj.is_running = False

            obj.save()

            print(f'HLS segments generated and saved at: {output_hls_path}')
        else:
            print('No video with status "Pending" found.')

    except Exception as es:
        print(es)