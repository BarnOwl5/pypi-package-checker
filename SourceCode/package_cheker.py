import os, sys
import json
import requests
import re,time
from datetime import datetime

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


# PyPI API로 요청을 보낸 후 패키지 이름 실존 확인인
def get_pypi_data(package_name):
    global result
    
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code != 200:
        return None, False
    
    #패키지 정보 data
    data = response.json()
    return data, True

def check_core_metadata(data) :
    return "info" in data and "releases" in data

def check_release_validity(data) :
    version = data["info"].get("version")
    release_data = data["releases"].get(version,[])

    #버전이 존재하지 않거나 릴리즈 데이터가 없을 경우
    if not version or not release_data:
        return "N/A", None
    
    #마지막 업데이트 시점 판단
    try :
        last_update = release_data[-1]["upload_time"]
        year = int(last_update[:4])
        current_year = datetime.now().year
        susp_check = current_year - 4

        if year <= susp_check :
            return f"Package not updated recently (before {susp_check}", year
        
    except (KeyError, IndexError, ValueError):
        return "Missing upload time", False

# GitHub 주소 추출
def check_github_link(data) :
    project_urls = data.get("info", {}).get("project_urls", {})
    if not project_urls :
        return "No GitHub link", None
    for key, value in project_urls.items():
        if value and "github.com" in value.lower():
            return value
        else : return "No Github link", None

# summary lenth 추출
def check_summary(data) :
    summary = data.get("info", {}).get("summary", "")
    if not summary or len(summary) < 20 :
        return "Package description too short (<20 characters)", False
    return "summary exists", True

# author email 존재 여부
def check_author_email(data) :
    return bool(data.get("info",{}).get("author_email"))


# 결과 저장
def run_check_flow(package_name) :
    if is_valid_package_name(package_name) and is_valid_length :
        check_package_info(package_name)
        filename = save_result(result["name"], result) 
        return filename
    else :
        print("invalid package name. Try again :(")
    
# .json 형식
def package_result(name, exists, last_update, github_url, summary, has_email) :
    result = {
        "name" : name,
        "exists" : exists,
        "last update" : last_update,
        "github url" : github_url,
        "summary check" : summary,
        "has email" : has_email
    }
    return result

def check_package_info(package_name) :
    data, status = get_pypi_data(package_name)
    if not status or not data :
        return package_result(package_name, False, "N/A", None, ["Request failed or No data"],False)
    if not check_core_metadata : 
        return package_result(package_name, False, "N/A", None, ["Missing required metadata"],False)

    exists = True
    last_update = check_release_validity(data)
    github_url =  check_github_link(data)
    summary = check_summary(data)
    has_email = check_author_email(data)
    return package_result(package_name, exists, last_update, github_url[0], summary[0], has_email)

def run_check_flow(package_name) :
    if is_valid_package_name(package_name) and is_valid_length(package_name) :
        result = check_package_info(package_name)
        filename = save_result(result["name"],result)
        return filename
    else :
        print("invalid package name. Try Again :(")
        time.sleep(0.5)
        return None

def save_result(package_name,result) :
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 .py 파일 위치
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    filename = get_unique_filename(results_dir, package_name)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"[✔] '{os.path.basename(filename)}' saved successfully!\n")

    return filename

