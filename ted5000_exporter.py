#!/usr/bin/python
import time
import xml.etree.ElementTree
import urllib2
import tornado.ioloop
import tornado.web

class MetricHandler(tornado.web.RequestHandler):
    def get(self):
        data = []
        self.set_header("Content-Type", 'text/plain; charset="utf-8"')
	ip = self.get_argument("target", None, True)
        response = urllib2.urlopen('http://%s/api/LiveData.xml'%(ip))
        xmldata = response.read()
        e = xml.etree.ElementTree.fromstring(xmldata)

        for mtus in e.findall('Voltage'):
            for mtu in mtus:
                value = mtu.findall('VoltageNow')[0]
                data.append ( {"type" : "voltage", "name" : mtu.tag , "value" : float(value.text)/10 } )
        for mtus in e.findall('Power'):
            for mtu in mtus:
                value = mtu.findall('PowerNow')[0]
                data.append ( {"type" : "power", "name" : mtu.tag , "value" : float(value.text) } )

        for entry in data:
            self.write('ted5000_%s{mtu="%s"} %f\n'%(entry['type'], entry['name'], entry['value']))

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/metrics", MetricHandler),
    ])
    application.listen(9117)
    tornado.ioloop.IOLoop.instance().start()
