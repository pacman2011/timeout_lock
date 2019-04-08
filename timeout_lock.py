""" A locking mechanism that is similar to :class:`threading.Lock`, but implements Timeout on the
acquire method via an internal :class:`threading.Event` flag.

Copyright (C) 2019 Shane Matthijs Boissevain

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.

If not, see <https://www.gnu.org/licenses/>.
"""
##
# Python Imports
import threading


class Timeout_Lock(object):
    """ By implementing an internal :class:`threading.Event` flag as the locking mechanism, it is
    possible to leverage the :meth:`threading.Event.wait` function in order to gracefully wait for
    the lock to become available, while also implementing a timeout feature.

    This is accomplished by "flipping" the internal :class:`threading.Event` flag around.
        **IE:** When the lock is free, the event is ``True``; when locked, the flag is ``False``.

    :ivar str name: The name of this lock. Defaults to the class name.

    :vartype __event: :class:`threading.Event`
    :ivar    __event: The underlying event that actually "controls" the lock mechanism.
    """
    def __init__(self, Name=None):
        ##
        # Instance Variables
        if Name == None:
            self.name = self.__class__.__name__
        else:
            self.name = str(Name)
        self.__event = threading.Event()
        self.__event.set()


    def __str__(self):
        if self.available:
            return self.name + " (Available)"
        return self.name + " (NOT Available)"


    ##############
    # Properties #
    ##############
    @property
    def available(self):
        """ While not useful for acquiring or releasing the lock, provides some use in logging and
        logical tests.

        :rtype:   bool
        :returns: ``True`` if calls to acquire would return immediately and acquire the lock.
        """
        return self.__event.is_set()

    @property
    def locked(self):
        """ While not useful for acquiring or releasing the lock, provides some use in logging and
        logical tests.

        :rtype:   bool
        :returns: ``True`` if calls to acquire would block.
        """
        return not self.available


    ####################
    # Public Functions #
    ####################
    def acquire(self, Timeout=None):
        """ Acquires the lock so that all further calls will either return ``False`` if the lock is
        not released before Timeout.

        :type  Timeout: int
        :param Timeout: Number of seconds to wait for the lock to become available. ``None``
            (the default) will block until :func:`~timeout_lock.Timeout_Lock.release` is called.

        .. warning::
            A ``Timeout`` value of ``None`` can deadlock the application if the lock never becomes
            available.

        :rtype:   bool
        :returns: ``True`` if the lock was acquired. ``False`` if the lock was not acquired within
            ``Timeout`` seconds.
        """
        if Timeout == None:
            self.__event.wait()
            self.__event.clear()
            return True
        else:
            if not self.__event.wait(Timeout):
                return False
            self.__event.clear()
            return True


    def release(self):
        """ Releases the lock so that other calls can acquire the lock.
        """
        if not self.__event.is_set():
            self.__event.set()
