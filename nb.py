#!/usr/bin/env python
# coding: utf-8

# In[ ]:


Model = "https://huggingface.co/Epiculous/Violet_Twilight-v0.2-GGUF/resolve/main/Violet_Twilight-v0.2.Q8_0.gguf" #@param[https://huggingface.co/mradermacher/L3-8B-Lunar-Stheno-GGUF/resolve/main/L3-8B-Lunar-Stheno.Q8_0.gguf]{allow-input: true}
Layers = "99" #@param [99]{allow-input: true}
ContextSize = "8192" # @param ["8192","4096", "16384"] {"allow-input":true}
# SillyTavern extras
#@markdown Allows to run SillyTavern Extras on CPU (use if you're out of daily GPU allowance)
use_cpu = False #@param {type:"boolean"}
#@markdown Allows to run Stable Diffusion pipeline on CPU (slow!)
use_sd_cpu = False #@param {type:"boolean"}
#@markdown Stable Diffusion Pipeline Settings(Tweaks)
use_sd_xl = True #@param {type:"boolean"}
lowvram = False #@param {type:"boolean"}
#@markdown ***
#@markdown Enables SD picture generation
extras_enable_sd = True #@param {type:"boolean"}
sd_model = "Darkknight535/KiraDepth-v1-Vpred-Diffusers" # @param ["Meina/MeinaMix_V11", "Meina/MeinaHentai_V5", "John6666/blue-pencil-xl-v7-sdxl-spo", "ckpt/anything-v4.5-vae-swapped", "Darkknight535/IMAGE-MODEL-Diffusers"]
sd_vae = "None" # @param ["madebyollin/sdxl-vae-fp16-fix"]




#ST-EXTRAS
import subprocess
import secrets
extras_url = '(disabled)'
params = []
if lowvram:
    params.append('--lowvram')
if use_cpu:
    params.append('--cpu')
if use_sd_cpu:
    params.append('--sd-cpu')
params.append('--port 2221')
params.append('--listen')
params.append('--cuda-device cuda:0')
modules = []

if extras_enable_sd:
  modules.append('sd')
params.append(f'--sd-model={sd_model}')
if sd_vae!= "None":
    params.append(f'--sd-vae={sd_vae}')
params.append(f'--enable-modules={",".join(modules)}')

get_ipython().run_line_magic('cd', '/kaggle/')
get_ipython().system('git clone https://github.com/Abdulhanan535/SillyTavern-ExtrasFix > /dev/null 2>&1')
get_ipython().run_line_magic('cd', '/kaggle/SillyTavern-ExtrasFix')
get_ipython().run_line_magic('pip', 'install -r requirements.txt > /dev/null 2>&1')
get_ipython().system('curl -O https://install.tunnelmole.com/xD345/install && sudo bash install')
get_ipython().run_line_magic('pip', 'install colorama > /dev/null 2>&1')
cmd = f"python /kaggle/SillyTavern-ExtrasFix/SDXL-vpred.py {' '.join(params)}"

#Ngrok 
get_ipython().system('pip3 install pyngrok > /dev/null 2>&1')
from pyngrok import ngrok
get_ipython().system('ngrok authtoken 2XekRXjuUStFiaZWvpTIBorUEDH_7H4KvF9BGjDM1e6Y1D8Qp > /dev/null 2>&1')

#KoboldCPP
get_ipython().run_line_magic('cd', '/kaggle')
get_ipython().system('wget -O dlfile.tmp https://kcpplinux.concedo.workers.dev > /dev/null 2>&1 && mv dlfile.tmp koboldcpp_linux > /dev/null 2>&1')
get_ipython().system('test -f koboldcpp_linux')
get_ipython().system('chmod +x ./koboldcpp_linux')
get_ipython().system('apt update > /dev/null 2>&1')
get_ipython().system('apt install aria2 -y > /dev/null 2>&1')
# simple fix for a common URL mistake
if "https://huggingface.co/" in Model and "/blob/main/" in Model:
    Model = Model.replace("/blob/main/", "/resolve/main/")
get_ipython().system('aria2c -x 10 -o model.gguf --summary-interval=5 --download-result=default --allow-overwrite=false --file-allocation=none $Model > /dev/null 2>&1')

get_ipython().run_line_magic('cd', '/kaggle/')
get_ipython().system('tmole 2221 & $cmd & ./koboldcpp_linux model.gguf --usecublas 1 mmq --gpulayers $Layers --contextsize $ContextSize --port 2222 --quiet --flashattention > /dev/null 2>&1 & ngrok http --url=grub-sacred-sailfish.ngrok-free.app 2222 > /dev/null 2>&1')
