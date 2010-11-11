'''
Created on Oct 22, 2010
@author: Stephen O'Hara
'''
# PyVision License
#
# Copyright (c) 2006-2008 Stephen O'Hara
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# 3. Neither name of copyright holders nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
# 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

class ImageBuffer:
    '''
    Stores a limited number of images from a video (or any other source)
    Makes it easy to do N-frame-differencing, for example, by easily being
    able to get the current (middle) frame, plus the first and last frames of the
    buffer. With an ImageBuffer of size N, as images are added, eventually the
    buffer fills, and older items are dropped off the end. This is convenient
    for streaming input sources, as the user can simply keep adding images
    to this buffer, and internally, the most recent N will be kept available.
    '''

    def __init__(self, N=5):
        '''
        @param N: how many image frames to buffer
        '''
        self._data = [None for i in xrange(N)]
        self._count = 0
        self._max = N
            
    def __getitem__(self, key):
        return self._data[key]
        
    def __len__(self):
        '''
        This is a fixed-sized ring buffer, so length is always the number
        of images that can be stored in the buffer (as initialized with Nframes)
        '''
        return self._max
    
    def isFull(self):
        if self._count == self._max:
            return True
        else:
            return False
            
    def clear(self):
        self._data = [None for i in xrange(self._max)]
        self._count = 0
            
    def getCount(self):
        '''
        Note that getCount() differs from __len__() in that this method returns the number of
        image actually stored in the ImageBuffer, while __len__() returns the size of the buffer,
        defined as the number of images the buffer is allowed to store.
        '''
        return self._count
    
    def getBuffer(self):
        return self._data
            
    def getFirst(self):
        return self._data[0]
    
    def getLast(self):
        return self._data[-1]
    
    def getMiddle(self):
        mid = int(self._count/2)
        return self._data[mid]
            
    def add(self, image):
        '''
        add an image to the buffer, will kick out the oldest of the buffer is full
        @param  image: image to add to buffer
        '''
        self._data.pop(0)  #remove last, if just beginning, this will be None
        self._data.append(image)
        self._count += 1
        if(self._count > self._max):
            self._count = self._max
            
    