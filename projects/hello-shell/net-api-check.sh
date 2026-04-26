 #!/bin/bash
  # 网络状态检查 - 第1周 Day 5

  echo "========== 网络状态检查 =========="
if ping -c 1 -w 1 8.8.8.8 &> /dev/null;then
	  echo "8.8.8.8通"
else
	  echo "8.8.8.8不通"
fi
if ping -c 1 -w 1 baidu.com &> /dev/null;then
	echo "baidu.com通"
else
	echo "baidu.com不通"
fi

echo "=============curl 调 API================"
weather=$(curl -s --connect-timeout 5 https://wttr.in/Shanghai?format=3) 
echo "$weather"

echo "=============wget 下载测试==============="
burl=/tmp/baidu_homepage.html
wget -q -O $burl https://www.baidu.com
if [ -f $burl ];then
	echo "下载成功"
else
	echo "下载失败"
fi
rm -f $burl

  echo "========== 检查完成 =========="
