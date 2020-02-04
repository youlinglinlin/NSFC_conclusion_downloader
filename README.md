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
 - 原始信息中的 `root.data.projectType` 与展示 项目类别 的关系定义在 `http://output.nsfc.gov.cn/common/data/supportTypeClassOneData` 中，目前关系如下
    ```json
    {
    "630": "青年科学基金项目", 
    "631": "地区科学基金项目", 
    "218": "面上项目", 
    "632": "海外及港澳学者合作研究基金", 
    "220": "重点项目",
    "222": "重大项目", 
    "339": "重大研究计划", 
    "429": "国家杰出青年科学基金", 
    "432": "创新研究群体项目",
    "433": "国际(地区)合作与交流项目", 
    "649": "专项基金项目", 
    "579": "联合基金项目", 
    "70": "应急管理项目", 
    "7161": "科学中心项目", 
    "635": "国家基础科学人才培养基金", 
    "2699": "优秀青年科学基金项目", 
    "8531": "专项项目",
    "51": "国家重大科研仪器设备研制专项",
    "52": "国家重大科研仪器研制项目", 
    "2733": "海外或港、澳青年学者合作研究基金"
    }
    ```
 - 下载的临时PNG图片会在PDF文件合成后被移除，如需保存，请自己修改代码。
