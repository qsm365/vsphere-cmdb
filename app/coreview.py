# -*- coding:utf-8 -*-

from flask import request,Blueprint,render_template,session,redirect,url_for,send_file
#import cStringIO, string, os, random, io
#from PIL import Image, ImageDraw, ImageFont
from . import app

coreprofile = Blueprint('coreprofile', __name__)

@app.route('/logout',methods = ['GET','POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        #if request.form['imagecode'].lower()!=session['captcha']:
            #return render_template('login.html',imagecode_is_wrong=True)
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            return render_template('login.html',password_is_wrong=True)
        session['username']='test'
        return redirect(url_for('vsphere_host_list'))
    else:
        return render_template('login.html')

'''
@app.route('/captcha',methods = ['GET'])
def captcha():
    image = Image.new('RGB', (128, 49), color = (255, 255, 255))
    # model, size, background color
    font_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'arial.ttf')
    # choose a font file
    font = ImageFont.truetype(font_file, 39)
    # the font object
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.letters + string.digits, 4))
    # The random string
    j=0
    for i in rand_str:
        draw.text((7+28*j, 1), i, fill=(random.randint(0,200), random.randint(0,200), random.randint(0,200)), font=font)
        j=j+1
    # position, content, color, font
    del draw
    session['captcha'] =rand_str.lower()
    # store the content in Django's session store
    buf = cStringIO.StringIO()
    # a memory buffer used to store the generated image
    image.save(buf, 'gif')
    return send_file(io.BytesIO(buf.getvalue()))
    # return the image data stream as image/jpeg format, browser will treat it as an image
'''

@app.template_filter('average')
def average_filter(s):
    if len(s) > 0:
        return round(sum(s) / float(len(s)), 2)
    else:
        return 0


@app.template_filter('max')
def max_filter(s):
    if s:
        return max(s)
    else:
        return 0

@app.template_filter('notnone')
def notnone_filter(s):
    if s:
        return s
    else:
        return '-'