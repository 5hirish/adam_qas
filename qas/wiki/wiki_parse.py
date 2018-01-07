from lxml import etree

from qas.constants import OUTPUT_DIR, SAVE_OUTPUTS
"""
Parsing with XPath 1.0 query
XPath Documentation : https://developer.mozilla.org/en-US/docs/Web/XPath
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

    irrelevant_headlines = ['''//*[@id="See_also"]''', '''//*[@id="Notes_and_references"]''',
                            '''//*[@id="Explanatory_notes"]''', '''//*[@id="Citations"]''',
                            '''//*[@id="Further_reading"]''', '''//*[@id="External_links"]''']

    html_data = ''
    html_tree = None
    isFile = False

    def __init__(self, html_data, isFile):
        self.html_data = html_data
        parser = etree.XMLParser(ns_clean=True, remove_comments=True)
        if isFile:
            self.html_tree = etree.parse(self.html_data, parser)
        else:
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

    def strip_headings(self):
        for heading in self.irrelevant_headlines:
            heading_parent = self.html_tree.xpath(heading)[0].getparent()
            heading_parent.getparent().remove(heading_parent)

    def save_html(self):
        html_str = etree.tostring(self.html_tree, pretty_print=True)
        with open(OUTPUT_DIR+'/wiki_content_cleaned.html', 'wb') as fp:
            fp.write(html_str)


if __name__ == "__main__":
    with open(OUTPUT_DIR+'/wiki_content.html', 'r') as fp:
        xpe = XPathExtractor(fp, True)
        xpe.strip_tag()
        xpe.strip_headings()
        if SAVE_OUTPUTS:
            xpe.save_html()
