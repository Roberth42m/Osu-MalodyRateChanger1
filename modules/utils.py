import os
import zipfile


def extract_osz(osz_path, extract_dir):

    with zipfile.ZipFile(osz_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


def find_osu_files(directory):

    osu_files = []

    for file in os.listdir(directory):

        if file.lower().endswith(".osu"):

            osu_files.append(
                os.path.join(directory, file)
            )

    return osu_files


def find_audio_file(directory):

    audio_extensions = [
        ".mp3",
        ".ogg",
        ".wav",
        ".flac",
        ".m4a",
    ]

    for file in os.listdir(directory):

        if any(
            file.lower().endswith(ext)
            for ext in audio_extensions
        ):

            return os.path.join(directory, file)

    return None