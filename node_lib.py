from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy
from scipy import misc

# node graph
class graph(dict):
    def __init__(self, *args, **kwds):
        super(graph, self).__init__(*args, **kwds)
        self.__dict__ = self

# node composite
def composite_(cached_a,cached_b,mask,job):
    if (job=='mask'):
        aCom = Image.fromarray(cached_a)
        bCom = Image.fromarray(cached_b)
        iMask = Image.fromarray(mask)
        out = numpy.array(Image.composite(aCom, bCom, iMask))
    if (job=='plus'):
        out=cached_a+cached_b
    if (job=='minus'):
        out=cached_a-cached_b
    if (job=='multiply'):
        out=cached_a*cached_b
    print '->Composite',job
    return out;

# node size
def size_(cached,size,w,h):
    if (size>0):
        S= int(round(h*size)), int(round(w*size))
        out=misc.imresize(cached,S,'bilinear','RGB')
    if (size<0):
        S= int(round(h/abs(size))),int(round(w/abs(size)))
        out=misc.imresize(cached,S,'bilinear','RGB')
    print '->Size',S
    return out;

# node Color Correct (CC)
def CC_(cached,bright,contrast):
    out_cc = Image.fromarray(cached)
    enhancer = ImageEnhance.Brightness(out_cc) # Brightness
    out_cc = enhancer.enhance(bright)
    enhancer = ImageEnhance.Contrast(out_cc) # Contrast
    out = numpy.array(enhancer.enhance(contrast))
    print '->Color correct: bright=',bright,' contrast=',contrast
    return out;

# node rotate
def rotate_(cached,angle):
    out=misc.imrotate(cached,angle,'bilinear')
    print '->Rotate',angle
    return out;

# node blur
def blur_(cached,size):
    out=cached
    for k in range(size):
        out=misc.imfilter(out,'blur')
        print '.',
    print '->Blur',size
    return out;

# node sharpen
def sharpen_(cached,size):
    out=cached
    for k in range(size):
        out=misc.imfilter(out,'sharpen')
        print '.',
    print '->Sharpen',size
    return out;

# node gradient
def gradient_(width,height):
    im = Image.new("L", (1, height))
    draw = ImageDraw.Draw(im)
    for l in xrange(height):
        G=255 * l/height
        colour = (G)
        draw.line((0, l, height, l), fill=colour)
    im=im.resize((width, height), Image.NEAREST)
    out = numpy.array(im)
    del draw
    print '->Gradient: width=',width,' height=',height
    return out;

