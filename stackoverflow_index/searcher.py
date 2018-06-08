from whoosh.qparser import QueryParser
from whoosh import index
from whoosh.qparser.dateparse import DateParserPlugin

ix = index.open_dir("stackoverflow_idx", readonly=True)

qp = QueryParser("body", schema=ix.schema)
qp.add_plugin(DateParserPlugin(free=True))
q = qp.parse(u'creation_date:[20000101 to 20080901] "import os"')

with ix.searcher() as s:
    results = s.search(q, scored=False, sortedby=None, limit=None)
    print(results)

