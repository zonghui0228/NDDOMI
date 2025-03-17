# *_* coding: utf-8 *_*
# @author: zong hui
# @object: download registration files from ClinicalTrials.gov with a list of given condition terms


import os
import yaml
import zipfile
import requests
import argparse
from yaml.loader import SafeLoader
from utils import logger_config


class ClinicalTrialsXmlDownloader:
    """Given a list of terms, download registration file from ClinicalTrials.gov, 
    then unzip and remove the duplicate files.
    Args:
        terms (:obj: 'list'):
            A list contains the search terms or keywords.
        save_path (:obj: 'str'):
            the path to save downloaded files.
    """

    def __init__(self, terms, save_path):
        self.terms = terms
        self.zip_path = os.path.join(save_path, 'zip') # path to saved downloaded zip files.
        self.xml_path = os.path.join(save_path, 'xml') # path to saved extracted xml files.
        os.makedirs(self.zip_path, exist_ok=True)
        os.makedirs(self.xml_path, exist_ok=True)

        self.base_url = "https://clinicaltrials.gov/ct2/download_studies?cond="
        self.logger = logger_config(log_path=os.path.join(save_path, 'log.txt'))

    def download(self):
        # for each term, downloaed the clinical trials zip files.
        self.logger.info("start download ...")
        for term in self.terms:
            url = self.base_url + term.replace(' ', '+')
            zipfilename = os.path.join(self.zip_path, term+".zip")
            if os.path.exists(zipfilename):
                self.logger.info("[term]: {}, [save path]: {}".format(term, zipfilename))
                continue
            try:
                r = requests.get(url)
                with open(zipfilename, "wb") as f:
                    f.write(r.content)
                self.logger.info("[term]: {}, [save path]: {}".format(term, zipfilename))
            except Exception as e:
                self.logger.debug("Error occurred when downloading file, error message: "+e)

    def deduplication(self):
        # delete duplicate files
        self.logger.info("start deduplication ...")
        term2files = {}

        # begin to extract files.
        xml_files = list()
        for term in self.terms:
            zip_file_name = os.path.join(self.zip_path, term+".zip")
            # skip the empty zip file.
            if os.path.getsize(zip_file_name) == 0:
                term2files[term] = []
                continue
            # extract the xml from unempty zip file
            zFile = zipfile.ZipFile(zip_file_name, "r")
            term2files[term] = zFile.namelist()
            for xlm_file in zFile.namelist():
                zFile.extract(xlm_file, self.xml_path)
                if xlm_file not in xml_files:
                    xml_files.append(xlm_file)

        for term, files in term2files.items():
            self.logger.info("[term]: {}, [files]: {}".format(term, len(files)))
        self.logger.info("{} unique files save to folder {}.".format(len(xml_files), self.xml_path))


if __name__ == "__main__":
    # load params
    parser = argparse.ArgumentParser(description='download clinical trial registration information')
    parser.add_argument('-mesh', help='MeSH information', type=str, default='D010300')
    parser.add_argument('-save_dir', help='folder for downloaded files', type=str, default='data/')
    opt = parser.parse_args()

    # load config
    with open(f'./conf/{opt.mesh}.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

    # call functions
    terms = [data['name']] + data['entry_terms']
    save_path = opt.save_dir + opt.mesh
    ctd = ClinicalTrialsXmlDownloader(terms, save_path)
    ctd.download()
    ctd.deduplication()
