def base_splitstring(src, sep):
	#// Empty string must not generate anything in vector
	if (len(src) == 0):
		return;

	first = 0;
	last = len(src);
	dest = []
	while(True):
		next = src.find(sep, first);
		if (next < 0):
			next = len(src)
		part = ""
		if (next > first):
			part = src[first: next]
			dest.append(part)

		first = next + 1;       #// + 1 to remove the separator
		if (first >= last):
			break

	return dest

def parsedoubles(s):

	try:
		values = base_splitstring(s, " ");
		res = []
		for i in range(0,len(values)):
			v = (float)(values[i])
			res.append(v)
		return res
	except:
		return []

