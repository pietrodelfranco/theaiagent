from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv
from moviepy.editor import TextClip, concatenate_videoclips

# Carica le variabili d'ambiente dal file .env
load_dotenv()
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    """Pagina principale per inserire il comando dell'utente."""
    return render_template("index.html")

@app.route("/generate_video", methods=["POST"])
def generate_video():
    """Genera un video basato sul comando dell'utente."""
    user_command = request.form.get("command")

    if not user_command or user_command.strip() == "":
        return "Errore: il comando è vuoto.", 400

    try:
        # Step 1: Usa OpenAI per generare una sceneggiatura
        script_response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "Sei un assistente che crea sceneggiature per video."},
                    {"role": "user", "content": user_command}
                ]
            }
        )
        script_response.raise_for_status()
        script = script_response.json()["choices"][0]["message"]["content"]

        # Step 2: Genera un video con MoviePy
        video = TextClip(script, fontsize=70, color='white', size=(1280, 720))
        video = video.set_duration(10)  # Durata di 10 secondi
        video_path = "static/generated_video.mp4"
        video.write_videofile(video_path, fps=24)

        return jsonify({"message": "Video generato con successo!", "video_url": video_path})
    except requests.exceptions.RequestException as e:
        return f"Errore durante la chiamata a OpenAI: {str(e)}", 500
    except Exception as e:
        return f"Errore durante la generazione del video: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


