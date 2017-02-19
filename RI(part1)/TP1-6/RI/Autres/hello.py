A = {1:21,3:37,57:13}
from collections import OrderedDict

A = OrderedDict(sorted(A.items(), key=lambda t: t[1], reverse=True))
print A.keys()

print A
