"""
French TTS - Generate speech from French text with multiple voices.

REQUIREMENTS (run once):
    pip install TTS

USAGE:
    python generate_french_speech.py

HOW VOICES WORK WITH XTTS v2:
  - XTTS v2 uses "voice cloning" - you give it a short audio sample (WAV, 6-30 sec)
    and it clones that exact voice to read your French text.
  - So for male/female voices you just need a male and a female audio WAV sample.
  - We include 3 demo modes below depending on what you have available.
"""

import os
from TTS.api import TTS

# =============================================================================
# CONFIGURATION — Edit this section to match your needs
# =============================================================================


#   [0] Claribel Dervla
#   [1] Daisy Studious
#   [2] Gracie Wise
#   [3] Tammie Ema
#   [4] Alison Dietlinde
#   [5] Ana Florence
#   [6] Annmarie Nele
#   [7] Asya Anara
#   [8] Brenda Stern
#   [9] Gitta Nikolina
#   [10] Henriette Usha
#   [11] Sofia Hellen
#   [12] Tammy Grit
#   [13] Tanja Adelina
#   [14] Vjollca Johnnie
#   [15] Andrew Chipper
#   [16] Badr Odhiambo
#   [17] Dionisio Schuyler
#   [18] Royston Min
#   [19] Viktor Eka
#   [20] Abrahan Mack
#   [21] Adde Michal
#   [22] Baldur Sanjin
#   [23] Craig Gutsy
#   [24] Damien Black
#   [25] Gilberto Mathias
#   [26] Ilkin Urbano
#   [27] Kazuhiko Atallah
#   [28] Ludvig Milivoj
#   [29] Suad Qasim
#   [30] Torcull Diarmuid
#   [31] Viktor Menelaos
#   [32] Zacharie Aimilios
#   [33] Nova Hogarth
#   [34] Maja Ruoho
#   [35] Uta Obando
#   [36] Lidiya Szekeres
#   [37] Chandra MacFarland
#   [38] Szofi Granger
#   [39] Camilla Holmström
#   [40] Lilya Stainthorpe
#   [41] Zofija Kendrick
#   [42] Narelle Moon
#   [43] Barbora MacLean
#   [44] Alexandra Hisakawa
#   [45] Alma María
#   [46] Rosemary Okafor
#   [47] Ige Behringer
#   [48] Filip Traverse
#   [49] Damjan Chapman
#   [50] Wulf Carlevaro
#   [51] Aaron Dreschner
#   [52] Kumar Dahl
#   [53] Eugenio Mataracı
#   [54] Ferran Simen
#   [55] Xavier Hayasaka
#   [56] Luis Moray

# Your French text to generate
TEXTES_FRANCAIS = [
"Exactement : services d'enseignement. Et avec plus de 500 salariés… Mais pour Recycl'Tout, regardez bien les seuils de chiffre d'affaires au Maroc…"
]# Speaker index from the list above (0-57). Change this number to switch voice.
SPEAKER_INDEX = 22  # [46] Rosemary Okafor

# Output folder where .wav files will be saved
OUTPUT_DIR = "french_audio_output"

# =============================================================================
# MODE 1 — EASIEST: Use a built-in French model (single voice, no GPU needed)
# =============================================================================
def mode_1_simple_french():
    """
    Uses the dedicated French VITS model.
    - Single voice (female)
    - No voice samples needed
    - Fast, works on CPU
    - Model: tts_models/fr/css10/vits
    """
    print("\n" + "="*60)
    print("MODE 1: Simple French Model (single voice)")
    print("="*60)

    tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=True, gpu=False)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, texte in enumerate(TEXTES_FRANCAIS):
        output_file = os.path.join(OUTPUT_DIR, f"mode1_phrase_{i+1}.wav")
        print(f"\n[{i+1}] Génération: {texte[:60]}...")
        tts.tts_to_file(text=texte, file_path=output_file)
        print(f"  → Sauvegardé : {output_file}")

    print(f"\nDone! Files saved in '{OUTPUT_DIR}/'")


# =============================================================================
# MODE 2 — BEST QUALITY: XTTS v2 with your own voice samples (voice cloning)
# =============================================================================
def mode_2_voice_cloning(male_voice_wav: str, female_voice_wav: str):
    """
    Uses XTTS v2 — the best model. You provide a short WAV audio sample
    (6 to 30 seconds works best) for each voice you want to clone.

    Args:
        male_voice_wav:   Path to a WAV file with a male voice sample
        female_voice_wav: Path to a WAV file with a female voice sample

    To get voice samples:
      - Record yourself or someone else for ~10 seconds (WAV or MP3 converted to WAV)
      - Or download free voice samples from:
          https://www.openslr.org/94/  (multilingual, includes French)
          https://www.voicemod.net/
    """
    print("\n" + "="*60)
    print("MODE 2: XTTS v2 — Voice Cloning (male + female)")
    print("="*60)

    # XTTS requires accepting terms of service — set env var to auto-accept
    os.environ["COQUI_TOS_AGREED"] = "1"

    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2",
              progress_bar=True, gpu=False)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    voices = {
        "homme": male_voice_wav,
        "femme": female_voice_wav,
    }

    for voix_nom, voix_wav in voices.items():
        if not os.path.exists(voix_wav):
            print(f"  ⚠  Fichier introuvable: {voix_wav} — ignoré.")
            continue

        for i, texte in enumerate(TEXTES_FRANCAIS):
            output_file = os.path.join(OUTPUT_DIR, f"mode2_{voix_nom}_phrase_{i+1}.wav")
            print(f"\n[Voix {voix_nom}] Phrase {i+1}: {texte[:50]}...")
            tts.tts_to_file(
                text=texte,
                speaker_wav=voix_wav,
                language="fr",
                file_path=output_file,
            )
            print(f"  → Sauvegardé : {output_file}")

    print(f"\nDone! Files saved in '{OUTPUT_DIR}/'")


# =============================================================================
# MODE 3 — XTTS v2 with built-in speakers (no audio samples needed)
# =============================================================================
def mode_3_builtin_speakers():
    """
    XTTS v2 comes with pre-built speaker profiles (included in the model download).
    This lists all available speaker names and generates speech with a few of them.
    No voice samples required.
    """
    print("\n" + "="*60)
    print("MODE 3: XTTS v2 — Built-in Speakers")
    print("="*60)

    os.environ["COQUI_TOS_AGREED"] = "1"

    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2",
              progress_bar=True, gpu=False)

    # List all available built-in speaker names
    if not tts.speakers:
        print("No built-in speakers found (model may need the speakers_xtts.pth file).")
        return

    print(f"\nAvailable built-in speakers ({len(tts.speakers)} total):")
    for i, s in enumerate(tts.speakers):
        print(f"  [{i}] {s}")

    idx = SPEAKER_INDEX
    if idx < len(tts.speakers):
        selected_speakers = [tts.speakers[idx]]
        print(f"\nUsing speaker [{idx}]: {tts.speakers[idx]}")
    else:
        print(f"SPEAKER_INDEX {idx} out of range, falling back to speaker 0.")
        selected_speakers = [tts.speakers[0]]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    texte_demo = TEXTES_FRANCAIS[0]

    for speaker in selected_speakers:
        output_file = os.path.join(OUTPUT_DIR, f"mode3_{speaker.replace(' ', '_')}.wav")
        print(f"\n[Speaker: {speaker}]: {texte_demo[:50]}...")
        tts.tts_to_file(
            text=texte_demo,
            speaker=speaker,
            language="fr",
            file_path=output_file,
        )
        print(f"  → Sauvegardé : {output_file}")

    print(f"\nDone! Files saved in '{OUTPUT_DIR}/'")

# =============================================================================
# MAIN — Choose which mode to run
# =============================================================================
if __name__ == "__main__":
    mode_3_builtin_speakers()
