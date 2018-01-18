import boto3
import hashlib
import logging
from datetime import datetime

logging.config.fileConfig(fname="logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("url_logger")

SEPARATOR = "/"
s3 = boto3.resource('s3')
bucket = s3.Bucket() #specify bucket name
boto3.set_stream_logger('boto3', logging.WARNING)

def generate_filename(url):
    '''
    Generate output file name from url.
    Parameter
     url(str) : URL
    Return
     File name made by url and date.
    '''
    split_url = url.split("//")[-1].split("/")
    domain = split_url[0].translate(str.maketrans('./\\','-__'))
    path = ""
    if len(split_url) > 1:
        path = "_".join(split_url[1:])
    path_hash = hashlib.md5(path.encode("utf-8")).hexdigest()

    return datetime.now().strftime('%y%m%d') + "/%s_%s.html" % (domain, path_hash)

def save2file(scrapy_response):
    ''' 
    Save renponse html to file. 
    Parameter
     scrapy_response : Scrapy's response object.
    Return
     Return true if success save html file. 
    '''
    try:
        filename = generate_filename(scrapy_response.url.replace('\n', ''))
        html = scrapy_response.body
    except:
        # None or not response object
        raise
    try:
        bucket.Object(filename).put(Body = html)

        # logging
        logger.debug(scrapy_response.url.replace('\n', '') + ", " + filename)
    except:
        raise
    return True

