from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LookupDriveEvents(FileSystemEventHandler):

    def on_created(self,event):
        print('on_created : {}'.format(event.src_path))
    def on_deleted(self,event):
        print('on_deleted : {}'.format(event.src_path))
    def on_moved(self,event):
        print('on_moved : {}'.format(event.src_path))

if __name__ == '__main__':
    observer = Observer()
    event_handler = LookupDriveEvents()
    observer.schedule(event_handler = event_handler,path = 'C:\\',recursive=True)
    observer.start()
    observer.join()
