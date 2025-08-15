#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量安装 requirements.txt 中的依赖包（使用 pip._internal，非 subprocess）
逐个安装，出错时跳过并继续下一个
"""

import sys
import os
import time
import logging

# 配置日志，让 pip 输出更清晰
logging.basicConfig(level=logging.INFO)

# 尝试导入 pip 内部模块
try:
    import pip._internal as pip_internal
except ImportError:
    try:
        import pip as pip_internal
    except ImportError:
        print("❌ 错误：无法导入 pip 模块，请确保 pip 已安装。")
        sys.exit(1)

def install_from_requirements(file_path='requirements.txt', index_url=None):
    """
    从 requirements.txt 文件逐个安装包（使用 pip._internal）
    """
    if not os.path.exists(file_path):
        print(f"❌ 错误：文件 {file_path} 不存在！")
        return

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        packages = f.readlines()

    # 过滤有效行
    valid_packages = []
    for line in packages:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('-r'):
            package = stripped.split('==')[0].split('>=')[0].split('~=')[0]
            valid_packages.append((package, stripped))

    print(f"✅ 共找到 {len(valid_packages)} 个需要安装的包。\n")

    success_count = 0
    failed_packages = []

    for package_name, full_spec in valid_packages:
        print(f"📦 正在安装: {full_spec} ...")

        # 构造 pip install 参数
        cmd = ['install', full_spec]
        if index_url:
            cmd.extend(['-i', index_url])
        # 可选：添加超时、信任源等
        # cmd.extend(['--timeout', '300'])

        try:
            # 调用 pip 内部 main 函数
            # 返回值为 0 表示成功，非 0 表示失败
            exit_code = pip_internal.main(cmd)
            if exit_code == 0:
                print(f"✅ 成功安装: {package_name}\n")
                success_count += 1
            else:
                print(f"❌ 安装失败: {package_name} (退出码: {exit_code})\n")
                failed_packages.append(full_spec)
        except Exception as e:
            print(f"🚨 未知错误: {package_name} - {str(e)}\n")
            failed_packages.append(full_spec)

        time.sleep(1)  # 可选：避免过快

    # 最终统计
    print("="*60)
    print(f"🎉 安装完成！成功: {success_count}, 失败: {len(failed_packages)}")
    if failed_packages:
        print("❌ 以下包安装失败：")
        for pkg in failed_packages:
            print(f"    {pkg}")

if __name__ == '__main__':
    # ================================
    # 🔧 配置区
    # ================================
    REQUIREMENTS_FILE = 'requirements.txt'
    INDEX_URL = 'https://mirrors.aliyun.com/pypi/simple/'  # 阿里源，推荐

    # ================================
    # 执行安装
    # ================================
    install_from_requirements(file_path=REQUIREMENTS_FILE, index_url=INDEX_URL)