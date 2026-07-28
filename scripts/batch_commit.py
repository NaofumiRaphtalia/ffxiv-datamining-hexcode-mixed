import subprocess
import os

# 配置
REPO_DIR = os.getcwd()
LANG_GROUPS = ["chs", "de", "en", "fr", "ja"]
OTHER_LANGS = [
    {"name": "ko", "default": "7.35"},
    {"name": "tc", "default": "7.2"}
]

def run_git(args):
    """执行 git 命令"""
    result = subprocess.run(['git'] + args, capture_output=True, text=True, encoding='utf-8', cwd=REPO_DIR)
    return result

def has_changes(path):
    """检查路径是否有改动"""
    result = run_git(['status', '--porcelain', path])
    return len(result.stdout.strip()) > 0

def commit_dir(path, message):
    """添加并提交目录"""
    full_message = f"{message} {path.upper()}"
    print(f"  -> 提交 {path}: {full_message}")
    run_git(['add', path])
    run_git(['commit', '-m', full_message])

def main():
    print("=== Git 批量分目录提交工具 ===")
    
    # 1. 处理通用语言组 (Global langs)
    active_global_langs = [l for l in LANG_GROUPS if has_changes(l)]
    
    global_msg = ""
    if active_global_langs:
        print(f"\n检测到以下全球版本目录有变动: {', '.join(active_global_langs)}")
        while True:
            global_msg = input("输入通用版本号 (例如 7.4): ").strip()
            if global_msg:
                break
            print("错误：提交信息不能为空，请输入版本号。")
        
        for lang in active_global_langs:
            commit_dir(lang, global_msg)
    else:
        print("\n[chs, de, en, fr, ja] 目录无变动。")

    # 2. 处理独立语言组 (KO, TC)
    for item in OTHER_LANGS:
        lang = item['name']
        if has_changes(lang):
            print(f"\n检测到 {lang} 目录有变动:")
            while True:
                msg = input(f"输入 {lang} 的提交信息: ").strip()
                if msg:
                    break
                print(f"错误：{lang} 的提交信息不能为空。")
            commit_dir(lang, msg)
        else:
            print(f"\n[{lang}] 目录无变动。")

    print("\n任务完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n操作已取消。")
