# ZTIME CLI

import xml.etree.ElementTree as ET
import sys
import datetime as dt
from dateutil.parser import *
import time
import os
import math

from PIL import Image, ImageDraw, ImageFont

from colorama import Fore, Style
import colorsys

def unix_time(string):
	return int(time.mktime(parse(string).timetuple()))

def sunix_time(string):
	return str(unix_time(string))

log_string = ""
def log(*strings):
	global log_string
	print(*strings)
	for string in strings:
		log_string += string.replace(Fore.BLUE, "").replace(Fore.BLACK, "").replace(Fore.CYAN, "").replace(Fore.GREEN, "").replace(Fore.MAGENTA, "").replace(Fore.RED, "").replace(Fore.YELLOW, "").replace(Fore.WHITE, "").replace(Style.BRIGHT, "").replace(Style.DIM, "").replace(Style.NORMAL, "").replace(Style.RESET_ALL, "") + " "
	log_string += "\n"

def instructions():
	log("Time taking tool. ")
	log("\nPossible commands:")
	log("draw".rjust(10), f"| {Fore.BLUE}begin {Style.DIM}end {Fore.WHITE}width {Fore.GREEN}filters...{Style.RESET_ALL}")
	log("enter".rjust(10), f"| {Fore.GREEN}type {Fore.BLUE}begin end{Style.RESET_ALL}".ljust(32+3*5), f"{Style.DIM}alias: add{Style.RESET_ALL}")
	log("type".rjust(10), f"| {Fore.GREEN}type {Fore.RED}color{Style.RESET_ALL}")
	log("remove".rjust(10), f"| {Fore.YELLOW}id{Style.RESET_ALL}")
	log("modify".rjust(10), f"| {Fore.YELLOW}id {Fore.WHITE}[t|b|e] [{Fore.GREEN}type{Fore.WHITE}|{Fore.BLUE}begin{Fore.WHITE}|{Fore.BLUE}end{Fore.WHITE}]{Style.RESET_ALL}".ljust(32+9*5), f"{Style.DIM}alias: edit{Style.RESET_ALL}")
	log("list".rjust(10), f"| {Fore.YELLOW}{Style.DIM}start end {Fore.GREEN}filter{Style.RESET_ALL}")
	log("start".rjust(10), f"| {Fore.GREEN}type{Style.RESET_ALL}".ljust(32+2*5), f"{Style.DIM}alias: begin{Style.RESET_ALL}")
	log("types".rjust(10), "| ")
	log("running".rjust(10), "| ")
	log("stat".rjust(10), f"| {Fore.GREEN}type {Fore.BLUE}begin end{Style.RESET_ALL}")

def ztime_main(argv, doc_path):
	global log_string
	log_string = ""
	if len(argv) <= 1:
		instructions()
		return log_string
	
	# Create time.xml document if it doesn't exist
	if not os.path.isfile(doc_path):
		log(f"Couldn't find \"{doc_path}\", creating file.")
		tree = ET.fromstring("<data><types></types><entries></entries><current></current></data>")
		tree.write(doc_path)

	if argv[1] == "draw":
		if len(argv) < 3:
			log("Usage: draw 'begin' [end] [filters..]")
			return log_string
		draw(argv, doc_path)
	elif argv[1] == "enter" or argv[1] == "add":
		if len(argv) < 4:
			log("Usage: enter 'type' 'begin' [end]")
			return log_string

		tree = ET.parse(doc_path)
		entries = tree.getroot().find("entries")
		end = sunix_time(argv[4]) if len(argv) > 4 else str(int(time.mktime(dt.datetime.now().timetuple())))
		entry = ET.SubElement(entries, argv[2])
		entry.attrib.update(id=entries.attrib.get("next_id"), begin=sunix_time(argv[3]), end=end)
		entries.attrib.update(next_id=str(int(entries.attrib.get("next_id"))+1))
		tree.write(doc_path)
		log("Entered", argv[2], "(", entry.attrib.get("id"), ")")
	elif argv[1] == "type":
		if len(argv) < 4:
			log("Usage: type 'type' 'hex color'")
			return log_string

		tree = ET.parse(doc_path)
		types = tree.getroot().find("types")
		type = types.find(argv[2])
		action = "Modified type"
		if type == None:
			type = ET.SubElement(types, argv[2])
			action = "Added type"
		type.attrib.update(color=argv[3])
		tree.write(doc_path)
		log(action, argv[2], argv[3])
	elif argv[1] == "remove":
		if len(argv) < 3:
			log("Usage: remove 'id'")
			return log_string

		tree = ET.parse(doc_path)
		entries = tree.getroot().find("entries")

		entry = entries.find(".//*[@id='"+argv[2]+"']")
		name = entry.tag

		entries.remove(entry)
		tree.write(doc_path)
		log("Removed", name, "(", argv[2], ")")
	elif argv[1] == "modify" or argv[1] == "edit":
		if len(argv) < 5:
			log("Usage: modify 'id' '[t|b|e]' '[type|begin|end]'")
			return log_string

		tree = ET.parse(doc_path)
		entries = tree.getroot().find("entries")

		entry = entries.find(".//*[@id='"+argv[2]+"']")
		if argv[3] == 't':
			entry.tag = argv[4]
			log("(", entry.attrib.get("id"), ") type is now", argv[4])
		if argv[3] == 'b':
			entry.attrib.update(begin=sunix_time(argv[4]))
			log("(", entry.attrib.get("id"), ") begin is now is now", dt.datetime.fromtimestamp(int(entry.attrib.get("begin"))).strftime("%m/%d/%y %I:%M %p"))
		if argv[3] == 'e':
			entry.attrib.update(end=sunix_time(argv[4]))
			log("(", entry.attrib.get("id"), ") end is now is now", dt.datetime.fromtimestamp(int(entry.attrib.get("end"))).strftime("%m/%d/%y %I:%M %p"))
		tree.write(doc_path)
		log("Modified", entry.tag, "'s", "(", entry.attrib.get("id"), ")")
	elif argv[1] == "list":
		output = "TIME ENTRIES\n~~~~~~~~~~~~\n\n"

		low = int(argv[2]) if len(argv)>2 else 0
		high = int(argv[3]) if len(argv)>3 else 10000000

		tree = ET.parse(doc_path)
		entries = tree.getroot().find("entries")

		columns = os.get_terminal_size().columns
		tag_plus_id_width = columns - 38
		id_width = len(entries.attrib.get("next_id"))
		tag_width = tag_plus_id_width - 4 - id_width

		for entry in entries:
			id = int(entry.attrib.get("id"))
			if id >= low and id < high and ((entry.tag == argv[4]) if len(argv) > 4 else True):
				output += entry.tag.ljust(tag_width)
				output += (" ({:"+str(id_width)+"d}) ").format(id)
				output += dt.datetime.fromtimestamp(int(entry.attrib.get("begin"))).strftime("%m/%d/%y %I:%M %p")
				output += " - "
				output += dt.datetime.fromtimestamp(int(entry.attrib.get("end"))).strftime("%m/%d/%y %I:%M %p")
				output += "\n"
		log(output)
	elif argv[1] == "start" or argv[1] == "begin":
		if len(argv) < 3:
			log("Usage: start 'type'")
		type = argv[2]
		tree = ET.parse(doc_path)
		current = tree.getroot().find("current")
		for running in current:
			if running.tag == type:
				log(type, "already running!")
				return log_string
		ET.SubElement(current, type, {"begin": sunix_time(argv[3]) if len(argv) > 3 else str(int(time.mktime(dt.datetime.now().timetuple())))})
		tree.write(doc_path)
		log("Started", type)
	elif argv[1] == "stop" or argv[1] == "end":
		if len(argv) < 3:
			log("Usage: stop 'type'")
		type = argv[2]
		tree = ET.parse(doc_path)
		current = tree.getroot().find("current")
		for running in current:
			if running.tag == type:
				entries = tree.getroot().find("entries")

				entry = ET.SubElement(entries, type)
				entry.attrib.update(id=entries.attrib.get("next_id"), begin=running.attrib["begin"], end=sunix_time(argv[3]) if len(argv) > 3 else str(int(time.mktime(dt.datetime.now().timetuple()))))
				entries.attrib.update(next_id=str(int(entries.attrib.get("next_id"))+1))

				current.remove(running)
				tree.write(doc_path)
				log("Entered", type, "(", entry.attrib.get("id"), ")")
				return log_string
		log("Couldn't find", type)
	elif argv[1] == "types":

		tree = ET.parse(doc_path)
		types = tree.getroot().find("types")
		max_len = 5
		for type in types:
			if len(type.tag) > max_len:
				max_len = len(type.tag)
		for type in types:
			log(type.tag.rjust(max_len+2), "|", type.attrib["color"])
	elif argv[1] == "running":

		tree = ET.parse(doc_path)
		running = tree.getroot().find("current")
		max_len = 5
		for run in running:
			if len(run.tag) > max_len:
				max_len = len(run.tag)
		for run in running:
			log(run.tag.rjust(max_len+2), "|", dt.datetime.fromtimestamp(int(run.attrib.get("begin"))).strftime("%m/%d/%y %I:%M %p"))
	elif argv[1] == "stat":
		if len(argv) < 4:
			log("Usage: stat 'type' 'begin' [end]")
			return log_string
		stat(argv, doc_path)
	else:
		instructions()
	return log_string

def intersect(a_begin, a_end, b_begin, b_end):
	return int(a_end) > int(b_begin) and int(a_begin) < int(b_end)

def stat(argv, doc_path):
	tree = ET.parse(doc_path)
	entries = tree.getroot().find("entries")
	type = argv[2]
	begin = unix_time(argv[3])
	end = unix_time(argv[4]) if len(argv) > 4 else int(time.mktime(dt.datetime.now().timetuple()))

	time_spent = 0
	for entry in entries:
		if entry.tag==type and intersect(entry.attrib["begin"], entry.attrib["end"], begin, end):
			time_spent += min(end, int(entry.attrib["end"])) - max(begin, int(entry.attrib["begin"]))

	def time_length_string(time):
		time_string = str(int(time) % 60) + " seconds"
		if time > 60:
			time_string = str(int(time / 60) % 60) + " minutes, " + time_string
		if time > 3600:
			time_string = str(int(time / 3600) % 24) + " hours, " + time_string
		if time > 86400:
			time_string = str(int(time / 86400)) + " days, " + time_string
		return time_string

	log("Statistics on", type)
	log("~~~~~~~~~~~~~~"+"~"*len(type))
	log("-", str(int(time_spent)), "seconds")
	if time_spent > 60:
		log("-", str(int(time_spent/6)/10), "minutes")
	if time_spent > 3600:
		log("-", str(int(time_spent/360)/10), "hours")
	if time_spent > 86400:
		log("-", str(int(time_spent/864)/100), "days")
	log("Or,", time_length_string(time_spent))
	log("~~~~~~~~~~~~~~"+"~"*len(type))
	if end-begin > 86400*2:
		log(time_length_string(time_spent / ((end-begin)/86400)), "per day")
	if end-begin > 86400*14:
		log(time_length_string(time_spent / ((end-begin)/604800)), "per week")

def draw(argv, doc_path):
	tree = ET.parse(doc_path)
	entries = tree.getroot().find("entries")
	included_entries = []

	low = unix_time(argv[2])
	high = unix_time(argv[3]) if len(argv) > 3 else int(time.mktime(dt.datetime.now().timetuple()))

	widthProvided = len(argv) > 4 and argv[4].isnumeric()
	width = int(argv[4]) if widthProvided else 3600
	height = 120

	filterStart = 5 if widthProvided else 4
	filter = len(argv) > filterStart

	def get_x(timestamp):
		return width * (int(timestamp) - low) / (high - low)

	for entry in entries:
		matchesFilter = not filter
		if filter:
			for f in range(filterStart, len(argv)):
				if argv[f] == entry.tag:
					matchesFilter = True
		if intersect(low, high, entry.attrib["begin"], entry.attrib["end"]) and matchesFilter:
			level = 0
			i = 0
			while i < len(included_entries):
				included_entry = included_entries[i]
				if intersect(entry.attrib["begin"], entry.attrib["end"], included_entry["xml"].attrib["begin"], included_entry["xml"].attrib["end"]) and included_entry["level"] == level:
					level += 1
					i = 0
				else:
					i += 1
			if height < level * 120 + 120:
				height = level * 120 + 120
			included_entries.append({"xml": entry, "level": level})

	image = Image.new("RGB", (width, height), "#ffffff")
	draw = ImageDraw.Draw(image)

	palette = {}
	types = tree.getroot().find("types")
	for type in types:
		palette.update({type.tag: type.attrib["color"]})

	def inverse(hex):
		rev = {"0": "f", "1": "e", "2": "d", "3": "c", "4": "b", "5": "a", "6": "9", "7": "8", "8": "7", "9": "6", "a": "5", "b": "4", "c": "3", "d": "2", "e": "1", "f": "0"}
		out = "#"
		for i in range(1, len(hex)):
			out += rev[hex[i]]

		r = int("0x" + hex[1] + hex[2], 16)
		g = int("0x" + hex[3] + hex[4], 16)
		b = int("0x" + hex[5] + hex[6], 16)
		(h, s, v) = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
		h += 0.25
		if h > 1:
			h -= 1
		#v = (1 - v)
		#v *= 0.8
		#s *= 1.1
		s = 1 - s
		v = 1 - v
		#s = max(s, 1)
		return f"hsv({h*360}, {s*100}%, {v*100}%)"

	deffont = ImageFont.truetype("basicbit3.ttf", 28)
	draw.font = deffont
	draw.fontmode = "L"

	hours_diff = math.ceil((high - low) / (60*60))
	if hours_diff < width / 50:
		begin = width * (low % (60 * 60)) / (high - low)
		for i in range(hours_diff):
			draw.rectangle((get_x(((low // (60 * 60))+i)*60*60),0,get_x(((low//(60*60))+i)*60*60)+1,height), fill="#000000")

	# draw.text()

	for include in included_entries:
		# print("Drawing", include, get_x(include["xml"].attrib["begin"]), get_x(include["xml"].attrib["end"])-get_x(include["xml"].attrib["begin"]))
		color = palette[include["xml"].tag] if include["xml"].tag in palette else "#ffffff"
		begin = int(include["xml"].attrib["begin"])
		end = int(include["xml"].attrib["end"])
		level = include["level"]*120
		
		if end < begin:
			log(f"Can't draw element <{include['xml'].tag} id={include['xml'].attrib['id']}> because begin is {dt.datetime.fromtimestamp(begin).strftime('%m/%d/%y %I:%M %p')} while end is {dt.datetime.fromtimestamp(end).strftime('%m/%d/%y %I:%M %p')}")
			continue

		string_a = dt.datetime.fromtimestamp(begin).strftime("%I:%M %p")
		string_b = include["xml"].tag
		string_c = dt.datetime.fromtimestamp(end).strftime("%I:%M %p")

		draw.rectangle((get_x(begin), level, get_x(end), level+120), fill=color)
		
		max_width = max(deffont.getlength(string_a), deffont.getlength(string_b), deffont.getlength(string_c))
		fnt = ImageFont.truetype("basicbit3.ttf", 28 if max_width < get_x(end)-get_x(begin) else int(28*((get_x(end)-get_x(begin))/max_width)))
		draw.font = fnt
		draw.text((get_x(begin), level+8), string_a, fill=inverse(color), font=fnt)
		draw.text(((get_x(begin)+get_x(end)-fnt.getlength(string_b))/2, level+(120-fnt.size)/2), string_b, align="center", fill=inverse(color), font=fnt)
		draw.text((get_x(end)-fnt.getlength(string_c), level+120-fnt.size-6), string_c, fill=inverse(color), font=fnt)
	image.save("time.png")

if __name__ == "__main__":
	ztime_main(sys.argv, "time.xml")
