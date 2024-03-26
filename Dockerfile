
# docker build -t k8shelper .
# docker run -p 8050:8050 -v ~/.kube:/root/.kube k8shelper:v1.0.0

# Python 베이스 이미지 사용
FROM python:3.9-slim


# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 의존성 파일 복사
COPY requirements.txt .

# 필요한 Python 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app

# Install necessary packages including curl and git
RUN apt-get update && apt-get install -y \
    curl \
    git

# Install kubectl by downloading the binary
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# 컨테이너 외부로 노출할 포트 지정
EXPOSE 8050

# 컨테이너가 시작될 때 애플리케이션 실행
CMD ["python", "k8shelper.py", "--server.port=8050"]
