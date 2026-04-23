#!/bin/bash
# file-practice.sh: 用命令自动创建一个目录结构

echo "开始创建 practice-demo 目录结构..."

#创建目录
mkdir -p practice-demo/docs
mkdir -p practice-demo/scripts
mkdir -p practice-demo/data

#创建文件并写入内容
echo "# 项目说明" > practice-demo/docs/readme.txt
echo "这是一个练习项目" >> practice-demo/docs/readme.txt

echo "#!/bin/bash" > practice-demo/scripts/hello.sh
echo 'echo "Hello from practice-demo!"' >> practice-demo/scripts/hello.sh

echo "name,age,city" > practice-demo/data/sample.csv
echo "Alice,20,shanghai" >> practice-demo/data/sample.csv
echo "Bob,22,Beijing" >> practice-demo/data/sample.csv

echo ""
echo "目录创建完成！"
echo "--- tree ---"
find practice-demo -type f | sort
