import subprocess



def search(text):
	result = subprocess.run(['searchsploit', '--cve', '-j', text], stdout=subprocess.PIPE).stdout.decode('utf-8')
	return result