"""
Individuate messages by source
1-1 mapping between source and schema
Read from multiple Kafka topics simultaneously
Poll schema for changes/new schema
JSON
Configuration-based; no hard-coding.
Add/delete Kafka topics by configuration change
Poll configuration for changes
"""

import os
import sys
import json
import yaml
import time
import threading
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, RegexMatchingEventHandler, FileCreatedEvent
from trunk_club_streams.tc_kafka import TrunkClubKafkaListener

SCHEMA_DIRECTORY = os.environ['SCHEMA_DIRECTORY']
CONFIG_PATH = os.environ['CONFIG_PATH']

def event_happened(*args, **kwargs):
    pass

def file_modified(*args, **kwargs):
    print 'file modified:', args, kwargs

def file_deleted(event, **kwargs):
    print 'file deleted:', event, kwargs

def file_added(event, **kwargs):
    print 'file added:', event, kwargs

if __name__ == "__main__":
    event_handler = RegexMatchingEventHandler(regexes=['.*'], ignore_regexes=[], ignore_directories=False, case_sensitive=False)
    event_handler.on_any_event = event_happened
    event_handler.on_modified = file_modified
    event_handler.on_deleted = file_deleted
    # event_handler.on_created = file_added
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
