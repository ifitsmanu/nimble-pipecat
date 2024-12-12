# NIM and Pipecat

# setting up notebook
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install jupyterlab
pip install ipykernel
python -m ipykernel install --user --name=venv --display-name "Python3.12"
```

# running the notebook with pipecat code
```bash
OPENAI_API_KEY=${OPENAI_API_KEY} \
DAILY_SAMPLE_ROOM_URL=${DAILY_SAMPLE_ROOM_URL} \
DAILY_API_KEY=${DAILY_API_KEY} \
NVIDIA_API_KEY=${NVIDIA_API_KEY} \
python -m jupyter notebook
```

# in notebook
```bash
!pip install "pipecat-ai==0.0.50"
!pip install nvidia-riva-client
!pip install nest_asyncio
!pip install loguru
!pip install onnxruntime
```

???
import os
os.environ["OPENAI_API_KEY"]="..."
