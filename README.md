# Eulytix Assignment

## Setup (using pip):

### 1.: Create Python venv

```bash
python -m venv .venv  # or python3 -m venv venv
```

### 2.: Activate the venv

#### Windows
```bash
.venv\Scripts\activate
```
#### Linux & Unix

```bash
source .venv/bin/activate
```

### 3.: Install required packages with pip (Selenium, Sci-kit Learn)
```bash
pip install -r requirements.txt
```

### Improvement Ideas:
1. [TPOT](https://epistasislab.github.io/tpot/) AutoML
2. [Polars](https://pola.rs/) If we need to handle larger datasets
3. [RAPIDS CuDF and CuML](https://rapids.ai/ecosystem/#software) To Handle Data Processing and Machine Learning on the (NVIDIA) GPU using CUDA
