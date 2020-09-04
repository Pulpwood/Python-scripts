# Write a program that scans through your email account, finds all the 
# unsubscribe links in all your emails, and automatically opens them 
# in a browser.
# This program will have to log in to your email provider’s IMAP server
# and download all of your emails. You can use BeautifulSoup (covered in
# Chapter 11) to check for any instance where the word unsubscribe occurs
# within an HTML link tag.
# Once you have a list of these URLs, you can use webbrowser.open() to
# automatically open all of these links in a browser.
# You’ll still have to manually go through and complete any additional
# steps to unsubscribe yourself from these lists. In most cases, this involves
# clicking a link to confirm.
# But this script saves you from having to go through all of your emails
# looking for unsubscribe links. You can then pass this script along to your
# friends so they can run it on their email accounts. (Just make sure your
# email password isn’t hardcoded in the source code!)

import imapclient, pyzmail, webbrowser
import bs4
from bs4 import BeautifulSoup

def unsubscribe_links(imap_address, e_mail, password):
	mail_un_links = set()

	try:
		with imapclient.IMAPClient(imap_address, ssl=True) as imap:
			imap.login(e_mail, password)
			print('Log in successful.')
			# print(imap.list_folders())
			imap.select_folder('INBOX', readonly=True)

			UIDs = imap.search('ALL')

			for i in UIDs:
				raw_messages = imap.fetch([i],[b'BODY[]', 'FLAGS'])
				messages = pyzmail.PyzMessage.factory(raw_messages[i][b'BODY[]'])
				# print(messages)

				if messages.html_part:
					html_form = messages.html_part.get_payload().decode(messages.html_part.charset)
					soup = bs4.BeautifulSoup(html_form, 'html.parser')
					links_elem = soup.find_all('a')

					
					for link in links_elem:
						if 'unsubscribe' in link.text.lower():
							unsubscribe_link = link.get('href')
							mail_un_links.add(unsubscribe_link)
			try:		
				for unsubscribe_link in mail_un_links:
					print('opening ' + str(unsubscribe_link))
					webbrowser.open(unsubscribe_link)
			except:
					print('No unsubscribe links found.')
	except:
		print('Log in unsuccessful.')

if __name__ == '__main__':
	message = """
	'This script openes links which allow you to unsubscribe 
	followed newsletters etc. In some cases you may need allow
	access to low secure apps. Some links will automatically 
	unsubscribe your subscribtions. Be carefull.'
	
	When you log in, links for unsubscription will appear in 
	web explorer. You need to go through them manually.
	In most cases, this involves clicking a link to confirm. 
	However some links will unsubscribe automatically.
	"""
	print(message)	
	e_mail = input('Enter your email: ')
	password = input('Enter your password: ')

	unsubscribe_links('imap.gmail.com', e_mail, password)
