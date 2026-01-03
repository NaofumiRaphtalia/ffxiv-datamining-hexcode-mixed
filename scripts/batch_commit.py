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
    print(f"  -> 提交 {path}: {message}")
    run_git(['add', path])
    run_git(['commit', '-m', message])

def main():
    print("=== Git 批量分目录提交工具 ===")
    
    # 1. 处理通用语言组 (Global langs)
    active_global_langs = [l for l in LANG_GROUPS if has_changes(l)]
    
    global_msg = ""
    if active_global_langs:
        print(f"\n检测到以下全球版本目录有变动: {', '.join(active_global_langs)}")
        prompt = "输入通用版本号 (例如 7.4, 直接回车默认为 7.4): "
        global_msg = input(prompt).strip() or "7.4"
        
        for lang in active_global_langs:
            commit_dir(lang, global_msg)
    else:
        print("\n[chs, de, en, fr, ja] 目录无变动。")

    # 2. 处理独立语言组 (KO, TC)
    for item in OTHER_LANGS:
        lang = item['name']
        if has_changes(lang):
            print(f"\n检测到 {lang} 目录有变动:")
            default = item['default']
            prompt = f"输入 {lang} 的提交信息 (直接回车默认为 '{default}'): "
            msg = input(prompt).strip() or default
            commit_dir(lang, msg)
        else:
            print(f"\n[{lang}] 目录无变动。")

    print("\n任务完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n操作已取消。")
