import json
import pandas as pd
from dataclasses import asdict
from Schemas import PO_SCHEMA, ClientInfo, GoodsItem, OrderInfo, PurchaseOrder
import pymupdf4llm



# -------------------------
# Step 1: Extract text (PDF or OCR)
# -------------------------
def extract_text_from_pdf(pdf_path, ai_model=None, api_key=None):
    """
    1. Try pymupdf4llm (best for structured text)
    2. Fallback to OCR if needed
    """

    text = ""

    # -------- Step 1: pymupdf4llm --------
    try:
        text = pymupdf4llm.to_markdown(pdf_path)
    except Exception as e:
        print(f"⚠️ pymupdf4llm failed: {e}")

    # -------- Step 2: OCR fallback --------
    if not text or not text.strip():
        #AI has better performance than OCR for example.
        text = parse_pdf_with_vision(pdf_path, ai_model=ai_model, api_key=api_key)

    return text

# -------------------------
# Step 2: AI-based extraction
# -------------------------
def build_prompt(text, schema):
    return f"""
You are an information extraction system.

Extract purchase order information from the text below.

Rules:
- Return JSON only
- Follow the schema exactly
- Missing fields must be null
- Do not invent data
- Numbers must be numbers

JSON schema:
{json.dumps(schema, indent=2)}

PURCHASE ORDER TEXT:
--------------------
{text}
"""

def extract_po_info(text, schema, AIClient=None, model=None):
    """
    Extract purchase order info using Google GenAI.

    Args:
        text (str): The PO text to parse.
        schema (dict): JSON schema (used only for building the prompt)
        model (str or None): Model name like 'models/gemini-2.5-flash'.
                             If None, prints the prompt for debugging.

    Returns:
        str: JSON string matching the schema.
    """
    prompt = build_prompt(text, schema)

    if AIClient is None or model is None:  # Debug mode
        print(prompt)
        return None
    else:
        # Send prompt directly; schema already included inside the prompt
        response = AIClient.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        return response.text

# ----------------------------------------
# Step 3: Convert to PurchaseOrder object
# ----------------------------------------
def build_structures(data):
    data_json = json.loads(data)
    client = ClientInfo(**data_json["client"])
    purchase_order = OrderInfo(**data_json["order_info"])
    items = [GoodsItem(**item) for item in data_json["items"]]

    po = PurchaseOrder(
        client=client,
        order_info=purchase_order,
        items=items
    )
    return po


# -------------------------
# Convert to DataFrame
# -------------------------
def po_to_dataframe(po: PurchaseOrder):
    po_dict = asdict(po)

    rows = []

    for item in po_dict["items"]:
        row = {
            **po_dict["client"],
            **po_dict["order_info"],
            **item
        }
        rows.append(row)

    return pd.DataFrame(rows)

def parse_pdf_to_json(pdf_path, ai_model, api_key):
    import google.genai as genai

    client = genai.Client(api_key=api_key)
    ai_model = ai_model
    text = extract_text_from_pdf(pdf_path, ai_model, api_key)
    return extract_po_info(text, PO_SCHEMA, client, ai_model)

def parse_pdf_with_vision(pdf_path, ai_model, api_key):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    # Read PDF bytes
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    prompt = """
    You are an information extraction system.

    Extract purchase order information from this document.

    Rules:
    - Return JSON only
    - Follow the schema exactly
    - Missing fields must be null
    - Numbers must be numbers
    """

    response = client.models.generate_content(
        model=ai_model,
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf"
            ),
            prompt
        ]
    )

    # Safely extract text
    return response.text if hasattr(response, "text") else str(response)
