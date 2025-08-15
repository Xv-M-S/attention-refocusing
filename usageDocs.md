# env

``` bash
conda create --name ldm_layout python==3.8.0
conda activate ldm_layout
# conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# 此处将CPython 换成了_graalpy_python
# conda install python==3.8.5
# pip3 install --upgrade pip setuptools
# pip3 install pycocotool==2.0.7
pip3 install -r requirements.txt
pip3 install git+https://github.com/CompVis/taming-transformers.git
pip3 install git+https://github.com/openai/CLIP.git
```

# download model

```bash
mkdir gligen_checkpoints
cd gligen_checkpoints
wget https://hf-mirror.com/gligen/gligen-generation-text-box/resolve/main/diffusion_pytorch_model.bin
```

# run

```bash
unset PYTORCH_CUDA_ALLOC_CONF
python guide_gligen.py --ckpt gligen_checkpoints/diffusion_pytorch_model.bin --file_save counting_500  --type counting --box_pickle ./data_evaluate_LLM/gpt_generated_box/counting.p
```