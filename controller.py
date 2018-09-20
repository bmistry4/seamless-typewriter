from model.video_searcher import VideoSearcher


class Controller:
    """Controller for the MVC framework that bridges between the model and view, defining the interface between them"""
    def __init__(self):
        self.model = None
        self.view = None

    def set_view(self, view):
        """Set reference to view object"""
        self.view = view

    def index_video(self, path, thread_queue):
        """Creates model for video given by path, which automatically indexes the video"""
        self.model = VideoSearcher(path)
        thread_queue.put("this can literally be anything")

    def get_timestamps(self, search_term):
        """Get search term timestamp results from the model"""
        if self.model is None:
            return None
        else:
            return self.model.get_timestamps(search_term)
