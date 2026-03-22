import json
import Parser
import Schemas
from getpass import getpass
from dataclasses import asdict
from pathlib import Path
from Parser import extract_text_from_pdf


if __name__ == "__main__":
    # API key is needed for ai or scanned pdf reading.
    api_key = getpass("Enter your API key: ").strip()
    ai_model = "gemini-2.5-flash"

    # ---- Usage ----
    pdf_file = "PO/Purchase_order__01_PR121676_2026-01-16_16-39-36_.PDF"
    # pdf_file = 'PO/Purchase Order 30046173.pdf'
    # pdf_file = 'PO/SPurchasing26011614040.pdf'
    AI_Test = False
    Outputs_test = False
    debug = False

    if AI_Test:
        import google.genai as genai
        client = genai.Client(api_key=api_key)

        data = Parser.extract_po_info('', Schemas.PO_SCHEMA, client, ai_model)
        po = Parser.build_structures(data)

        if debug:
            print(data)
            print("\n=== Purchase Order ===")
            print(json.dumps(asdict(po), indent=2))

        filename = Path(pdf_file).stem
        output_file = Path(f"Outputs/{filename}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(asdict(po), f, indent=2, ensure_ascii=False)
        print(f"Parsed file {pdf_file}, and saved to {output_file}")

    elif Outputs_test:
        filename = Path(pdf_file).stem
        input_file = Path(f"Outputs/{filename}.json")
        json_data = input_file.read_text(encoding="utf-8")

        # convert to dataclass
        po = Parser.build_structures(json_data)

        # convert to dataframe
        df = Parser.po_to_dataframe(po)

        # output csv
        output_file = input_file.with_suffix(".csv")
        df.to_csv(output_file, index=False)

        print(f"Saved CSV to {output_file}")

    else:   # Print prompt so to have free test
        text = extract_text_from_pdf(pdf_file, ai_model, api_key)
        print(text)
