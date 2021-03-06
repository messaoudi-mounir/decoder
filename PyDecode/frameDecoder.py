from symbol_generation import generateSymbols, generateIdentifiers
from frame_generation import generate
from copy import copy

def match_frame(data,frames):

    if len(data) <= 1:
        return None
    
    #for i, frame in enumerate(frames):
        #    print data, frame, len(data), len(frame), data[0].value, frame.identifier.value

    #    print data[0].value == frame.identifier.value 
    #    print len(frame) == len(data)
        
    #found_frame = [frame for i, frame in enumerate(frames) if data[0].value == frame.identifier.value and len(frame) == len(data)]

    found_frame = frames[data[0].value]
    
    #print data[0].value, found_frame, found_frame.identifier.value, len(found_frame), len(data)
    if len(found_frame) != len(data):
        return None

    found_frame = copy(found_frame)
    found_frame.symbols = data[1:]
    
    return found_frame

class frame_decoder:
    def __init__(self):
        self.frames = generate()
        self.identifiers = generateIdentifiers()
        self.symbols = generateSymbols()

    def decode(self,data):
        """;)"""
        
        new_frames = []
        
        new_data = []

        count = -1
        
        for d in data:
            
            #check to see if we've got an identifier
            if d.value < 0:
                new_frames.append([]) #add a new buffer
                count +=1 #increment the index to the frame buffer
            else: #if it's not an identifier
                if count >= 0: #and we've already got a frame index
                    new_frames[count].append(d) #append it to the frame buffer
        
        #for all of our new frame

        try:
            new_frames.remove([])
        except ValueError:
            pass #if it's not present
            
        #print len(new_frames)
        #ofor i in new_frames: print i
        
        matched_frames = [match_frame(frame,self.frames) for frame in new_frames]
        
        matched_frames = [i for i in matched_frames if i is not None]
        
        new_data = []
        
        #decompose the data

        [new_data.extend(i.decompose()) for i in matched_frames]
        
        #for frame in new_frames:

            #see if it matches any of our current frames
        #new_data = match_frame(frame,self.frames)
        #    pdb.set_trace()
        #    if new_data is not None:
        #        new_data.extend(d)

        return new_data

if __name__ == '__main__':
    import unittest, pdb, random
    
    class FrameDecoderTests(unittest.TestCase):
        def setUp(self):
            self.frames = generate()
            self.symbols = generateSymbols()

        def testOne(self):
            frame_decoder = FrameDecoder()
            
            
            #check the result of a good frame
            test = [symbol(i) for i in [-1,0,5]]
            t = frame_decoder.decode(test)

            self.failUnlessEqual(t[0].value,5)
            self.failUnlessEqual(t[0].name,'toolstatus')
            
            #check the result of another good frame
            test = [symbol(i) for i in [-1,1,4,5]]
            t = frame_decoder.decode(test)

            self.failUnlessEqual(t[0].value,405)
            self.failUnlessEqual(t[0].name,'azimuth')
            
            try:
                test = [symbol(i) for i in [-1,1,5]]
                t = frame_decoder.decode(test)
                self.fail()
            except Exception:
                pass
            
    fd = frame_decoder()
