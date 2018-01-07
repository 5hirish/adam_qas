from lxml import etree
from qas.constants import OUTPUT_DIR
"""
Parsing with XPath 1.0 query
"""


class XPathExtractor:

    regexpNS = "http://exslt.org/regular-expressions"

    toc_pattern = '''//*[@id="toc"]'''
    non_searchable_pattern = '''/div/div[starts-with(@class, "hatnote")]'''
    description_list_pattern = '''/div/dl'''
    references_pattern = '''/div/div[starts-with(@class, "refbegin")]'''
    references_list_pattern = '''/div/div[@class="reflist"]'''
    meta_data_box_pattern = '''/div/div[starts-with(@class, "metadata")]'''
    nav_boxes_pattern = '''/div/div[@class="navbox"]'''
    vertical_nav_boxes_pattern = '''/div/div[starts-with(@class, "vertical-navbox")]'''
    no_print_metadata_pattern = '''/div/div[starts-with(@class, "noprint")]'''

    see_also_pattern = '''//*[@id="See_also"]'''
    external_links_pattern = '''//*[@id="External_links"]'''

    html_data = ''
    html_tree = None

    def __init__(self, html_file):
        self.html_data = html_file
        parser = etree.XMLParser(ns_clean=True, remove_comments=True)
        self.html_tree = etree.parse(self.html_data, parser)

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

        nav_box_list = self.html_tree.xpath(self.nav_boxes_pattern)
        for nav_box in nav_box_list:
            nav_box.getparent().remove(nav_box)

        vnav_box_list = self.html_tree.xpath(self.vertical_nav_boxes_pattern)
        for vnav_box in vnav_box_list:
            vnav_box.getparent().remove(vnav_box)

        no_print_list = self.html_tree.xpath(self.no_print_metadata_pattern)
        for no_print in no_print_list:
            no_print.getparent().remove(no_print)

        see_also_list = self.html_tree.xpath(self.see_also_pattern)
        for see_also in see_also_list:
            see_also_data = see_also.getparent().getnext()
            see_also_data.getparent().remove(see_also_data)

        external_link_list = self.html_tree.xpath(self.external_links_pattern)
        for external_link in external_link_list:
            external_link_data = external_link.getparent().getnext()
            external_link_data.getparent().remove(external_link_data)




    def save_html(self):
        html_str = etree.tostring(self.html_tree, pretty_print=True)
        with open(OUTPUT_DIR+'/wiki_content_cleaned.html', 'wb') as fp:
            fp.write(html_str)


with open(OUTPUT_DIR+'/wiki_content.html', 'r') as fp:
    xpe = XPathExtractor(fp)
    xpe.strip_tag()
    xpe.save_html()
