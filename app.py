import os
import tempfile
import shutil

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from reamber.osu.OsuMap import OsuMap

from modules.utils import (
    extract_osz,
    find_osu_files,
    find_audio_file,
)

from modules.audio import rate_audio
from modules.map import rate_maps
from modules.packer import create_osz

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():

    uploaded_map = request.files.get("map_file")
    uploaded_audio = request.files.get("audio_file")

    if not uploaded_map or not uploaded_audio:

        return "Missing files", 400

    # NUEVO
    mode = request.form.get("mode", "rate")

    keep_pitch = (
        request.form.get("keep_pitch") == "on"
    )

    work_dir = tempfile.mkdtemp()

    try:

        map_filename = secure_filename(
            uploaded_map.filename
        )

        audio_filename = secure_filename(
            uploaded_audio.filename
        )

        map_path = os.path.join(
            work_dir,
            map_filename
        )

        audio_path = os.path.join(
            work_dir,
            audio_filename
        )

        uploaded_map.save(map_path)
        uploaded_audio.save(audio_path)

        # Detectar .osz o .osu

        if map_filename.lower().endswith(".osz"):

            extract_dir = os.path.join(
                work_dir,
                "map"
            )

            extract_osz(
                map_path,
                extract_dir
            )

        else:

            extract_dir = os.path.join(
                work_dir,
                "map"
            )

            os.makedirs(
                extract_dir,
                exist_ok=True
            )

            shutil.copy(
                map_path,
                extract_dir
            )

        osu_files = find_osu_files(extract_dir)

        if not osu_files:

            return "No .osu files found", 400

        # NUEVO: calcular rate usando BPM

        if mode == "bpm":

            first_map = OsuMap.read_file(
                osu_files[0]
            )

            original_bpm = (
                first_map.bpms[0].bpm
            )

            target_bpm = float(
                request.form.get("bpm")
            )

            rate = target_bpm / original_bpm

        else:

            rate = float(
                request.form.get("rate", 1.0)
            )

        # Buscar audio original

        original_audio = find_audio_file(
            extract_dir
        )

        if (
            original_audio
            and os.path.exists(original_audio)
        ):

            os.remove(original_audio)

        audio_extension = os.path.splitext(
            audio_filename
        )[1]

        new_audio_name = (
            f"audio_{rate:.2f}x"
            f"{audio_extension}"
        )

        converted_audio_path = os.path.join(
            extract_dir,
            new_audio_name
        )

        # Convertir audio

        rate_audio(
            input_audio=audio_path,
            output_audio=converted_audio_path,
            rate=rate,
            keep_pitch=keep_pitch,
        )

        # Ratear mapas

        rate_maps(
            osu_files=osu_files,
            rate=rate,
            new_audio_filename=new_audio_name,
        )

        # Crear .osz final

        output_name = (
            f"Rate_{rate:.2f}x.osz"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            output_name
        )

        create_osz(
            extract_dir,
            output_path
        )

        return send_file(
            output_path,
            as_attachment=True
        )

    finally:

        shutil.rmtree(
            work_dir,
            ignore_errors=True
        )


if __name__ == "__main__":

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)