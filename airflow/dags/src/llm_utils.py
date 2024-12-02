import logging
import os
from typing import Any, Dict
from .config import load_config

config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "info_extraction_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


def extract_information_from_text(
    text: str, extraction_fields: list[str], client, model_name
) -> Dict[str, Any]:
    """
    Extract specified information from a text file using OpenAI's language model.

    Returns:
    - dict: A dictionary with the extracted information.
    """
    prompt = _generate_prompt(extraction_fields=extraction_fields, text=text)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        completion_text = response.choices[0].message.content.strip()
        logging.debug(f"Completion text: {completion_text}")
        results = _parse_completion_to_dict(completion_text, extraction_fields)
        logging.info("Information extracted successfully.")
        return results
    except Exception as e:
        logging.error(f"Failed to extract information: {e}")
        raise


def _generate_prompt(extraction_fields: list[str], text: str) -> str:
    """
    Create a dynamic prompt based on the extraction_fields
    """
    info_list_str = "\n".join([f"- {info}" for info in extraction_fields])
    output_format = ", ".join(
        [f"{info}: <{info.replace(' ', '_').lower()}>" for info in extraction_fields]
    )

    prompt = f"""
    Extract the following information:
    {info_list_str}

    Be as concise as possible and the output format should be:
    {output_format}

    from the text:
    {text}

    """
    logging.debug(f"Generated prompt: {prompt}")
    return prompt


def _parse_completion_to_dict(completion_text, extraction_fields):
    logging.info("Parsing completion text into a dictionary...")
    result = {}
    for field in extraction_fields:
        key = field.lower().replace(" ", "_")
        # Look for the field in the completion text
        start = completion_text.find(f"{field}:")
        if start != -1:
            start += len(f"{field}:")
            end = completion_text.find(",", start)
            result[key] = completion_text[start:end].strip()
        else:
            result[key] = None
    logging.debug(f"Parsed result: {result}")
    return result
