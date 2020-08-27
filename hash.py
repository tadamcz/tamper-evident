import hashlib
import json
import datetime
import time

with open("fake_twitter_for_testing.json","r") as f:
	header_chain = json.loads(f.read())

def myhash(object):
	if type(object) != str and type(object) != dict:
		raise TypeError("Must be string or dict")

	if type(object) == dict:
		object = json.dumps(object, sort_keys=True)	#https://stackoverflow.com/a/22003440/8010877

	utf_8_representation = object.encode('utf-8')
	hash_object = hashlib.sha256(utf_8_representation)
	digest = hash_object.hexdigest()
	return digest

def append_header(header_chain,string_to_add,username,do_hasing=False):
	if do_hasing:
		new_message = myhash(string_to_add)
	else:
		new_message = string_to_add

	if len(header_chain) > 0:
		hash_of_previous_header = myhash(header_chain[-1])
	else:
		hash_of_previous_header = None
	date = datetime.datetime.timestamp(datetime.datetime.now())

	#  each header contains the date, the hash of the new file, and the the hash of the previous header.
	# might not need the date, think more about this
	header = {'date_posix': date,
			  'new_message': new_message,
			  'hash_of_previous_header': hash_of_previous_header,
			  'username': username}
	header_chain.append(header)
	return header_chain

def bad_actor(header_chain,n):
	modified = myhash('I have hacked into the mainframe')
	header_chain[n]['hash_of_new_file'] = modified

def check_integrity_of_chain(header_chain,upto_index_inclusive):
	for i in range(upto_index_inclusive+1):
		header = header_chain[i]
		print("")
		print('index',i,'header with date',header['date_posix'])
		if i == 0:
			print("First header, nothing to check")
		else:
			previous_header = header_chain[i-1]
			if myhash(previous_header) == header['hash_of_previous_header']:
				print("Chain valid up to here")
			else:
				raise AssertionError("Chain not valid from here onwards")

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

with open("fake_twitter_for_testing.json","w") as f:
	f.write(json.dumps(header_chain))

