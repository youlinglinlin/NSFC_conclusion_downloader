import os
import json
import argparse
from glob import glob

import img2pdf
import requests

import utils


def arg_parser():
    parse = argparse.ArgumentParser(
        description='A tool to Download PDF format conclusion from http://output.nsfc.gov.cn/')
    parse.add_argument('--ratify', '-r', help='The ratify id of the project you want to download', required=True)
    parse.add_argument('--tmp_path', '-t', default='./tmp', help='The path you want to save tmp file')
    parse.add_argument('--out_path', '-o', default='./output', help='The path you want to save output PDF file')
    return parse.parse_args()


class NsfcDownloader:

    def __init__(self, tmp_path, out_path):
        self.tmp_path = tmp_path
        self.out_path = out_path

    def download(self, ratify):
        print('开始获取项目信息，项目编号： {}'.format(ratify))

        project_info_file = os.path.join(self.tmp_path, '{}.json'.format(ratify))
        if os.path.exists(project_info_file):
            rj = json.load(open(project_info_file, 'r', encoding='utf-8'))
        else:
            r = requests.get('http://output.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/{}'.format(ratify))
            r.raise_for_status()

            rj = r.json()  # project_info
            print('保存项目信息至 {}'.format(project_info_file))
            json.dump(rj, open(project_info_file, 'w', encoding='utf-8'), ensure_ascii=False, sort_keys=True)

        if rj.get('code') != 200:
            exit('项目可能不存在，请重新检查网页 http://output.nsfc.gov.cn/conclusionProject/{} 显示'.format(ratify))

        ratify_prefix = ratify[:2]
        project_name = rj['data'].get('projectName')
        out_pdf_file = os.path.join(self.out_path, utils.clean_filename('{} {}.pdf'.format(ratify, project_name)))

        if os.path.exists(out_pdf_file):
            print('PDF已存在 ，请打开 {}'.format(out_pdf_file))
        else:
            print('开始下载 {} {}'.format(ratify, project_name))

            img_bytes_list = []

            i = 1
            while True:
                tmp_file = os.path.join(self.tmp_path, '{}_{}.png'.format(ratify, i))
                if os.path.exists(tmp_file):
                    content = open(tmp_file, 'rb').read()
                else:
                    req_url = "http://output.nsfc.gov.cn/report/{}/{}_{}.png".format(ratify_prefix, ratify, i)
                    print('正在请求页面 {}'.format(req_url))
                    r = requests.get(req_url, timeout=10)
                    if r.status_code == 404:
                        break
                    content = r.content
                    with open(tmp_file, 'wb') as tmp_f:
                        tmp_f.write(r.content)

                img_bytes_list.append(content)
                i += 1

            print('下载完成 {} {}'.format(ratify, project_name))

            if len(img_bytes_list) > 0:
                print('正在组合PDF {}'.format(out_pdf_file))
                pdf = img2pdf.convert(img_bytes_list)
                with open(out_pdf_file, "wb") as file_:
                    file_.write(pdf)

                print('移除临时文件')
                for f in glob(os.path.join(self.tmp_path, '{}_*.png'.format(ratify))):
                    os.remove(f)


if __name__ == '__main__':
    args = arg_parser()
    downloader = NsfcDownloader(args.tmp_path, args.out_path)
    downloader.download(args.ratify)
