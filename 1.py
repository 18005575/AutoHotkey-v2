#!/usr/bin/env python3
# push_all.py
import os
import subprocess
import datetime
import webbrowser
import sys

REPO_URL = "https://github.com/18005575/AutoHotkey-v2.git"
BRANCH   = "main"

# 如果你愿意，直接在这里写死
GIT_USER  = "18005575"
GIT_EMAIL = "50049195+18005575@users.noreply.github.com"

def run(cmd):
    """运行 shell 命令并实时打印输出"""
    print(f"$ {cmd}")
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line, end="")
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"命令返回值非 0：{ret}")

def ensure_git_identity():
    """确保 Git 有用户名和邮箱"""
    try:
        subprocess.check_output("git config user.name", shell=True)
        subprocess.check_output("git config user.email", shell=True)
    except subprocess.CalledProcessError:
        print("检测到 Git 身份未配置，正在自动写入…")
        run(f'git config user.name "{GIT_USER}"')
        run(f'git config user.email "{GIT_EMAIL}"')

def main():
    if not os.path.exists(".git"):
        run("git init")

    ensure_git_identity()   # 关键：自动写身份

    run("git add .")
    msg = f"Initial commit / Auto sync {datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
    run(f'git commit -m "{msg}"')

    run(f"git remote add origin {REPO_URL} 2>nul || echo origin already exists")
    run(f"git branch -M {BRANCH}")
    run(f"git push -u origin {BRANCH} --force")

    webbrowser.open(REPO_URL)

if __name__ == "__main__":
    try:
        main()
        print("\n==== 推送完成 ====")
    except Exception as e:
        print("\n==== 发生错误 ====")
        print(e)
