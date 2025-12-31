from config.ai_config import GROQ_CLIENT

def ai_should_close_buffer(buffer_text: str, next_line_text: str) -> bool:
    """
    Returns True if AI detects a topic/context shift between buffer_text and next_line_text.
    """
    prompt = (
        "Decide if the next line is a continuation of the previous text or a new topic. "
        "Answer YES if it's a new topic, NO if it continues the same context.\n\n"
        f"Previous text:\n{buffer_text}\n\nNext line:\n{next_line_text}\n\n"
        "Answer YES or NO only."
    )

    try:
        
        response = GROQ_CLIENT.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        
        # answer = response["choices"][0]["message"]["content"].strip().upper()
        answer = response.choices[0].message.content.strip().upper()


        return answer == "YES"
    except Exception as e:
        print(f"[AI Error] {e}")
        # Fail-safe: continue buffer if AI fails
        return False
