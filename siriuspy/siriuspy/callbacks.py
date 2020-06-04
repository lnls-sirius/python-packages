"""Generic class to handle callbacks."""


class Callback:
    """Generic class to handle callbacks."""

    def __init__(self, callback=None):
        """Initialize Instance.

        callback can be any callable or list/tuple of callables.
        """
        self._callbacks = dict()
        if callback is None:
            return
        elif isinstance(callback, (tuple, list)):
            for thiscb in callback:
                self.add_callback(thiscb)
        else:
            self.add_callback(callback)

    def add_callback(self, callback, index=None, **kw):
        """Add a callback to a PV.

        Optional keyword arguments set here will be preserved and passed
        on to the callback at runtime.

        Note that there might be multiple callbacks, so that each
        has a unique index (small integer) that is returned by
        add_callback.  This index is needed to remove a callback.
        """
        if not callable(callback):
            raise ValueError("Tried to set non callable as a callback")
        if index is None:
            index = 0
            if self._callbacks:
                index = 1 + max(self._callbacks.keys())
        self._callbacks[index] = (callback, kw)
        return index

    def remove_callback(self, index=None):
        """Remove a callback by index."""
        if index in self._callbacks:
            self._callbacks.pop(index)

    def clear_callbacks(self):
        """Clear all callbacks."""
        self._callbacks = {}

    def run_callbacks(self, *args, **kwd):
        """Run all user-defined callbacks with the current data.

        Normally, this is to be run automatically on event, but
        it is provided here as a separate function for testing
        purposes.
        """
        for index in sorted(list(self._callbacks.keys())):
            self.run_callback(index, *args, **kwd)

    def run_callback(self, index, *args, **kwd):
        """Run a specific user-defined callback, specified by index.

        Note that callback functions are called with keyword/val
        arguments including:
            - any positional argument for the specific application
            - any keyword argument for the specific application
            - keyword args included in add_callback()
            - keyword 'cb_info' = (index, self)
        where the 'cb_info' is provided as a hook so that a callback
        function  that fails may de-register itself.
        """
        try:
            fcn, kwargs = self._callbacks[index]
        except KeyError:
            return
        kwargs2use = kwargs.copy()
        kwargs2use.update(kwd)
        kwargs2use['cb_info'] = (index, self)
        if callable(fcn):
            fcn(*args, **kwargs2use)
