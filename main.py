import base64
import random
import requests
import string
import time

from requests import Session


def generate_random_letters(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def get_gitee_file_sha(url):
    """
    https://gitee.com/api/v5/repos/{owner}/{repo}/contents(/{path})
    :param url:
    :return:
    """
    url = url
    headers = {
        "accept": "application/json",
        "charset": "UTF-8",
    }
    response = requests.get(url, headers=headers, timeout=20).json()
    if response.get("sha"):
        return response["sha"]


def update_gitee_file(token, url, string):
    url = url
    headers = {
        "accept": "application/json",
        "charset": "UTF-8",
    }
    data = {
        "access_token": token,
        "content": base64.b64encode(string.encode("utf-8")).decode("utf-8"),
        "message": time.asctime(),
        "sha": get_gitee_file_sha(url)
    }
    resp = requests.put(url=url, headers=headers, json=data, timeout=20)
    if resp.status_code == 200:
        print(f"{ url } updated.")
    else:
        print(f"update { url }  failed! code: { resp.status_code }. text: { resp.text }")


def get_subscribe_content(fny_url):
    session = Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                    "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    # 先获取cookie
    session.get(fny_url)
    username = generate_random_letters(8)
    data = {
        "email": f"{username}@gmail.com",
        "password": f"{username}",
        "invite_code": "",
        "email_code": "",
    }
    # 注册
    resp = session.post(f"{fny_url}/api/v1/passport/auth/register", data=data, timeout=20)
    print(resp.text)
    # 获取订阅链接
    # resp = session.get(f"{fny_url}api/v1/user/getSubscribe", timeout=20)
    # print(resp.json())
    # subscribe_url = resp.json()["data"]["subscribe_url"]
    subscribe_url = fny_url + "/api/v1/client/subscribe?token=" + resp.json()["data"]["token"]
    # print("sub url:", subscribe_url)
    resp = session.get(subscribe_url, timeout=20)
    # resp = requests.get(subscribe_url, headers={"User-Agent": "Clash"})
    return resp.text


def main():
    _token = input()
    _fny_url = input()
    _clash_url1 = input()

    content1 = get_subscribe_content(_fny_url)
    update_gitee_file(_token, _clash_url1, content1)

    print("End", time.asctime())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
