from whoosh.qparser import QueryParser
from stackoverflow_index import indexer
from whoosh import index
from whoosh.query import Phrase

ix = index.open_dir("stackoverflow_idx", readonly=True)

#qp = QueryParser("body", schema=ix.schema)
q = Phrase("body", [u"import", u"os"])

with ix.searcher() as s:
    results = s.search(q, scored=False, sortedby=None, limit=None)
    print(results)

