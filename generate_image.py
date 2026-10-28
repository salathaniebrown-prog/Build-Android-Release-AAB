import os
import sys
import io
from google import genai
from google.genai import types
from PIL import Image

def generate_astra_art(prompt: str, output_filename: str = "station_render.png"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    print(f"🎨 [AI STUDIO IMAGEN]: Generating image for prompt: '{prompt}'...")

    # Standard Google AI Studio API key initialization (vertexai disabled)
    client = genai.Client(api_key=api_key)

    try:
        # Direct Imagen 3 call on Google AI Studio
        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png"
            )
        )

        if response.generated_images:
            image_bytes = response.generated_images[0].image.image_bytes
            image = Image.open(io.BytesIO(image_bytes))
            output_path = os.path.join(os.getcwd(), output_filename)
            image.save(output_path)
            print(f"✅ [SUCCESS]: Image saved to -> {output_path}")
            return output_path
        else:
            print("❌ No images returned.")
            return None

    except Exception as e:
        print(f"⚠️ Imagen Direct call failed ({e}), attempting Gemini 2.0 Flash image generation...")
        try:
            # Fallback for API keys with multimodal response enabled
            resp = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"Generate an image of: {prompt}",
            )
            for part in resp.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image = Image.open(io.BytesIO(part.inline_data.data))
                    output_path = os.path.join(os.getcwd(), output_filename)
                    image.save(output_path)
                    print(f"✅ [SUCCESS]: Image saved via Gemini Flash to -> {output_path}")
                    return output_path
            print(f"❌ [ERROR]: {resp.text}")
            return None
        except Exception as err2:
            print(f"❌ [IMAGE GEN FAILED]: {err2}")
            return None

if __name__ == "__main__":
    prompt_input = sys.argv[1] if len(sys.argv) > 1 else "Futuristic 3D cybernetic space station with cyan holographic telemetry panels"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "station_render.png"
    generate_astra_art(prompt_input, out_file)
