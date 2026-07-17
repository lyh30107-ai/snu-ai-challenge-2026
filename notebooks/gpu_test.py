import sys
import torch

print("Python 위치:", sys.executable)
print("Python 버전:", sys.version)
print("PyTorch 버전:", torch.__version__)
print("CUDA 사용 가능:", torch.cuda.is_available())

if torch.cuda.is_available():
    device = torch.device("cuda")

    print("GPU 이름:", torch.cuda.get_device_name(0))

    x = torch.randn(3000, 3000, device=device)
    result = x @ x

    print("계산 장치:", result.device)
    print("GPU 테스트 성공")
else:
    print("GPU를 사용할 수 없습니다.")