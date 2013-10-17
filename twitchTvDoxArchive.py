import web
from web.wsgiserver import CherryPyWSGIServer
import glob
import os
import pwd
import grp
import cgi
from recaptcha.client import captcha


urls = ('/', 'index',
'/doxing/(.*)', 'display',
'/doxing', 'doxing',
'/post', 'post')


app = web.application(urls, globals())

render = web.template.render('templates/')

web.config.debug = False

class index:
	def GET(self):
		web.header('Content-Type','text/html; charset=utf-8', unique=True) 
		return web.redirect('./doxing')

class doxing:
	def GET(self):
		web.header('Content-Type','text/html; charset=utf-8', unique=True) 
		doxes = []
		newDoxes = []
		
		for txt in glob.glob('dox/*.txt'):
			doxes.append(txt.replace('dox/', ''))
		
		for dox in doxes:
			dox = "<a href='./doxing/%s'>%s</a><br />" % (dox.replace('.txt', ''), dox.replace('.txt', ''))
			newDoxes.append(dox)

		return render.index('doxing.tv', str(newDoxes).replace('[\"', '').replace('\"]', '').replace('\"', '').replace(', ', ''), './post')

class display:
	def GET(self, username):
		print(web.ctx.env.get("HTTP_CF_CONNECTING_IP", '127.0.0.1'))
		web.header('Content-Type','text/html; charset=utf-8', unique=True) 
		import cgi
		dox = cgi.escape(open('dox/%s.txt' % username, 'r').read().strip(), True)
		dox = '&#x0a;'.join(filter(None, dox.split('\n'))).replace('\r', '')
		return '<!DOCTYPE html><html><title>%s</title><body bgcolor="#444448" link="#ADB389" vlink="#ADB389"><br\><pre><font color="#989CF1">%s</font></pre><br /><br /> <a href="../doxing">Back to archive</a></body></html>' % (username, dox.decode('utf-8'))


class post:
	def GET(self):
		web.header('Content-Type','text/html; charset=utf-8', unique=True) 
		return render.post('doxing.tv')

	def POST(self):

		web.header('Content-Type','text/html; charset=utf-8', unique=True) 
		postData = web.input()

		response = captcha.submit(
        postData['recaptcha_challenge_field'],
        postData['recaptcha_response_field'],
        'captchaPrivKey',
        web.ctx['ip'])
		
		if not response.is_valid:
			return render.posted('doxing.tv', 'Captcha Invalid.', 'leluraretardufuck')
		else:
			dox = postData['dox']
			doxee = postData['username']
			if doxee.rstrip() != '':
				if os.path.isfile('dox/%s.txt' % doxee.rstrip()):
					return render.posted('doxing.tv', 'Dox exists.', doxee)
				openFile = open('dox/%s.txt' % doxee.rstrip(), 'w')
				openFile.write(dox.encode('utf-8'))
				openFile.close()
			else:
				return render.posted('doxing.tv', 'You are a fucking faggot that forgot the username.', doxee)
			return render.posted('doxing.tv', 'Dox posted.', doxee)

		



if __name__ == "__main__":
	app.run()

