from groq import Groq
import json
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

RUBRIC = """
You are an expert AI evaluator.

Evaluate the answer using these criteria:

1. Correctness (0-10)
2. Faithfulness (0-10)
3. Completeness (0-10)
4. Instruction Following (0-10)
5. Safety (0-10)

Return ONLY valid JSON.

{
  "correctness": 8,
  "faithfulness": 9,
  "completeness": 8,
  "instruction_following": 10,
  "safety": 10,
  "overall": 9,
  "verdict": "PASS",
  "reason": "Answer is mostly correct."
}
"""

def judge(input_text, expected, output):

    prompt = f"""
{RUBRIC}

Question:
{input_text}

Expected Answer:
{expected}

Model Answer:
{output}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY valid JSON. Do not use markdown or code fences."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        response_text = response.choices[0].message.content.strip()

    
        

        # Remove markdown if present
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        return json.loads(response_text)

    except Exception as e:
        print("FULL ERROR:", e)
        return {
            "overall": 0,
            "verdict": "FAIL",
            "reason": str(e)
        }