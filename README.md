# python 小工具

## 新增python的虚拟环境

```shell
py -m venv [虚拟环境的名称]
```

## 切换到当前环境
```shell
.\venv\Scripts\activate
```

## 保存到requirements.txt
```shell
pip3 freeze > requirements.txt
```

## 工具

### pdf转换成图片

电子发票转换为图片格式
```shell
python pdf2imageApp.py
```

### 生成exe执行文件
```shell
# 安装pyinstaller
pip install pyinstaller
# -F参数指定打包成1个exe文件，--paths指定dependency的路径
pyinstaller -F --paths=<your_path>\Lib\site-packages  yourprogram.py
```