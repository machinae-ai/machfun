import json

def merge_json(json1_str, json2_str):
    # Convert JSON strings to dictionaries
    json1 = json.loads(json1_str)
    json2 = json.loads(json2_str)

    # Merge dictionaries using update() method
    merged = json1.copy()
    merged.update(json2)

    # Convert merged dictionary to JSON string
    merged_str = json.dumps(merged)

    # Return merged JSON string
    return merged_str
