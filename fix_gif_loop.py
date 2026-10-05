#!/usr/bin/env python3
"""
fix_gif_loop.py
Memproses ulang GIF dalam direktori target, memaksa loop count menjadi 0 (tak terbatas).
Mengatasi masalah di mana GIF di README GitHub berhenti setelah diputar sekali.
"""

import sys
from pathlib import Path
from PIL import Image, ImageSequence

def force_infinite_loop(gif_path: Path, output_path: Path = None):
    """
    Baca GIF, tulis ulang semua frame, tetapkan loop=0.
    loop=0 berarti tak terbatas.
    """
    if output_path is None:
        output_path = gif_path
    
    try:
        with Image.open(gif_path) as im:
            frames = []
            durations = []
            
            for frame in ImageSequence.Iterator(im):
                # Konversi ke RGBA untuk menghindari masalah palet
                frame_rgba = frame.convert("RGBA")
                frames.append(frame_rgba)
                durations.append(frame.info.get("duration", 100))
            
            if not frames:
                print(f"⚠️  {gif_path.name}: Tidak ada frame yang dapat dibaca, dilewati")
                return False
            
            # Simpan ulang, kunci loop=0 (tak terbatas)
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,              # 0 = loop tak terbatas
                disposal=2,          # Bersihkan frame sebelumnya, hindari ghosting
                optimize=False,      # Jangan optimasi, pastikan blok loop ditulis dengan benar
            )
            
            print(f"✅ {gif_path.name}: Sudah diperbaiki menjadi loop tak terbatas")
            return True
            
    except Exception as e:
        print(f"❌ {gif_path.name}: Pemrosesan gagal — {e}")
        return False

def main():
    # Default memproses direktori assets/gifs di bawah direktori skrip
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./assets/gifs")
    
    if not target_dir.exists():
        print(f"❌ Direktori tidak ada: {target_dir}")
        sys.exit(1)
    
    gif_files = list(target_dir.glob("*.gif"))
    
    if not gif_files:
        print(f"⚠️  Tidak ditemukan file GIF di {target_dir}")
        sys.exit(0)
    
    print(f"📁 Menemukan {len(gif_files)} file GIF, mulai diproses...\n")
    
    success = 0
    for gif_path in gif_files:
        # Buat file sementara, hindari menimpa file asli secara langsung
        tmp_path = gif_path.with_suffix(".tmp.gif")
        if force_infinite_loop(gif_path, tmp_path):
            tmp_path.replace(gif_path)  # Timpa file asli
            success += 1
        else:
            if tmp_path.exists():
                tmp_path.unlink()
    
    print(f"\n🎉 Selesai: {success}/{len(gif_files)} file GIF diperbaiki menjadi loop tak terbatas")

if __name__ == "__main__":
    main()
