import os
import edge_tts
import PIL.Image
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

async def create_voice(text, output_path):
    """Menghasilkan audio dengan proteksi tipe data."""
    clean_text = str(text) if text else "Harimau adalah raja rimba."
    print(f"[*] Menghasilkan audio: {output_path}")
    try:
        communicate = edge_tts.Communicate(clean_text, "id-ID-ArdiNeural")
        await communicate.save(output_path)
        await asyncio.sleep(1)
    except Exception as e:
        print(f"[!] Gagal membuat audio: {e}")

def build_long_documentary(audio_files, output_path):
    print("[*] Editor Agent: Merangkai video dokumenter 30 detik (Multi-Clip)...")
    
    final_clips = []
    bg_folder = "assets/raw_videos/"
    bg_files = sorted([f for f in os.listdir(bg_folder) if f.startswith('bg_')])

    for i, audio_p in enumerate(audio_files):
        bg_path = os.path.join(bg_folder, bg_files[i % len(bg_files)])
        
        if not os.path.exists(audio_p) or os.path.getsize(audio_p) < 100:
            continue

        try:
            audio_clip = AudioFileClip(audio_p)

            video_clip = VideoFileClip(bg_path).subclip(0, audio_clip.duration)

            segment = (video_clip.resize(height=854)
                       .crop(x_center=360, width=480)
                       .set_audio(audio_clip))
            
            final_clips.append(segment)
            print(f"[+] Segmen {i+1} Berhasil (Durasi: {audio_clip.duration:.2f}s)")
        except Exception as e:
            print(f"[!] Error segmen {i+1}: {e}")

    if not final_clips:
        print("[!] Tidak ada klip valid untuk digabung.")
        return

    print("[*] Menggabungkan klip bervariasi...")
    final_video = concatenate_videoclips(final_clips, method="compose")
    
    try:
        final_video.write_videofile(
            output_path, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            threads=1,
            preset='ultrafast'
        )
        print(f"[***] VIDEO SELESAI: {output_path}")
    except Exception as e:
        print(f"[!] Gagal Render: {e}")
    finally:
        for c in final_clips: c.close()