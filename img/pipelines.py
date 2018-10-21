import urllib2
import os


class ImgPipeline(object):
    x=1

    def process_item(self, item, spider):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        req = urllib2.Request(url=item['pic_url'], headers=headers)
        res = urllib2.urlopen(req)
        if os.path.exists('/Users/apple/Desktop/down/' + item['name']):
            file_name = os.path.join(r'/Users/apple/Desktop/down/', item['name'] + '/' + item['pic_name'] + '.jpg')
        else:
            os.makedirs('/Users/apple/Desktop/down/' + item['name'])
            file_name = os.path.join(r'/Users/apple/Desktop/down/', item['name'] + '/' + item['pic_name'] + '.jpg')
        with open(file_name, 'wb') as fp:
            fp.write(res.read())