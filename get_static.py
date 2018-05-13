import json
from statistics import mean, stdev

def main():
	data = json.load(open('flaski/choice.json'))
	names = ['Chaturvedi', 'FDGIB', 'STGIB', 'TRGIB']
	list = [ [{ "answer": [], "time":[]} for i in range(4)] for j in range(4)]
	for datum in data:
		if datum['layout'] == 'Chatu':
			list[int(datum['task'])-1][0]['answer'].append(int(datum['answer']))
			list[int(datum['task'])-1][0]['time'].append(float(datum['time']))
		elif datum['layout'] == 'FDGIB':
			list[int(datum['task'])-1][1]['answer'].append(int(datum['answer']))
			list[int(datum['task'])-1][1]['time'].append(float(datum['time']))
		elif datum['layout'] == 'STGIB':
			list[int(datum['task'])-1][2]['answer'].append(int(datum['answer']))
			list[int(datum['task'])-1][2]['time'].append(float(datum['time']))
		elif datum['layout'] == 'TRGIB':
			list[int(datum['task'])-1][3]['answer'].append(int(datum['answer']))
			list[int(datum['task'])-1][3]['time'].append(float(datum['time']))
	outputs= [ [{} for i in range(4)] for j in range(4)]
	print(list)
	for task in range(4):
		for layout in range(4):
			print(list[task][layout])
			try:
				ans = mean(list[task][layout]['answer'])
				dev_ans = stdev(list[task][layout]['answer'])
				time = mean(list[task][layout]['time'])
				dev_time = stdev(list[task][layout]['time'])
				outputs[task][layout]['ans'] = ans
				outputs[task][layout]['dev_ans'] = dev_ans
				outputs[task][layout]['time'] = time
				outputs[task][layout]['dev_time'] = dev_time
				outputs[task][layout]['layout'] = names[layout]
			except:
				pass

	f = open('./flaski/statistics.json', 'w')
	json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

if __name__ == '__main__':
	main()
