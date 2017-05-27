from nanostream.nanostream_processor import (
    NanoStreamProcessor, NanoStreamSender)
from watchdog.observers import Observer
from watchdog.events import (
    LoggingEventHandler, FileModifiedEvent,
    RegexMatchingEventHandler, FileCreatedEvent)


class WatchdogDirectoryListener(NanoStreamSender):
    def __init__(
        self, regexes=None, ignore_directories=False,
            case_sensitive=True, watchdog_path='.', ignore_regexes=None):

        self.event_handler = RegexMatchingEventHandler(
            regexes=regexes or ['.*'],
            ignore_regexes=ignore_regexes or [],
            ignore_directories=ignore_directories,
            case_sensitive=case_sensitive)

        self.event_handler.on_modified = self.file_modified
        self.observer = Observer()
        self.observer.schedule(self.event_handler, watchdog_path, recursive=False)

        super(WatchdogDirectoryListener, self).__init__()

    def file_modified(self, *args, **kwargs):
        print 'file modified...'
        if not isinstance(args[0], FileModifiedEvent):
            return None  # NoneType is automatically ignored
        modified_file = args[0].src_path
        self.queue_message(modified_file)

    def start(self):
        self.observer.start()
