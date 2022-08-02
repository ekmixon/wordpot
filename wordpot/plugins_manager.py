#!/usr/bin/env python

from flask import request
from wordpot.logger import *
import os
import configparser

CURRENTPATH = os.path.abspath(os.path.dirname(__file__))

class PluginsManager():
    def __init__(self):
        self.plugins_path = os.path.join(CURRENTPATH, 'plugins/') 

        self.plugins_loaded = {'plugins': [], 'themes': [], 'admin': [], 'commons': []}
        return

    def _import_plugin(self, name):
        mod = __import__(name)
        components = name.split('.')
        for c in components[1:]:
            mod = getattr(mod, c)
        return mod

    def load(self):
        for root, dirs, files in os.walk(self.plugins_path):
            for file in files:
                if file[-3:] == '.py' and file != '__init__.py':
                    modname = f'wordpot.plugins.{file[:-3]}'
                    plugin = self._import_plugin(modname).Plugin()
                    plugin._load_config(file[:-3])

                    # Add to loaded list organized by categories
                    if plugin.hooks != None:
                        for h in plugin.hooks:
                            self.plugins_loaded[h].append(plugin)

    def hook(self, hook):
        return self.plugins_loaded[hook]
                    
class BasePlugin(object):
    def __init__(self, slug=None):
        self.name           = None
        self.author         = None
        self.link           = None  
        self.description    = None
        self.version        = None
        
        self.slug           = None
        self.hooks          = None

        self.request        = None

        self.inputs         = {}
        self.outputs        = {}

    def _load_config(self, slug=None):
        self.slug = slug
        try:
            config = ConfigParser.ConfigParser()
            plugin_config = os.path.join(CURRENTPATH, f'plugins/{self.slug}.ini')

            config.read(plugin_config)

            self.name = config.get('plugin', 'name')
            self.author = config.get('plugin', 'author')
            self.link = config.get('plugin', 'link')
            self.description = config.get('plugin', 'description')
            self.version = config.get('plugin', 'version')

            self.hooks = [v.strip() for v in config.get('plugin', 'hooks').split(',')]
        except Exception as e:
            pass
    
    def start(self, **kwargs):
        self.outputs = {}

        self.inputs = dict(kwargs.iteritems())
        try:
            self.run()
        except Exception as e:
            LOGGER.error('Unable to run plugin: %s\n%s', self.name, e.message)

    def run(self):
        return

    def to_json_log(self, **kwargs):
        import json
        return json.dumps(dict(kwargs, 
            source_ip=self.inputs['request'].remote_addr, 
            source_port=self.inputs['request'].environ['REMOTE_PORT'],
            dest_ip=self.inputs['request'].environ['SERVER_NAME'],
            dest_port=self.inputs['request'].environ['SERVER_PORT'],
            user_agent=self.inputs['request'].user_agent.string,
            url=self.inputs['request'].url
        ))
