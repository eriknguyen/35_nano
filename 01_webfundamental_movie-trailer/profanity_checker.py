from urllib import request

def read_text():
	quotes = open('/Users/eriknguyen/workspace/35_nano/01_movie-trailer/movie_quotes.txt')
	content = quotes.read()
	print(content)
	quotes.close()
	check_profanity(content)


def check_profanity(text_to_check):
	connection = request.urlopen('http://wdyl.com/profanity?q=' + text_to_check)
	# connection = request.urlopen('http://google.com.sg')
	output = connection.read()
	# print(output)
	connection.close()
	if 'true' in output:
		print("Profanity alert!!!")
	elif 'false' in output:
		print('No curse word!')
	else:
		print('Could not scan document')


read_text()