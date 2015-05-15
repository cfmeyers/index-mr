
target = open('urls_to_2013.txt', 'w')
target.truncate()

with open('sitemap.xml') as f:
    content = f.readlines()
    for row in content:
        if 'loc' in row:
            url =  row.replace('<loc>', '').replace('</loc>','').strip()
            target.write(url+'\n')

target.close()


