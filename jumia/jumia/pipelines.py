# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import unicodedata
import w3lib.html
from itemadapter import ItemAdapter


def normalize_product_details(text):
    text = w3lib.html.remove_tags(text)
    text = text.replace('\xa0', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('\u200b', '')
    return text.replace('\n', ' ')


def normalize_features(key_features_list):
    if len(key_features_list) == 0:
        return None
    else:
        normalized_keys = [text.replace('\xa0', ' ').replace('&amp;', '&').replace('·', '').replace('\n', '')
                           for text in key_features_list]
        return [values.strip() for values in normalized_keys]


class JumiaPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        adjust_data = ['sku', 'gtin', 'material', 'weight', 'country']
        for field in adjust_data:
            value = adapter.get(field)
            if value:
                value = value.split()[-1]
                adapter[field] = value
            else:
                adapter[field] = None

        if adapter.get('material') == '-':
            adapter['material'] = None

        price_string = adapter.get('price')
        adapter['price'] = price_string.split()[-1].replace(',', '')

        prd_detail_str = adapter.get('product_detail')
        adapter['product_detail'] = normalize_product_details(prd_detail_str)

        key_features_list = adapter.get('key_features')
        adapter['key_features'] = normalize_features(key_features_list)

        return item
