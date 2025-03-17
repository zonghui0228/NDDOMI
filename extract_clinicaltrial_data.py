# *_* coding: utf-8 *_*
# @author: zong hui
# @object: extract registration information from downloaded files of ClinicalTrials.gov


import os
import json
import codecs
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup
from utils import logger_config


class ClinicalTrialsXmlParser:
    """
    parse the downloaded xml file from ClinicalTrials.gov
    Args:
        NCTfile (:obj: 'string'):
            A NCT file of clinical trials.
    """
    def __init__(self, infile):
        self.infile = infile
        self.soup = BeautifulSoup(codecs.open(self.infile, encoding="UTF-8"), 'xml')

        self.data = {
            "nct_id": self.get_string_info("nct_id"),
            "brief_title": self.get_string_info("brief_title"),
            "official_title": self.get_string_info("official_title"),
            "overall_status": self.get_string_info("overall_status"),

            "start_date": self.get_string_info("start_date"),
            "completion_date": self.get_string_info("completion_date"),
            "study_first_posted": self.get_string_info("study_first_posted"),
            "study_first_submitted": self.get_string_info("study_first_submitted"),
            "last_update_submitted": self.get_string_info("last_update_submitted"),
            "verification_date": self.get_string_info("verification_date"),

            "phase": self.get_string_info("phase"),
            "study_type": self.get_string_info("study_type"),
            "primary_purpose": self.get_string_info("primary_purpose"),
            "condition": self.get_string_info("condition"),
            "enrollment": self.get_string_info("enrollment"),
            "gender": self.get_string_info("gender"),
            "minimum_age": self.get_string_info("minimum_age"),
            "maximum_age": self.get_string_info("maximum_age"),

            "PMID": self.get_PMID(),

            # "brief_summary": self._get_textblock_info("brief_summary"),
            # "detailed_description": self._get_textblock_info("detailed_description"),
            # "criteria": self._get_textblock_info("criteria"),
            "primary_outcome": self.get_outcome_measure("primary_outcome"),
            "secondary_outcome": self.get_outcome_measure("secondary_outcome"),
            "other_outcome": self.get_outcome_measure("other_outcome"),
            "url": self.get_string_info("url"),
        }

    def get_string_info(self, term):
        """extract information in string"""
        try:
            terms = [i.string for i in self.soup.find_all(term)]
            if len(terms) == 1:
                return terms[0]
            else:
                return terms
        except AttributeError:
            return ""

    def get_textblock_info(self, term):
        """extract information in textblock """
        try:
            terms = [i.textblock.string for i in self.soup.find_all(term)]
            if len(terms) == 1:
                return terms[0]
            else:
                return terms
        except AttributeError:
            return ""

    def get_PMID(self):
        """extract PMID"""
        try:
            terms = [i.pmid.string for i in list(self.soup.find_all("reference"))]
            return terms
        except AttributeError:
            return []

    def get_outcome_measure(self, term):
        """extract information of outcome measure"""
        measures = []
        try:
            # measure = {"measure":'', "time_frame":'', "description":''}
            for i in self.soup.find_all(term):
                measure = {"measure":'', "time_frame":'', "description":''}
                if i.measure:
                    measure["measure"] = i.measure.text
                if i.time_frame:
                    measure["time_frame"] = i.time_frame.text
                if i.description:
                    measure["description"] = i.description.text
                measures.append(measure)
            return measures
        except AttributeError:
            return measures

    def pretty_print(self):
        """print data"""
        print(json.dumps(self.data, sort_keys=False, indent=4, ensure_ascii=False))

    def save_info(self, outfile):
        """save data with json format"""
        with open(outfile, "w") as f:
            json.dump(self.data, f, indent=4)


if __name__ == "__main__":
    # =========================================================================================
    # process single file
    # test_data = "./data/D000544/all/NCT05153941.xml"
    # ctgxp = ClinicalTrialsXmlParser(test_data)
    # ctgxp.pretty_print()

    # =========================================================================================
    # batch process files
    # load params
    parser = argparse.ArgumentParser(description='download clinical trial registration information')
    parser.add_argument('-mesh', help='MeSH information', type=str, default='D010300')
    parser.add_argument('-save_dir', help='folder for downloaded files', type=str, default='data/')
    opt = parser.parse_args()

    # extract data
    logger = logger_config(log_path=os.path.join(opt.save_dir, opt.mesh, 'log.txt'))
    logger.info("start extraction ...")
    xmlfiles_dir = os.path.join(opt.save_dir, opt.mesh, 'xml')
    xmlfiles = [f for f in os.listdir(xmlfiles_dir) if f.endswith(".xml")]
    xmlfiles = sorted(xmlfiles)
    data = []
    for xmlfile in tqdm(xmlfiles, ncols=100):
        ctp = ClinicalTrialsXmlParser(os.path.join(xmlfiles_dir, xmlfile))
        data.append(ctp.data)

    # save data
    save_path = os.path.join(opt.save_dir, opt.mesh, opt.mesh+'.json')
    with open(save_path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.info("[mesh]: {}, [save path]: {}".format(opt.mesh, save_path))
