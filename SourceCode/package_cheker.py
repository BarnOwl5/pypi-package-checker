import os, sys
import json
import requests
import re

sys.path.append(os.path.dirname(__file__))
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
    global result
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
def run_check_flow(package_name) :
    if is_valid_package_name(package_name) and is_valid_length :
        check_package_info(package_name)
        filename = save_result(result["name"], result) 
        return filename
    else :
        print("invalid package name. Try again :(")
    
def save_result(package_name,result) :
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 .py 파일 위치
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    filename = get_unique_filename(results_dir, package_name)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"[✔] '{os.path.basename(filename)}' saved successfully!\n")

    return filename