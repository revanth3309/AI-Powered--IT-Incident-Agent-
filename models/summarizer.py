import google.generativeai as genai

# ✅ Step 1: Configure Gemini API Key
genai.configure(api_key="$$$$$$")  # Replace with your actual key

# ✅ Step 2: Load Gemini Pro model
model = genai.GenerativeModel('gemini-2.0-flash') 
def generate_summary(current_description, root_cause, similar_cases):
    root_cause = root_cause or "Not available"

    # Format the similar cases into readable text
    case_texts = []
    for case in similar_cases:
        desc = case['ticket'].get('Description', 'N/A')
        cause = case['ticket'].get('root_cause', 'N/A')
        full = desc + " - " + case['ticket'].get('Close notes', '')
        case_texts.append(f"→ Description: {desc}\n  Root Cause: {cause}\n  Full Description: {full}\n" + "="*80)

    input_text = f"🔍 Top {len(case_texts)} results for query: \"{current_description}\"\n\n" + "\n".join(case_texts)

    prompt = f"""INCIDENT SUMMARY REQUEST  *CURRENT INCIDENT:* Description: {current_description} Root Cause: {root_cause} *SIMILAR INCIDENTS FROM HISTORY:*

    {input_text}

    Based on the current incident and these similar cases, provide a summary with:

    ## SUMMARY
    What is happening and why it matters

    ## LIKELY ROOT CAUSE
    Most probable cause based on patterns

    ## IMMEDIATE ACTIONS
    Top 3 steps to take right now

    ## EXPECTED RESOLUTION TIME
    Based on similar incidents

    ## CONFIDENCE LEVEL
    How sure you are about this analysis (High/Medium/Low)
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini LLM Error: {str(e)}"
