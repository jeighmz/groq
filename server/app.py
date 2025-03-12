from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import groq
from mem0 import MemoryClient
from youtube_transcript_api import YouTubeTranscriptApi
import re  # For YouTube link detection

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)

# Retrieve API keys
api_key = os.getenv('GROQ_API_KEY')
api_key_mem = os.getenv('MEM0_API_KEY')

if not api_key:
    raise ValueError("Groq API key not found in environment variables!")
if not api_key_mem:
    raise ValueError("Mem0 API key not found in environment variables!")

# Initialize clients
groq_client = groq.Client(api_key=api_key)
memory_client = MemoryClient(api_key=api_key_mem)

# Regex for detecting YouTube links
youtube_regex = re.compile(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        selected_models = data.get('models', [])
        user_id = data.get('user_id', 'default_user')

        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        if not selected_models:
            return jsonify({"error": "No models selected"}), 400

        # Check if the message contains a YouTube link
        youtube_match = youtube_regex.search(user_message)
        if youtube_match:
            video_id = youtube_match.group(1)
            transcript = fetch_youtube_transcript(video_id)

            if transcript:
                summarization_prompt = f"Summarize the key points of this YouTube video transcript:\n\n{transcript}"

                responses = []
                for model in selected_models:
                    chat_completion = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": summarization_prompt}],
                        model=model,
                    )
                    response_text = chat_completion.choices[0].message.content

                    responses.append({
                        "model": model,
                        "response": response_text,
                        "retrieved_memory": []  # 🛑 Ensure NO MEMORY IS RETURNED
                    })

                return jsonify(responses), 200

            else:
                return jsonify({"error": "Failed to retrieve transcript"}), 500

        # Normal chat processing (WITH MEMORY RETRIEVAL)
        past_memories = memory_client.search(user_message, user_id=user_id)
        history = []
        retrieved_memory = []

        if past_memories:
            for mem_obj in past_memories:
                if mem_obj.get("score", 0) > 0.25:
                    memory_text = mem_obj["memory"]
                    history.append({"role": "system", "content": f"(Memory) {memory_text}"})
                    retrieved_memory.append(memory_text)

        history.append({"role": "user", "content": user_message})

        responses = []
        for model in selected_models:
            chat_completion = groq_client.chat.completions.create(
                messages=history,
                model=model,
            )
            response_text = chat_completion.choices[0].message.content

            responses.append({
                "model": model,
                "response": response_text,
                "retrieved_memory": retrieved_memory
            })

            memory_client.add([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": response_text}
            ], user_id=user_id)

        return jsonify(responses), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


def fetch_youtube_transcript(video_id):
    """Fetch transcript for a given YouTube video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript])
    except Exception as e:
        print("Error fetching YouTube transcript:", e)
        return None


@app.route('/api/youtube-transcript', methods=['POST'])
def get_youtube_transcript():
    """API route to fetch YouTube transcripts."""
    try:
        data = request.json
        video_id = data.get('videoId')

        if not video_id:
            return jsonify({"error": "Invalid YouTube video ID"}), 400

        transcript_text = fetch_youtube_transcript(video_id)
        if transcript_text:
            return jsonify({"transcript": transcript_text}), 200
        else:
            return jsonify({"error": "Failed to retrieve transcript"}), 500

    except Exception as e:
        print("Error fetching YouTube transcript:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)