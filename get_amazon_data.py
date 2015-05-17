import os
from amazon.api import AmazonAPI


AMAZON_ACCESS_KEY = os.environ['AMAZON_ACCESS_KEY']

AMAZON_SECRET_KEY = os.environ['AMAZON_SECRET_KEY']
AMAZON_ASSOC_TAG = os.environ['AMAZON_ASSOC_TAG']

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

asic = '0810125838'
product = amazon.lookup(ItemId=asic)
print product.title
print product.author
print product.medium_image_url
print product.get_attribute('ProductGroup') #e.g. Book, DVD, etc

for node in product.browse_nodes:
    print node.name
    print node.id


