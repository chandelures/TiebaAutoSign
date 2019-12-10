#!/bin/bash
cd `dirname $0`
dir=`pwd`
python="${dir}/venv/bin/python"
start_file_path="${dir}/start.py"
cookies_file_path="${dir}/cookies.txt"
log_path="/var/log/tieba.log"
cmd="${python} ${start_file_path} -c ${cookies_file_path} >> ${log_path} 2>&1"

is_file_exist(){
    file_path="$1"
    if [ -f "$file_path" ]; then
            return 1
    else
            error "文件${file_path}不存在"
    fi
}

is_dir_exist(){
    dir_path="$1"
    if [ -d "$dir_path" ]; then
        return 1
    else
        error "目录${dir_path}不存在"
    fi
}

error(){
    msg "[ERROR]${1}"
}

msg() {
    printf '%b\n' "$1" >&2
}

main(){
    is_dir_exist "${dir}"
    for file_path in "${python}" "${start_file_path}" "${cookies_file_path}"
    do
        is_file_exist ${file_path}
    done
    if [ $? -eq 0 ]; then
        msg "开始进行一键签到......"
        eval ${cmd}
    else
        error "一键签到失败。"
    fi
}

main
