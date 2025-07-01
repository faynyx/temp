import vertexai
from vertexai.vision_models import ImageGenerationModel

def generate_image(prompt: str):
    
    vertexai.init(project="project_name", location="us-central1")
    generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-06-06")
    images = generation_model.generate_images(
        prompt=prompt,
        number_of_images=1,  
        aspect_ratio="1:1",
        add_watermark=True,
    )
    return images

def generate_image_not_watermarking(prompt: str):
    
    vertexai.init(project="project_name", location="us-central1")
    generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-06-06")
    images = generation_model.generate_images(
        prompt=prompt,
        number_of_images=1,  
        aspect_ratio="1:1",
        add_watermark=False,
    )
    return images

if __name__ == "__main__":
    prompt = "A majestic golden retriever sitting on a mountain peak with clouds below, epic adventure style"
    try:
        images = generate_image(prompt)
        not_watermarking_image = generate_image_not_watermarking(prompt)

        images[0].save("watermark_image.png")
        not_watermarking_image[0].save("not_watermarking_image.png")

    except Exception as e:
        print ("Exception : ", e)
