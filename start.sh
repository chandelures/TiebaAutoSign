#!/bin/bash
cd `dirname $0`
dir=`pwd`
python="${dir}/venv/bin/python"
start_file_path="${dir}/start.py"
cookies_file_path="${dir}/cookies.txt"
cmd="${python} ${start_file_path} -c ${cookies_file_path}"


is_file_exist(){
    if [[ -f $1 ]];then
    return 1
    else
    error "文件$1不存在"
    fi
}

is_dir_exist(){
    if [[ -d $1 ]];then
    return 1
    else
    error "目录$1不存在"
    fi
}

error(){
    echo "[ERROR]$1"
}

main(){
    if [[ is_dir_exist ${dir} ]] && [[ is_file_exist ${python} ]] && [[ is_file_exist ${start_file_path} ]] && [[ is_file_exist ${cookies_file_path} ]];
    then
    eval ${cmd}
    else
    error "签到失败"
    fi
}

main