import torch
from PIL import Image

from niceml.deployment.fastapicreateapp import create_fastapi_app
from niceml.utilities.encoding import base64_to_bytesio
from transformers import AutoImageProcessor, TableTransformerForObjectDetection


assets = {}

asset_loaders = {
    "image_processor": lambda: AutoImageProcessor.from_pretrained(
        "microsoft/table-transformer-detection"
    ),
    "model": lambda: TableTransformerForObjectDetection.from_pretrained(
        "microsoft/table-transformer-detection"
    ),
}


app = create_fastapi_app(assets, asset_loaders)


@app.post("/detect_structure")
async def detect_structure(input_data: dict) -> dict:
    input_image = Image.open(base64_to_bytesio(input_data["image"])).convert("RGB")
    image_processor = assets["image_processor"]
    inputs = image_processor(images=input_image, return_tensors="pt")
    outputs = assets["model"](**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    target_sizes = torch.tensor([input_image.size[::-1]])
    results = image_processor.post_process_object_detection(
        outputs, threshold=0.9, target_sizes=target_sizes
    )[0]

    output_dict = {}
    for score, box in zip(results["scores"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        confidence = round(float(score), 2)

        output_dict = {
            "bbox": box,
            "score": confidence,
        }
    print("=========================================")
    print(output_dict)
    print("=========================================")

    return output_dict
