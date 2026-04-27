#!/bin/bash
target_dir=/mnt/c/Users/H1831/Desktop/lianjing-internship-prep/projects/hello-shell
cd $target_dir

successed=0
skipped=0

rename_one(){
	local old_name="$1"
	local new_name="backup_$old_name"

	if [ -e "$new_name" ];then
		echo "跳过：$old_name -> $new_name"
		return 1
	else
		mv "$old_name" "$new_name"
		echo "成功：$old_name -> $new_name"
		return 0
	fi

}
for file in *.csv *.log;do
	[ -f "$file" ] || continue

	if rename_one "$file";then
		((++successed))
	else
		((++skipped))
	fi
done
echo "成功重命名: $successed 个文件"
echo "跳过: $skipped 个文件"
