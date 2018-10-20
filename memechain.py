import time, json, urllib2, os, random

from sightengine.client import SightengineClient


class MemeChain():
	def __init__(self):
		self.api_root = "http://95.179.132.93:1337/api"

	def getJSON(self, url):
		return json.loads(urllib2.urlopen(urllib2.Request(url), timeout=30).read())

	def get_last_5_memes(self):
		memechain_height = self.getJSON("%s/getheight" % self.api_root)['result']
		response = []

		if memechain_height > 5:
			for meme in range(memechain_height - 4, memechain_height + 1)[::-1]:
				rawdata_meme = self.getJSON("%s/getmemedatabyheight/%s" % (self.api_root, str(meme)))['result']
				response.append(dict(rawdata_meme, **{'meme_height' : meme}))
		else:
			for meme in range(1, memechain_height + 1)[::-1]:
				rawdata_meme = self.getJSON("%s/getmemedatabyheight/%s" % (self.api_root, str(meme)))['result']
				response.append(dict(rawdata_meme, **{'meme_height' : meme}))

		return response

	def get_meme(self, height):
		rawdata_meme = self.getJSON("%s/getmemedatabyheight/%s" % (self.api_root, str(height)))

		sightclient = SightengineClient("1347331372", "BhoFasNuF3zAGp8XSRXi")
		output = sightclient.check('nudity').set_url('https://ipfs.io/ipfs/%s' % rawdata_meme['result']['ipfs_id'])

		try:
			if output['nudity']['safe'] > 0.5:
				if rawdata_meme:
					return dict(rawdata_meme, **{'meme_height' : meme})
				else:
					return None
			else:
				return None

		except KeyError as e:
			if rawdata_meme:
				return dict(rawdata_meme, **{'meme_height' : meme})
			else:
				return None
			

