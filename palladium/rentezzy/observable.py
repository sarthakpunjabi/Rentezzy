"""
This is Subject for Property discount - Observer Pattern.
"""


class Observable:
    """
    Observable class.
    """
    def __init__(self, lst=[]):
        self.callbacks = lst

    def subscribe(self, callback):
        """
        Method for adding subscribers to notify.
        """
        self.callbacks.append(callback)

    def notify(self):
        """
        Method for Notifying the list of subscribers.
        """
        for callback_function in self.callbacks:
            callback_function()
