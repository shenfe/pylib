# coding: utf8

from __future__ import print_function

import os
import sys
import json
from importlib import import_module

import click

from libpy.config import parse_config


class Attrs:
    def __repr__(self):
        return 'Attrs(%s)' % ', '.join('%s=%s' % kv for kv in vars(self).items())


@click.group()
@click.option('--config-file', default='')
@click.option('--config-json', default='')
@click.option('--config-module', default='', help='python module that contains the config object')
@click.pass_context
def main(context, config_file, config_json, config_module):
    '''
    Configs can be passed by file or directly from json.
    If neither `--config-file` or `--config-json` is passed, attempts to read the file from stdin.
    '''
    context.obj = Attrs()

    def load_config():
        # Cache the config object so it can be accessed multiple times
        if not hasattr(context.obj, 'config'):
            if config_module:
                context.obj.config = import_module(config_module).config
            else:
                if config_file:
                    with open(config_file) as f:
                        config = json.load(f)
                elif config_json:
                    config = json.loads(config_json)
                else:
                    click.echo('No config file specified, reading from stdin')
                    config = json.load(sys.stdin)
                context.obj.config = parse_config(config)
        return context.obj.config

    context.obj.load_config = load_config

    print('main')


@main.command()
@click.option('--use-gpu/--no-gpu', default=True, help='Run with GPU or not.')
@click.pass_context
def fn1(context, use_gpu):
    config = context.obj.load_config()
    print(config)
    print('this is a function')
    if use_gpu:
        print('using gpu')
    else:
        print('not using gpu')


@main.command()
@click.pass_context
def fn2(context):
    config = context.obj.load_config()
    print(config)
    print('this is just another function')
