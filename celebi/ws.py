#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015
# Gmail:liuzheng712
#

from ansible import playbook, callbacks

import tornado.web
import tornado.ioloop
import tornado.websocket
import os, sys
import subprocess
import time
import StringIO
import json


class Index(tornado.web.RequestHandler):
    def get(self):
        self.render('./static/index.html')


def run_playbook(playbook_path, hosts_path):
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=0)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=0)
    playbook.PlayBook(
        playbook=playbook_path,
        host_list=hosts_path,
        stats=stats,
        forks=4,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
    ).run()

    return stats


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 300

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def check_origin(self, origin):
        return True

    def open(self):
        print "Chat WebSocket Open"

    def on_close(self):
        print "Chat WebSocket Clost"

    def on_message(self, e):
        print "on_message "
        send = {"msg": e, "time": time.mktime(time.localtime())}
        self.write_message(json.dumps(send))


class PLSocketHandler(tornado.websocket.WebSocketHandler):
    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def check_origin(self, origin):
        return True

    def open(self):
        print "Playbook WebSocket Open"

    def on_close(self):
        print "Playbook WebSocket Close"

    def on_message(self, e):
        command = e
        print command
        if command.strip() == "ping -c 4 localhost":
            # stdout = sys.stdout
            # sys.stdout = file = StringIO.StringIO()
            # self.write_message(file.getvalue())
            # for nextline in iter(child.stdout.readline, b''):
            # self.write_message("[ "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+"] "+nextline)
            # child.stdout.close()
            # child.wait()
            child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            while True:
                nextline = child.stdout.readline()
                if nextline.strip() == "" and child.poll() != None:
                    break
                self.write_message("[ " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] " + nextline)
        elif command.strip() == "ansible-playbook -i hosts test.yml":
            callbacks.AggregateStats.compute = self.compute
            stats = run_playbook(
                playbook_path='./test.yml',
                hosts_path='./hosts',
            )
        else:
            self.write_message("Input Error")


    def compute(self, runner_results, setup=False, poll=False, ignore_errors=False):
        ''' walk through all results and increment stats '''

        for (host, value) in runner_results.get('contacted', {}).iteritems():
            # if not ignore_errors and (('failed' in value and bool(value['failed'])) or
            # ('failed_when_result' in value and [value['failed_when_result']] or ['rc' in value and value['rc'] != 0])[0]):
            # callbacks.AggregateStats()._increment('failures', host)
            #     elif 'skipped' in value and bool(value['skipped']):
            #         callbacks.AggregateStats()._increment('skipped', host)
            #     elif 'changed' in value and bool(value['changed']):
            #         if not setup and not poll:
            #             callbacks.AggregateStats()._increment('changed', host)
            #         callbacks.AggregateStats()._increment('ok', host)
            #     else:
            #         if not poll or ('finished' in value and bool(value['finished'])):
            #             callbacks.AggregateStats()._increment('ok', host)
            global lazy_out
            lazy_out = runner_results
            self.write_message("liuzheng: " + json.dumps(host) + " => " + json.dumps(value))

            # for (host, value) in runner_results.get('dark', {}).iteritems():
            #     callbacks.AggregateStats()._increment('dark', host)


if __name__ == '__main__':
    app = tornado.web.Application([
        ('/playbook', PLSocketHandler),
        ('/chat', ChatSocketHandler),
    ])
    app.listen(8001)
    tornado.ioloop.IOLoop.instance().start()