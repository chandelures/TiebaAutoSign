#!/bin/bash
cd `dirname $0`
dir=`pwd`
python="${dir}/venv/bin/python"
start_file_path="${dir}/start.py"
cookies_file_path="${dir}/cookies.txt"
cmd="${python} ${start_file_path} -c ${cookies_file_path}"


is_file_exist(){
    local file_path="$1"
    if [ -f "$file_path" ]; then
        return 1
    else
        error "文件${file_path}不存在"
    fi
}

is_dir_exist(){
    local dir_path="$1"
    if [ -d "$dir_path" ]; then
        return 1
    else
        error "目录${dir_path}不存在"
    fi
}

error(){
    echo "[ERROR]${1}"
}

main(){
    [ "is_dir_exist ${dir}" ] && [ "is_file_exist ${python}" ] && [ "is_file_exist ${start_file_path}" ] && [ "is_file_exist ${cookies_file_path}" ]
    eval ${cmd}
}

main
