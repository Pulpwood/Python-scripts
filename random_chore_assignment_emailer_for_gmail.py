#!python3
#Script sends randomly duty mails to people's mail in the variable 'people'

def duty_send(mail, password):
	import random, smtplib, sys, re
	from email.message import EmailMessage
	people = ['michael@example.com', 'john@example.com', 'kitka@example.com',
	'kajtek@example.com']
	chores = ['dishes', 'bathroom', 'vacuum', 'walking dog']
	duties_for_people = {}


	for random_chore in range(0,4):
		random_chore = random.choice(chores)
		chores.remove(random_chore)
		random_person = random.choice(people)
		people.remove(random_person)
		duties_for_people[random_person] = random_chore
		
		with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
			smtp.ehlo()
			smtp.starttls()
			try:
				smtp.login(mail, password)
			except:
				print('Authorization unsuccessful. Enter valid data.')
				sys.exit()


			msg = EmailMessage()
			msg['Subject'] = 'Duties for following week.'
			msg['From'] = mail
			msg['To'] = random_person
			print('Sending mail to ' + random_person)
			msg.set_content('Your duty for following weekend is ' + random_chore + '.')
			smtp.send_message(msg)

if __name__ == '__main__':
	message1 = 'Program sends mails with random duty to random person'
	print(message1)
	mail = input('Insert your mail: ')
	password = input('Insert your password: ')
	duty_send(mail, password)
