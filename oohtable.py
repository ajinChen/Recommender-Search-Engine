"""
Implement the hashtable class as the dic() in the python
__len__, __setitem__, __getitem__, __contain__  -->  O(1)
__keys__, __items__, __str__, __repr__  -->  O(n)
"""
class HashTable(object):

    def __init__(self, nbuckets):
        self.size = 0
        self.nbuckets = nbuckets
        self.htable = [[] for _ in range(nbuckets)]


    def __len__(self):
        return self.size


    def __setitem__(self, key, value):
        find = self.getindex(key)
        if not find:
            self.size += 1
            self.htable[self.key2code(key)].append((key, value))
        else:
            h_code, idx = find
            self.htable[h_code][idx] = (key, value)


    def __getitem__(self, key):
        find = self.getindex(key)
        if find:
            h_code, idx = find
            return self.htable[h_code][idx][1]
        return None


    def __contains__(self, key):
        return key in [tup[0] for tup in self.htable[self.key2code(key)]]


    def __iter__(self):
        for key in self.keys():
            yield key


    def __repr__(self):
        output = ''
        for idx, bucket in enumerate(self.htable):
            output += f"{idx:04d}->"
            if not bucket:
                output += "\n"
            else:
                line = [f"{tup[0]}:{tup[1]}" for tup in bucket]
                output += ', '.join(line) + "\n"
        return output


    def __str__(self):
        res = []
        for bucket in self.htable:
            for tup in bucket:
                res.append(f"{tup[0]}:{tup[1]}")
        return '{' + ", ".join(res) + '}'


    def keys(self):
        res = []
        for bucket in self.htable:
            for tup in bucket:
                res.append(tup[0])
        return res


    def items(self):
        res = []
        for bucket in self.htable:
            for tup in bucket:
                res.append(tup)
        return res


    def key2code(self, key):
        if isinstance(key, int):
            h = key
        elif isinstance(key, str):
            h = 0
            for c in key:
                h = h * 31 + ord(c)
        else:
            h = None
        return h % self.nbuckets


    def getindex(self, key):
        h_code = self.key2code(key)
        bucket = self.htable[h_code]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return (h_code, i)
        return None