import os
import time
import random
import shutil
import numpy as np
import re
from datetime import datetime
from moviepy.editor import *
from moviepy.video.fx.all import speedx 

# ==============================================================================
# 🎛️ INSTAGRAM VIRAL SETTINGS (PEAK MEME AESTHETIC - EXACT MATCH)
# ==============================================================================

PARTS_PER_VIDEO = 1          
VIDEO_QUALITY = 'superfast'  

DIR_INPUT = "input_anime"
DIR_DONE = "completed"
DIR_OUTPUT = "READY_TO_UPLOAD"
DIR_SONGS = "songs"

VIRAL_TITLES = [
    " : This scene is literally straight peak 🗣️🔥",
    " : Did we just witness the biggest plot\ntwist of the year? 💀🔥",
    " : They really went all out on this\nanimation 👑",
    " : The absolute disrespect in this\nscene 🥶",
    " : Pure goosebumps from start to\nfinish 💯"
]

# ==============================================================================
# ⚙️ SYSTEM ENGINE
# ==============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_ANIME = os.path.join(BASE_DIR, DIR_INPUT)
FOLDER_DONE = os.path.join(BASE_DIR, DIR_DONE)
FOLDER_OUTPUT = os.path.join(BASE_DIR, DIR_OUTPUT)
FOLDER_SONGS = os.path.join(BASE_DIR, DIR_SONGS)

def clean_filename(folder, filename):
    clean = re.sub(r'[^\w\.]', '_', filename)
    clean = clean.replace("___", "_").replace("__", "_")
    full_old_path = os.path.join(folder, filename)
    full_new_path = os.path.join(folder, clean)
    if filename != clean:
        os.rename(full_old_path, full_new_path)
        return clean
    return filename

def get_random_song():
    if not os.path.exists(FOLDER_SONGS): return None
    songs = [f for f in os.listdir(FOLDER_SONGS) if f.endswith('.mp3')]
    if songs: return os.path.join(FOLDER_SONGS, random.choice(songs))
    return None

def find_best_moment(clip):
    print("🧠 Veda System: Scanning for the absolute PEAK moment...")
    duration = clip.duration
    if duration < 120: return [0]
    
    window = 10 
    volume_scores = []
    try:
        for t in range(0, int(duration), window):
            sub = clip.audio.subclip(t, min(t+window, duration))
            chunk = sub.to_soundarray(fps=22000)
            volume = np.sqrt(np.mean(chunk**2))
            volume_scores.append((t, volume))
        
        volume_scores.sort(key=lambda x: x[1], reverse=True)
        best_time = volume_scores[0][0]
        return [best_time]
    except:
        return [random.uniform(0, duration-60)]

# --- MAIN EDITING LOGIC ---

def create_reel(clip, start_time, index, video_name):
    print(f"\n🔨 Processing Ultimate Cut (Applying Exact Match Style)...")
    try:
        real_start = max(0, start_time - 5)
        subclip = clip.subclip(real_start, min(real_start + 59, clip.duration))
        subclip = subclip.fx(speedx, 1.05)

        final_w, final_h = 1080, 1920
        background = ColorClip(size=(final_w, final_h), color=(255, 255, 255), duration=subclip.duration)
        
        new_h = int(subclip.h * (1080 / subclip.w))
        if new_h % 2 != 0: new_h -= 1 
        video_layer = subclip.resize(width=1080, height=new_h).set_position(("center", "center"))
        
        layers = [background, video_layer]
        hook = random.choice(VIRAL_TITLES)
        
        txt_clip = TextClip(hook, fontsize=45, color='#1A1A1A', font='DejaVu-Sans', align='West', method='caption', size=(920, None))
        txt_clip = txt_clip.set_position(("center", 520)).set_duration(subclip.duration)
        layers.append(txt_clip)

        song = get_random_song()
        if song:
            bg_music = AudioFileClip(song).subclip(0, subclip.duration).volumex(0.15)
            final_audio = CompositeAudioClip([subclip.audio.volumex(1.0), bg_music]) if subclip.audio else bg_music
        else:
            final_audio = subclip.audio

        final = CompositeVideoClip(layers).set_audio(final_audio)
        
        if not os.path.exists(FOLDER_OUTPUT): os.makedirs(FOLDER_OUTPUT)
        timestamp = datetime.now().strftime("%H%M%S")
        clean_name = video_name.split('.')[0]
        out_filename = f"{clean_name}_VIRAL_{timestamp}.mp4"
        out_path = os.path.join(FOLDER_OUTPUT, out_filename)
        
        print(f"⏳ Rendering Clean Video to: {out_path}")
        final.write_videofile(out_path, codec='libx264', audio_codec='aac', fps=24, preset=VIDEO_QUALITY, ffmpeg_params=['-pix_fmt', 'yuv420p'])
        print(f"✅ SAVED: {out_filename} - READY TO GO VIRAL!")

    except Exception as e:
        print(f"❌ Error during rendering: {e}")

def start_worker():
    for f in [FOLDER_ANIME, FOLDER_DONE, FOLDER_OUTPUT, FOLDER_SONGS]:
        if not os.path.exists(f): os.makedirs(f)

    # ✅ JADOO YAHAN HAI: Bot ko '.webm' dekhna sikha diya!
    anime_files = [f for f in os.listdir(FOLDER_ANIME) if f.endswith(('.mp4', '.mkv', '.webm'))]
    if not anime_files:
        print("zzz... Waiting for raw anime episodes...", end='\r')
        return

    raw_name = anime_files[0]
    safe_name = clean_filename(FOLDER_ANIME, raw_name)
    video_path = os.path.join(FOLDER_ANIME, safe_name)
    
    print(f"\n🎬 STARTING BATCH: {safe_name}")
    
    try:
        clip = VideoFileClip(video_path)
        moments = find_best_moment(clip) 
        
        for i, t in enumerate(moments):
            create_reel(clip, t, i+1, safe_name)
            
        clip.close()
        shutil.move(video_path, os.path.join(FOLDER_DONE, safe_name))
        print("\n🎉 EPISODE PROCESSED! Peak moment extracted.\n")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        try:
            shutil.move(video_path, os.path.join(FOLDER_DONE, safe_name))
        except: pass

if __name__ == "__main__":
    print("🔥 VEDA LOGIC: VIRAL MEME BOT ACTIVATED 🔥")
    while True:
        start_worker()
        time.sleep(5)
