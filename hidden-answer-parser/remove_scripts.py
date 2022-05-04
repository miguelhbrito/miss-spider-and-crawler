import os

from bs4 import BeautifulSoup

INPUT_PATH = './results/'
if not INPUT_PATH.endswith('/'):
    INPUT_PATH += '/'

OUTPUT_PATH = './no-script'

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

post_tags = os.listdir(INPUT_PATH)

posts = []
for tag in post_tags:
    #print(tag)
    tag_path = INPUT_PATH + tag

    all_posts_path = os.listdir(tag_path)

    for html_file in all_posts_path:
        html_path = '{}/{}'.format(tag_path, html_file)

        with open(html_path, 'r') as html_file_handler:
            html_lines = html_file_handler.readlines()

        html_content = ''.join(html_lines)
        parsed_html = BeautifulSoup(html_content, 'html.parser')

        for script_tag in parsed_html.findAll('script'):
            script_tag.extract()
        
        for span_tag in parsed_html.findAll('span',{'class':'qa-activity-count-data'}):
            span_tag.extract()
        
        for span_tag in parsed_html.findAll('span',{'class':'qa-c-item-who-points-data'}):
            span_tag.extract()
        
        for span_tag in parsed_html.findAll('span',{'class':'qa-q-view-who-points-data'}):
            span_tag.extract()
        
        for span_tag in parsed_html.findAll('span',{'class':'qa-a-item-who-points-data'}):
            span_tag.extract()
        
        #for span_tag in parsed_html.findAll('span'):
        #    span_tag.extract()

        no_script_path = '{}/{}/{}'.format(OUTPUT_PATH, tag, html_file)
        directory, file = os.path.split(no_script_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(no_script_path, 'w') as no_script_file:
            no_script_file.write(str(parsed_html))
