
# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
if ! command -v conda >/dev/null 2>&1; then
    MINICONDA_DIR="$HOME/miniconda3"
    INSTALLER="$HOME/miniconda.sh"
    wget -q -O "$INSTALLER" "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    bash "$INSTALLER" -b -p "$MINICONDA_DIR"
    rm -f "$INSTALLER"
    source "$MINICONDA_DIR/etc/profile.d/conda.sh"
else
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/anaconda3/etc/profile.d/conda.sh"
    fi
fi


# Conda 환셩 생성 및 활성화
## TODO
if ! conda env list | grep -q "^myenv"; then
    conda create -y -n myenv python=3.11
fi
conda activate "myenv"


## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
## TODO
python -m pip install -q mypy


# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    ## TODO
    num="${file##*_}"
    num="${num%.py}"

    input_file="../input/${num}_input"
    output_file="../output/${num}_output"

    python "$file" < "$input_file" > "$output_file" || exit 1
done

# mypy 테스트 실행 및 mypy_log.txt 저장
## TODO
mypy . > mypy_log.txt 2>&1


# conda.yml 파일 생성
## TODO
conda env export > conda.yml


# 가상환경 비활성화
## TODO
conda deactivate
