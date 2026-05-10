# bushido (武士道)
Bushido is a discipline-driven personal logging and analytics app. It helps you capture structured data about training, recovery, and daily activities while keeping the system minimal, extensible, and under your control.

### Installation for usage
* download tarball 
* install pipx
```aiignore
pipx install bushido-major.minor.patch.tar.gz
```

### Installation for dev 

#### Prerequisites
* Python 3.14+
```
curl -Ls https://astral.sh/uv/install.sh | sh
git clone https://github.com/njavet/bushido.git
cd bushido
uv sync
uv run bushido
```