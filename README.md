# NSFC_conclusion_downloader

帮助你从 [科学基金共享服务网（科技成果信息系统）](http://output.nsfc.gov.cn/) 下载 国自然结题报告，并生成PDF文件的工具。

## 核心思路

1. 通过 `http://output.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/{ratifyNo}` 接口确定该项目是否存在。
2. 通过 `while循环` 遍历 `http://output.nsfc.gov.cn/report/{ratifyNo[:2]}/{ratifyNo}_{i}.png` 下载该项目所有PNG，直到请求代码为404（即文件不存在）。
3. 使用 `img2pdf` 库生成对应PDF文件。

## 使用说明

1. 安装 Python3 以及 pip
2. 下载项目，并安装 Python依赖

    ```shell script
    git clone https://github.com/Rhilip/NSFC_conclusion_downloader.git
    cd NSFC_conclusion_downloader
    pip install -r requirements.txt
    ```

3. 运行项目，其中 `{ratifyNo}` 替换成你所需要的项目 **批准号**

    ```shell script
    python3 nsfc_downloader.py --ratify '31270544'
    ```
    
    你也可以在其他项目中使用如下示例代码进行批量下载
    
    ```python
    from nsfc_downloader import NsfcDownloader
    
    downloader = NsfcDownloader(tmp_path, out_path)
    
    for ratify in ['23456','2345','U12345','2345678']:
        downloader.download(ratify)
    ```
    
4. 你会在当前目录的 `output`目录中 获得类似 `31270544 生物炭强化石油烃污染土壤生态修复及机理研究.pdf` 的PDF文件

## 命令行使用

```shell script
(venv) .\NSFC_conclusion_downloader>python3 nsfc_downloader.py
usage: nsfc_downloader.py [-h] --ratify RATIFY [--tmp_path TMP_PATH]
                          [--out_path OUT_PATH]
```

## 其他

 - 本项目会在 `./tmp` 目录下留下对应项目的原始信息，例如 `./tmp/31270544.json`，你可以使用其他代码进行组合完成整理任务。
 - 下载的临时PNG图片会在PDF文件合成后被移除，如需保存，请自己修改代码。