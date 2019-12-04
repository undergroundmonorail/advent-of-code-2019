def all_nums():
	def has_rep(s):
		for n, i in enumerate(s[:-1]):
			if i == s[n+1]:
				return True
		return False

	for a in range(10):
		for b in range(a, 10):
			for c in range(b, 10):
				for d in range(c, 10):
					for e in range(d, 10):
						for f in range(e, 10):
							n = '{}{}{}{}{}{}'.format(a, b, c, d, e, f)
							if has_rep(n):
								yield int(n)
							
print(sum((1 for i in all_nums() if 353096 < i < 843212)))
