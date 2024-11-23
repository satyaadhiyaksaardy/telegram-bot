import os

RTSP_URL = os.getenv("RTSP_URL")

def execute_ffmpeg_command(output_file, idc, ids):
    """
    Execute the FFmpeg command to capture an image or video from RTSP stream.
    """
    cmd = f"ffmpeg -rtsp_transport tcp -y -i '{RTSP_URL}/mode=real&idc={idc}&ids={ids}' -vframes:v 1 {output_file}"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists
    os.system(cmd)
    return output_file

def capture_video(output_file, duration, idc, ids):
    """
    Capture a video from an RTSP stream using FFmpeg.
    """
    cmd = f"ffmpeg -rtsp_transport tcp -y -i '{RTSP_URL}/mode=real&idc={idc}&ids={ids}' -c copy -t {duration} {output_file}"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists
    os.system(cmd)
    return output_file