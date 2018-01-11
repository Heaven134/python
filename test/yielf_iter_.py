# -*- coding: utf-8 -*-
import sys
import time
class Fab(object):
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def next(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()

for n in Fab(10):
    print n




def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
print '----------['
for n in fab(5):
    print n

print '-------------'
f=fab(3)
print f.next()
print f.next()
print f.next()







print "Fabs -------------"

class Fabs(object):
    def __init__(self,max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1  #特别指出：第0项是0，第1项是第一个1.整个数列从1开始
    def __iter__(self):
        print "Fabs __iter__"
        return self
    def next(self):
        print "Fabs next"
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()

print Fabs(5)
for key in Fabs(5):
    print key












print "listiter --------"

#sys.exit()
class ListIterator(object):
    def __init__(self, data):
        print 'ListIterator __init__'
        self.__data = data
        self.__count = 0

    def __iter__(self):
        print("call iterator __iter__().")
        return self

    def next(self):
        print("call iterator __next__().")
        if self.__count < len(self.__data):
            val = self.__data[self.__count]
            self.__count += 1
            return val
        else:
            raise StopIteration

class ListIterable(object):
    def __init__(self, data):
        print "ListIterable __init__"
        self.__data = data

    def __iter__(self):
        print("call iterable __iter__().")
        return ListIterator(self.__data)


a = ListIterable([1,2,4,5,6])
b = a.__iter__()
a
b

print '------'
#for i in ListIterator([1,2,4,5,6]):
    #print i
[i for i in a]


print 'logtailer-------'
def push_counter(counter, ctype):
    print counter
    print ctype
    print 123
    t = ""
    for k in counter:
        print k
        print 234
        if len(t) > 65000:
            yield t
            t = "%s:%s|%s" % (k,counter[k],ctype)
        else:
            t += "\n%s:%s|%s" % (k,counter[k],ctype)
    yield t
    print 345

counter_buffer={}
counter_buffer[1]={}
counter_buffer[1]['wesync.kylin_realtime_data.byhost.10_77_128_21.flow.10_77_128_90.hits']=1
counter_buffer[1]['wesync.kylin_realtime_data.byhost.10_77_128_21.flow.10_77_128_90.hits']=1
counter_buffer[2]={}
counter_buffer[2]['wesync.kylin_realtime_data.byhost.10_77_128_21.flow.10_77_128_90.hits12345678']=1
counter_buffer[2]['wesync.kylin_realtime_data.byhost.10_77_128_21.flow.10_77_128_90.hits12345678']=1
nodes = ['10.13.81.24:8100','10.13.81.25:8100','10.13.81.26:8100','10.13.81.27:8100','10.13.81.29:8100','10.13.81.30:8100','10.13.81.24:8101','10.13.81.25:8101','10.13.81.26:8101','10.13.81.27:8101','10.13.81.29:8101','10.13.81.30:8101','10.13.80.27:8100','10.13.80.27:8200','10.13.80.28:8100','10.13.80.28:8200','10.13.80.29:8100','10.13.80.29:8200','10.13.80.30:8100','10.13.80.30:8200','10.13.80.31:8100','10.13.80.31:8200','10.13.80.32:8100','10.13.80.32:8200','10.13.80.32:8100','10.13.80.32:8200','10.13.80.31:8100','10.13.80.31:8200','10.13.80.30:8100','10.13.80.30:8200']
for i in counter_buffer:
    print i
    if not counter_buffer[i]:
        continue
    mc = push_counter(counter_buffer[i], 'c')
    counter_buffer[i] = {}
    last_flush = time.time()
    print 'mc--------'
    print mc
    for _mc in mc:
        print '~~~~~~~~~'
        print _mc
        hash_value = nodes[i]
        if True:
            host = hash_value.split(":")[0]
            port = hash_value.split(":")[1]
        print (_mc,host,port)
