
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

from whoosh.analysis import SimpleAnalyzer
from html.parser import HTMLParser
from html import unescape
import dateutil.parser
import json
import os
import psutil
import struct


"""
<posts>
  <row Id="4" PostTypeId="1" AcceptedAnswerId="7" CreationDate="2008-07-31T21:42:52.667" Score="543" ViewCount="34799" Body="&lt;p&gt;I want to use a track-bar to change a form's opacity.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;This is my code:&lt;/p&gt;&#xA;&#xA;&lt;pre&gt;&lt;code&gt;decimal trans = trackBar1.Value / 5000;&#xA;this.Opacity = trans;&#xA;&lt;/code&gt;&lt;/pre&gt;&#xA;&#xA;&lt;p&gt;When I build the application, it gives the following error:&lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA;  &lt;p&gt;Cannot implicitly convert type &lt;code&gt;'decimal'&lt;/code&gt; to &lt;code&gt;'double'&lt;/code&gt;.&lt;/p&gt;&#xA;&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;I tried using &lt;code&gt;trans&lt;/code&gt; and &lt;code&gt;double&lt;/code&gt; but then the control doesn't work. This code worked fine in a past VB.NET project.&lt;/p&gt;&#xA;" OwnerUserId="8" LastEditorUserId="3151675" LastEditorDisplayName="Rich B" LastEditDate="2017-09-27T05:52:59.927" LastActivityDate="2018-02-22T16:40:13.577" Title="While applying opacity to a form, should we use a decimal or a double value?" Tags="&lt;c#&gt;&lt;winforms&gt;&lt;type-conversion&gt;&lt;decimal&gt;&lt;opacity&gt;" AnswerCount="13" CommentCount="1" FavoriteCount="39" CommunityOwnedDate="2012-10-31T16:42:47.213" />
"""

def stream(f):
    obj_str = ''
    f.read(50) # eat header and <posts>\n
    while True:
        c = f.read(1)
        if not c:
            print('EOF')
            break
        obj_str = obj_str + c
        if c == '\n':
            obj_str = obj_str.replace('u"', '"')
            yield bf.data(fromstring(obj_str))
            obj_str = ''
            c = f.read(1) # eat space


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class doc:
    def __init__(self, id, date, viewcount):
        self.id = id
        self.date = int(date)
        self.viewcount = int(viewcount)

    def __str__(self):
        return str(self.id) + ',' + str(self.date) + ',' + str(self.viewcount)

def indexer(obj, inv_idx, tokenizer):
    row = obj['row']
    title = u''
    view_count = -1
    if '@Title' in row:
        title = row['@Title']
    if '@ViewCount' in row:
        view_count = int(row['@ViewCount'])
    body = strip_tags(unescape( row['@Body'] ))
    datetime = dateutil.parser.parse(row['@CreationDate'])
    thisdoc = set()
    for token in tokenizer(body):
        if token.text in thisdoc:
            continue
        thisdoc.add(token.text)
        if token.text not in inv_idx:
            inv_idx[token.text] = list()
        inv_idx[token.text].append( doc(int(row['@Id']), datetime.timestamp(), view_count) )

if __name__ == "__main__":
    cnt = 0

    inv_idx = dict()
    tokenizer = SimpleAnalyzer()

    f = open('../data/Posts.xml', encoding="utf8")
    posts = stream(f)
    for x in posts:
        if cnt % 1000 == 0:
            process = psutil.Process(os.getpid())
            print('docs: ', cnt, 'tokens:', len(inv_idx), 'mem:', process.memory_info().rss)
        try:
            indexer(x, inv_idx, tokenizer)
        except:
            pass
        cnt += 1

    print('Writing')
    with open('./post_inv_idx.json', mode='wb') as w:
        for key in sorted(inv_idx):
            w.write(bytes(key, encoding="utf8"))
            for v in inv_idx[key]:
                w.write(struct.pack('i', v.id))
                w.write(struct.pack('i', v.date))
                w.write(struct.pack('i', v.viewcount))
            w.write(bytes('\n', encoding="utf8"))