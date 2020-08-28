import hashlib
import json
import datetime

def myhash(object):
	if type(object) != str and type(object) != dict:
		raise TypeError("Must be string or dict")

	if type(object) == dict:
		object = json.dumps(object, sort_keys=True)	#https://stackoverflow.com/a/22003440/8010877

	utf_8_representation = object.encode('utf-8')
	hash_object = hashlib.sha256(utf_8_representation)
	digest = hash_object.hexdigest()
	return digest

def get_from_twitter():
	try:
		with open("fake_twitter_for_testing.json", "r") as f:
			content = f.read()
			if len(content)>0:
				header_chain = json.loads(content)
			else:
				header_chain = []
	except FileNotFoundError:
		header_chain = []
	return header_chain

def append_header(string_to_add,username,do_hashing=False):
	header_chain = get_from_twitter()

	if do_hashing:
		new_message = myhash(string_to_add)
	else:
		new_message = string_to_add

	if len(header_chain) > 0:
		hash_of_previous_header = myhash(header_chain[-1])
	else:
		hash_of_previous_header = None
	date = datetime.datetime.timestamp(datetime.datetime.now())

	#  each header contains the date, the hash of the new file, and the the hash of the previous header.
	header = { 'message': new_message,
			  'hash_of_previous_header': hash_of_previous_header,
			  'username': username}
	header_chain.append(header)

	with open("fake_twitter_for_testing.json", "w") as f:
		f.write(json.dumps(header_chain))
	return header_chain

def bad_actor(header_chain,n):
	modified = myhash('I have hacked into the mainframe')
	header_chain[n]['hash_of_new_file'] = modified

def check_integrity_of_chain(upto_index_inclusive=None):
	header_chain = get_from_twitter()
	if upto_index_inclusive is None:
		upto_index_inclusive = len(header_chain)-1

	stringout = ''
	for i in range(upto_index_inclusive+1):
		header = header_chain[i]
		stringout += '\n'
		stringout += 'index '+str(i)+' header'+'\n'
		if i == 0:
			stringout+= "First header, nothing to check"+'\n'
		else:
			previous_header = header_chain[i-1]
			if myhash(previous_header) == header['hash_of_previous_header']:
				stringout += "Chain valid up to here"+'\n'
			else:
				stringout+= "Chain not valid from here onwards"+'\n'
				break
	return stringout

def check_file_against_hash(header_chain,file,index):
	check_integrity_of_chain(header_chain,index)

	date = header_chain[index]['date_posix']
	print("")
	print("checking '"+file+"' against hash at index",index,"with date",date)
	hash_to_check = header_chain[index]['hash_of_new_file']
	if hash_to_check == myhash(file):
		print("OK, they match")
	else:
		raise AssertionError("They do not match")

def tweet_compactly(previous_hash,string_to_add,username,do_hasing=False):
	placeholder_previous_hash = 'placeholder for previous header hash'
	stringout = placeholder_previous_hash+'@'+username+'\n'+string_to_add
