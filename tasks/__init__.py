from invoke import Collection

from . import ado, cruft, docs, performance, quality, search, test

ns = Collection()
ns.add_collection(quality, name="qa")
ns.add_collection(docs)
ns.add_collection(test)
ns.add_collection(ado)
ns.add_collection(cruft)
ns.add_collection(search)
ns.add_collection(performance)


from . import notebook

ns.add_collection(notebook, name="nb")
