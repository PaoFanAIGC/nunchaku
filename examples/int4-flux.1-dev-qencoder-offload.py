import torch
from diffusers import FluxPipeline

from nunchaku import NunchakuFluxTransformer2dModel, NunchakuT5EncoderModel

transformer = NunchakuFluxTransformer2dModel.from_pretrained(
    "mit-han-lab/svdq-int4-flux.1-dev", offload=True
)  # set offload to False if you want to disable offloading
text_encoder_2 = NunchakuT5EncoderModel.from_pretrained("mit-han-lab/svdq-flux.1-t5")
pipeline = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev", text_encoder_2=text_encoder_2, transformer=transformer, torch_dtype=torch.bfloat16
).to("cuda")
pipeline.enable_sequential_cpu_offload()  # remove this line if you want to disable the CPU offloading
image = pipeline("A cat holding a sign that says hello world", num_inference_steps=50, guidance_scale=3.5).images[0]
image.save("flux.1-dev.png")
