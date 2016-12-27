#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frida,sys

rdev = frida.get_remote_device()
session = rdev.attach("com.tencent.mm")
jscode = """
Interceptor.attach(Module.findExportByName("libwechatxlog.so" , "xlogger_Write"), {
    onEnter: function(args) {
        send(Memory.readUtf8String(args[1]));
        
    },
    onLeave:function(retval){
	   console.log(retval);
    }
});
"""

script = session.create_script(jscode)


def on_message(message ,data):
	print message['payload']
	
	
script.on("message" , on_message)
script.load()
sys.stdin.read()