# Wagon Survival Game

Petualangan bertahan hidup di padang gurun bersama kru unikmu!  
Game ini dibuat dengan Python dan Pygame.

---

## Fitur Utama

- **Manajemen Kru:** Pilih dan kelola kru dengan profesi unik (Chef, Hunter, Doctor, dsb).
- **Event Random:** Hadapi berbagai event musuh, cuaca, dan quest yang muncul secara acak.
- **Battle Animasi:** Battle dengan animasi jalan untuk kru dan musuh.
- **Sistem Hari & Malam:** Bertahan hidup selama 3 hari untuk menang.
- **Inventaris:** Kelola makanan, minuman, dan item kru.
- **Game Over & Finish:** Tampilan khusus dengan gambar `game_over.png` dan `finished.png`.

---

## Cara Main

1. **Jalankan game:**
    ```bash
    python main.py
    ```
2. **Ikuti instruksi di layar:**
    - Pilih kru, beri nama, dan kelola perjalanan.
    - Tekan angka 1/2/3 untuk memilih aksi di menu utama.
    - Hadapi event, battle, dan kelola inventaris.
    - Bertahan hidup hingga hari ke-3 untuk menang!

---

## Kontrol

- **[1]** Mulai perjalanan
- **[2]** Cek status kru
- **[3]** Lihat inventaris
- **[SPACE]** Lanjut cerita/event
- **[ESC]** Keluar saat game over/finish

---

## Struktur Folder

```
tes/
├── battle.py
├── crew.py
├── crew_inherit.py
├── event.py
├── game.py
├── interface.py
├── input_box.py
├── main.py
├── wagon.py
├── assets/
│   ├── *.png (semua gambar, termasuk game_over.png, finished.png, avatar, dsb)
│   ├── *.ttf (font)
│   └── *.mp3 (musik)
```

---

## Kebutuhan

- Python 3.x
- Pygame (`pip install pygame`)

---
## Pembagian Tugas Anggota

| No. | Nama                        | Pembagian Tugas                                                      |
|-----|-----------------------------|-----------------------------------------------------------------------|
| 1.  | Anisah Octa Rohila         | GameDev, Programmer, Lead Narrative Designer, Slides Maker           |
| 2.  | Ardiansyah Fernando        | GameDev, Lead Programmer, OOP Implementation                         |
| 3.  | Abel Fortino               | GameDev, Programmer, Main Assets Designer                            |
| 4.  | Ibrahim Budi Satria        | GameDev, Programmer, Assets Designer, UML                            |
| 5.  | Audy Olivya Br Gurusinga  | GameDev, Programmer                                                   |

**Selamat bermain dan bertahan hidup!**
