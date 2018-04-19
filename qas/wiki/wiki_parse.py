from lxml import etree
from pprint import pprint
import logging
import sys
import re
import json

from qas.constants import OUTPUT_DIR, SAVE_OUTPUTS
from qas.esstore.es_operate import ElasticSearchOperate
from qas.esstore.es_config import __wiki_raw__

"""
Parsing with XPath 1.0 query
XPath Documentation : https://developer.mozilla.org/en-US/docs/Web/XPath

The '.' at the beginning means, that the current processing starts at the current node. 
Your xpath starts with a slash '/' and is therefore absolute.
The '*' selects all element nodes descending from this current node with the @id-attribute-value or @class value'.
The '//' identifies any descendant designation element of element 
"""

logger = logging.getLogger(__name__)


class XPathExtractor:

    regexpNS = "http://exslt.org/regular-expressions"
    nonBreakSpace = u'\xa0'
    newLine_nonBreak_regex = r'(\n+)|(\xa0)'

    toc_pattern = '''//*[@id="toc"]'''
    non_searchable_pattern = '''/html/body/div/div[starts-with(@class, "hatnote")]'''
    description_list_pattern = '''/html/body/div/dl'''
    references_pattern = '''/html/body/div/div[starts-with(@class, "refbegin")]'''
    references_list_pattern = '''/html/body/div/div[starts-with(@class, "reflist")]'''
    meta_data_box_pattern = '''/html/body/div/div[starts-with(@class, "metadata")]'''
    nav_boxes_pattern = '''/html/body/div/div[@class="navbox"]'''
    vertical_nav_boxes_pattern = '''/html/body/div/table[starts-with(@class, "vertical-navbox")]'''
    no_print_metadata_pattern = '''/html/body/div/div[starts-with(@class, "noprint")]'''
    subscript_pattern = '''//sup[@class="reference"]'''
    edit_pattern = '''//span[@class="mw-editsection"]'''
    meta_data_table = '''/html/body/div/table[contains(@class, "metadata")]'''

    see_also_pattern = '''//*[@id="See_also"]'''
    external_links_pattern = '''//*[@id="External_links"]'''

    img_pattern = '''/html/body/div//div[starts-with(@class, "thumb ")]'''
    img_href = '''./div//a/@href'''
    img_caption = '''.//div[@class="thumbcaption"]/text()'''

    info_box_pattern = '''/html/body/div/table[starts-with(@class, "infobox")]'''
    info_box_item = '''./tr'''
    info_key_pattern = '''./th//text()'''
    info_value_pattern = '''./td//text()'''

    table_pattern = '''/html/body/div/table[@class="wikitable"]'''
    table_row_pattern = '''./tr'''
    table_key_pattern = '''./th'''
    table_value_pattern = '''./td'''
    all_text_pattern = '''.//text()'''

    irrelevant_headlines = ['''//*[@id="See_also"]''', '''//*[@id="Notes_and_references"]''',
                            '''//*[@id="Explanatory_notes"]''', '''//*[@id="Citations"]''',
                            '''//*[@id="Further_reading"]''', '''//*[@id="External_links"]''',
                            '''//*[@id="References"]''']

    html_data = ''
    extracted_img = {}
    html_tree = None
    isFile = False
    pageid = None
    es_ops = None
    newLine_nonBreak_pattern = None

    def __init__(self, html_data, isFile):
        self.es_ops = ElasticSearchOperate()
        self.html_data = html_data
        self.newLine_nonBreak_pattern = re.compile(self.newLine_nonBreak_regex)
        # parser = etree.XMLParser(ns_clean=True, remove_comments=True)
        parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
        if isFile:
            self.html_tree = etree.parse(self.html_data, parser)
        else:
            self.html_tree = etree.fromstring(self.html_data, parser)

    def __init__(self, pageid):
        self.pageid = pageid
        self.newLine_nonBreak_pattern = re.compile(self.newLine_nonBreak_regex)
        self.es_ops = ElasticSearchOperate()
        wiki_data = self.es_ops.get_wiki_article(pageid)
        if wiki_data is not None and __wiki_raw__ in wiki_data:
            self.html_data = wiki_data[__wiki_raw__]
            # parser = etree.XMLParser(ns_clean=True, remove_comments=True)
            parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
            self.html_tree = etree.fromstring(self.html_data, parser)

    def strip_tag(self):

        toc_list = self.html_tree.xpath(self.toc_pattern)
        for toc in toc_list:
            toc.getparent().remove(toc)

        non_searchable_list = self.html_tree.xpath(self.non_searchable_pattern)
        for non_searchable in non_searchable_list:
            non_searchable.getparent().remove(non_searchable)

        dl_list = self.html_tree.xpath(self.description_list_pattern)
        for dl in dl_list:
            dl.getparent().remove(dl)

        ref_begin_list = self.html_tree.xpath(self.references_pattern)
        for ref_begin in ref_begin_list:
            ref_begin.getparent().remove(ref_begin)

        ref_list = self.html_tree.xpath(self.references_list_pattern)
        for ref in ref_list:
            ref.getparent().remove(ref)

        meta_data_list = self.html_tree.xpath(self.meta_data_box_pattern)
        for meta_data in meta_data_list:
            meta_data.getparent().remove(meta_data)

        meta_data_table = self.html_tree.xpath(self.meta_data_table)
        for meta_data in meta_data_table:
            meta_data.getparent().remove(meta_data)

        nav_box_list = self.html_tree.xpath(self.nav_boxes_pattern)
        for nav_box in nav_box_list:
            nav_box.getparent().remove(nav_box)

        vnav_box_list = self.html_tree.xpath(self.vertical_nav_boxes_pattern)
        for vnav_box in vnav_box_list:
            vnav_box.getparent().remove(vnav_box)

        no_print_list = self.html_tree.xpath(self.no_print_metadata_pattern)
        for no_print in no_print_list:
            no_print.getparent().remove(no_print)

        sub_ref_list = self.html_tree.xpath(self.subscript_pattern)
        for sub_ref in sub_ref_list:
            sub_ref.getparent().remove(sub_ref)

        edit_list = self.html_tree.xpath(self.edit_pattern)
        for edit in edit_list:
            edit.getparent().remove(edit)

        see_also_list = self.html_tree.xpath(self.see_also_pattern)
        for see_also in see_also_list:
            see_also_data = see_also.getparent().getnext()
            see_also_data.getparent().remove(see_also_data)

        external_link_list = self.html_tree.xpath(self.external_links_pattern)
        for external_link in external_link_list:
            external_link_data = external_link.getparent().getnext()
            external_link_data.getparent().remove(external_link_data)

    def strip_headings(self):
        for heading in self.irrelevant_headlines:
            heading_parent_list = self.html_tree.xpath(heading)
            if len(heading_parent_list) > 0:
                heading_parent = heading_parent_list[0].getparent()
                heading_parent.getparent().remove(heading_parent)

    def img_extract(self):
        img_list = self.html_tree.xpath(self.img_pattern)
        for img in img_list:
            img_url, img_caption = "", ""
            img_url_list = img.xpath(self.img_href)
            if len(img_url_list) > 0:
                img_url = str(img_url_list[0])
            img_caption_list = img.xpath(self.img_caption)
            if len(img_caption_list) > 0:
                img_caption = ''.join(img_caption_list).strip()
            img.getparent().remove(img)
            if img_url != "":
                self.extracted_img[img_url] = img_caption
        logger.debug("Extracted Images: %d", len(self.extracted_img))
        return self.extracted_img

    def extract_info(self):
        info_box = self.html_tree.xpath(self.info_box_pattern)
        wikii = WikiInfo()
        for info in info_box:
            info_key = info.xpath(self.info_box_item)
            info_list = []
            info_title = ""
            for ikey in info_key:
                info_key = ''.join(ikey.xpath(self.info_key_pattern)).strip()           # issues with &nbsp;    // https://stackoverflow.com/a/33829869/8646414
                info_value = ''.join(ikey.xpath(self.info_value_pattern)).strip()
                info_value = info_value.split('\n')
                info_value = [item.strip() for item in info_value]
                if info_key != "" and len(info_value) >= 1:
                    if info_title == "":
                        info_title = info_key
                    if info_value[0] != '':
                        info_pair = {info_key: info_value}
                        info_list.append(info_pair)
            wikii.add_info(info_title, info_list)
            info.getparent().remove(info)
        res = self.es_ops.update_wiki_article(self.pageid, content_info=json.dumps(wikii.info_data))
        if res:
            logger.info("Inserted parsed content info for: %d", self.pageid)
        else:
            logger.error("Inserted of parsed content info failed")
        logger.debug("Extracted Bios: %d", len(wikii.info_data))
        return wikii.info_data

    def extract_tables(self):
        table_list = self.html_tree.xpath(self.table_pattern)
        wikit = WikiTable()
        for table in table_list:
            table_row_list = table.xpath(self.table_row_pattern)
            for table_row in table_row_list:
                table_head_list = table_row.xpath(self.table_key_pattern)
                for table_head in table_head_list:
                    wikit.add_header(''.join(table_head.xpath(self.all_text_pattern)))
                tab_data = []
                table_data_list = table_row.xpath(self.table_value_pattern)
                for table_data in table_data_list:
                    tab_data.append(''.join(table_data.xpath(self.all_text_pattern)))
                wikit.set_values(tab_data)
            table.getparent().remove(table)
        res = self.es_ops.update_wiki_article(self.pageid, content_table=json.dumps(wikit.tab_data))
        if res:
            logger.info("Inserted parsed content table for: %d", self.pageid)
        else:
            logger.error("Inserted of parsed content table failed")
        logger.debug("Extracted Tables: %d", len(wikit.tab_data))
        return wikit.tab_data

    def extract_text(self):
        text_data = ''.join(self.html_tree.xpath(self.all_text_pattern)).strip()
        text_data = re.sub(self.newLine_nonBreak_pattern, ' ', text_data)
        res = self.es_ops.update_wiki_article(self.pageid, content=text_data)
        logger.debug("Parsed content length: %d", len(text_data))
        if res:
            logger.info("Inserted parsed content for: %d", self.pageid)
        else:
            logger.error("Inserted of parsed content failed")
        return text_data

    def save_html(self, page=0):
        html_str = etree.tostring(self.html_tree, pretty_print=True)
        with open(OUTPUT_DIR+'/wiki_content_cleaned_'+str(page)+'.html', 'wb') as fp:
            fp.write(html_str)


class WikiInfo:
    info_data = []

    # def __str__(self):
    #     return "%s: %s" % (self.info_key, self.info_value)

    def add_info(self, key, value):
        info_tuple = (key, value)
        self.info_data.append(info_tuple)


class WikiTable:
    description = ""
    tab_header = []
    tab_data = []

    def add_header(self, tab_header):
        self.tab_header.append(tab_header)

    def set_values(self, tab_values):
        zipped_list = list(zip(self.tab_header, tab_values))
        if len(zipped_list) > 0:
            self.tab_data.append(zipped_list)


def extract_wiki_pages(wiki_page_ids):
    for page in wiki_page_ids:
        xpe = XPathExtractor(page)
        xpe.strip_tag()
        xpe.strip_headings()
        # xpe.img_extract()     # TODO: Save with Elasticsearch
        xpe.extract_info()      # TODO: Save with Elasticsearch
        xpe.extract_tables()    # TODO: Save with Elasticsearch
        xpe.extract_text()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        parse_pageId = sys.argv[1:]
        # for page in parse_pageId:
        #     with open(OUTPUT_DIR+'/wiki_content_'+page+'.html', 'r') as fp:
        #         xpe = XPathExtractor(fp, True)
        #         xpe.strip_tag()
        #         xpe.strip_headings()
        #         print("Extracted Images:", xpe.img_extract())
        #         pprint([str(item) for item in xpe.extract_info()])
        #         pprint(xpe.extract_tables())
        #         print(xpe.extract_text())
        #         if SAVE_OUTPUTS:
        #             xpe.save_html(page)
        for lpage in parse_pageId:
            lxpe = XPathExtractor(lpage)
            lxpe.strip_tag()
            lxpe.strip_headings()
            print("Extracted Images:", lxpe.img_extract())
            pprint([str(item) for item in lxpe.extract_info()])
            pprint(lxpe.extract_tables())
            print(lxpe.extract_text())
            if SAVE_OUTPUTS:
                lxpe.save_html(lpage)
    else:
        raise ValueError('No page id provided for Wiki parse')