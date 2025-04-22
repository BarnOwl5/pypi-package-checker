import os
import json
import requests
import re

# 파일 중복 방지
def get_unique_filename(base_path, base_name):
    filename = f"{base_path}/{base_name}.json"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_path}/{base_name}({counter}).json"
        counter += 1
    return filename

# 패키지 이름 유효성 검사
def is_valid_package_name(name):
    return re.fullmatch(r"[a-zA-Z0-9_\-]+", name) is not None

# 패키지 이름 입력값 길이 제한
def is_valid_length(name) :
    return len(name) <= 50

def check_package_info(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code != 200:
        result = {
            "name": package_name,
            "exists": False,
            "last_update": None,
            "github_url": None
        }
    else:
        data = response.json()
        version = data["info"]["version"]

        # 마지막 업로드 시점
        try:
            last_update = data["releases"][version][-1]["upload_time"]
        except (KeyError, IndexError):
            last_update = "정보 없음"

        # GitHub 주소 추출
        github_url = None
        project_urls = data.get("info", {}).get("project_urls", {})
        for key, value in project_urls.items():
            if value and "github.com" in value.lower():
                github_url = value
                break

        result = {
            "name": package_name,
            "exists": True,
            "last_update": last_update,
            "github_url": github_url
        }

    # 📁 결과 저장
    os.makedirs("D:/results", exist_ok=True)
    filename = get_unique_filename("D:/results", package_name)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"[✔] '{os.path.basename(filename)}' saved successfully!\n")

# 테스트 실행
if __name__ == "__main__" :
    package_name = input("input package name : ")

    if is_valid_package_name(package_name) and is_valid_length(package_name):
        check_package_info(package_name)

    else:
        print("invalid package name. Try again :(")
