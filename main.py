import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import tkmacosx as tkm
from PIL import Image, ImageTk
import os
import other.type_convertor as tc
from extras.dijkstra import Dijkstra


class Hex:
	"""
	Class for hex/decimal conversion
	"""
	hexnumerals = "0123456789abcdef"

	@staticmethod
	def to_hex(number):
		hexString = ""
		while number > 0:
			hexString = Hex.hexnumerals[int(number % 16)] + hexString
			number //= 16
		return hexString

	@staticmethod
	def to_dec(hexString):
		offset = 1
		total = 0
		for i in hexString[::-1]:
			total += offset * Hex.hexnumerals.index(i)
			offset *= 16
		return total

	@staticmethod
	def split_colour(colour):
		return Hex.to_dec(colour[1:3]), Hex.to_dec(colour[3:5]), Hex.to_dec(colour[5:7])

	@staticmethod
	def apply_contrast(colour1, colour2, contrast):
		result = "#"
		c1 = Hex.split_colour(colour1)
		c2 = Hex.split_colour(colour2)
		for i in range(3):
			result += Hex.to_hex(c1[i] * 1 - contrast + c2[i] * contrast)
		return result


class Window:
	def __init__(self, title: str, icon: str, main_win: bool):
		# set up the window
		if main_win:
			self._window = tk.Tk()
		else:
			self._window = tk.Toplevel()
		self._setup(title, icon)

	def _setup(self, title: str, icon: str):
		# colour scheme
		self._bg = "#000000"
		self._fg = "#ffffff"
		self._button_bg = Hex.apply_contrast(self._bg, self._fg, 0.2)
		self._button_fg = Hex.apply_contrast(self._fg, self._bg, 0.2)

		# setup window
		self._window.title(title)
		self._window.wm_iconphoto(True, tk.PhotoImage(file=icon))
		self._window.config(bg=self._bg)

		# fonts
		self._font = Font(
			family="Fixedsys Excelsior 3.01",
			size=32,
			weight="normal"
		)
		self._button_font = Font(
			family="Fixedsys Excelsior 3.01",
			size=20,
			weight="normal"
		)

		self.speaker = tk.Label(self._window, text="", bg=self._bg, fg=self._fg, font=self._font)
		self.question = tk.Label(self._window, text="", bg=self._bg, fg=self._fg, font=self._font)
		self._buttons = []
		self._spaces = []

	def make_button(self, text, command, colour: str):
		return tkm.Button(self._window, text=text, command=command, bg=self._button_bg, activebackground=self._button_bg, fg=colour, font=self._button_font)

	def start(self):
		self._window.focus_force()
		self._window.mainloop()


class GraphEditor:
	def __init__(self):
		self.places = [
			"Edinburgh", "London", "Brest", "Pamplona", "Barcelona", "Madrid", "Lisboa", "Cadiz", "Marseille", "Dieppe",
			"Bruxelles", "Paris", "Amsterdam", "Zurich", "Essen", "Kobenhavn", "Stockholm", "Frankfurt", "Munchen",
			"Venezia", "Roma", "Brindisi", "Palermo", "Zagrab", "Wien", "Berlin", "Danzic", "Riga", "Petrograd",
			"Warszawa", "Budapest", "Sarajevo", "Sofia", "Athina", "Smyrna", "Bucuresti", "Constantinople", "Angora",
			"Erzurum", "Sochi", "Sevastopol", "Rostov", "Kharkov", "Moskva", "Smolensk", "Wilno", "Kyiv"
		]
		self.distances = {
			("London", "Edinburgh"): 4,
			("London", "Amsterdam"): 2,
			("London", "Dieppe"): 2,
			("Lisboa", "Cadiz"): 2,
			("Stockholm", "Kobenhavn"): 3,
			("Stockholm", "Petrograd"): 8,
			("Brest", "Dieppe"): 2,
			("Pamplona", "Brest"): 4,
			("Pamplona", "Barcelona"): 2,
			("Pamplona", "Paris"): 4,
			("Pamplona", "Marseille"): 4,
			("Madrid", "Pamplona"): 3,
			("Madrid", "Lisboa"): 3,
			("Madrid", "Cadiz"): 3,
			("Madrid", "Barcelona"): 2,
			("Marseille", "Zurich"): 2,
			("Marseille", "Barcelona"): 4,
			("Marseille", "Paris"): 4,
			("Marseille", "Roma"): 4,
			("Bruxelles", "Dieppe"): 2,
			("Bruxelles", "Amsterdam"): 1,
			("Bruxelles", "Frankfurt"): 2,
			("Dieppe", "Paris"): 1,
			("Paris", "Zurich"): 3,
			("Paris", "Frankfurt"): 3,
			("Paris", "Brest"): 3,
			("Paris", "Bruxelles"): 2,
			("Zurich", "Munchen"): 2,
			("Zurich", "Venezia"): 2,
			("Essen", "Frankfurt"): 2,
			("Essen", "Berlin"): 2,
			("Essen", "Kobenhavn"): 3,
			("Essen", "Amsterdam"): 3,
			("Frankfurt", "Munchen"): 2,
			("Frankfurt", "Amsterdam"): 2,
			("Frankfurt", "Berlin"): 3,
			("Munchen", "Venezia"): 2,
			("Munchen", "Wien"): 3,
			("Venezia", "Roma"): 2,
			("Venezia", "Zagrab"): 2,
			("Roma", "Brindisi"): 2,
			("Roma", "Palermo"): 4,
			("Brindisi", "Palermo"): 3,
			("Brindisi", "Athina"): 4,
			("Zagrab", "Wien"): 2,
			("Zacrab", "Budapest"): 2,
			("Zacrab", "Sarajevo"): 3,
			("Wien", "Budapest"): 1,
			("Wien", "Berlin"): 3,
			("Wien", "Warszawa"): 4,
			("Berlin", "Danzic"): 4,
			("Danzic", "Warszawa"): 2,
			("Danzic", "Riga"): 3,
			("Riga", "Wilno"): 4,
			("Riga", "Petrograd"): 4,
			("Petrograd", "Wilno"): 4,
			("Petrograd", "Moskva"): 4,
			("Warszawa", "Wilno"): 3,
			("Warszawa", "Berlin"): 4,
			("Warszawa", "Kyiv"): 4,
			("Bucuresti", "Budapest"): 4,
			("Sarajevo", "Sofia"): 2,
			("Sarajevo", "Athina"): 4,
			("Sarajevo", "Budapest"): 3,
			("Sofia", "Bucuresti"): 2,
			("Sofia", "Athina"): 3,
			("Sofia", "Constantinople"): 3,
			("Smyrna", "Constantinople"): 2,
			("Smyrna", "Athina"): 2,
			("Smyrna", "Angora"): 3,
			("Smyrna", "Palermo"): 6,
			("Constantinople", "Angora"): 2,
			("Constantinople", "Sevastopol"): 4,
			("Constantinople", "Bucuresti"): 3,
			("Erzurum", "Angora"): 3,
			("Erzurum", "Sochi"): 3,
			("Erzurum", "Sevastopol"): 4,
			("Rostov", "Sochi"): 2,
			("Rostov", "Kharkov"): 2,
			("Sevastopol", "Rostov"): 4,
			("Sevastopol", "Bucuresti"): 4,
			("Sevastopol", "Sochi"): 2,
			("Moskva", "Kharkov"): 4,
			("Smolensk", "Moskva"): 2,
			("Smolensk", "Wilno"): 3,
			("Smolensk", "Kyiv"): 3,
			("Kyiv", "Wilno"): 2,
			("Kyiv", "Bucuresti"): 4,
			("Kyiv", "Kharkov"): 4,
			("Kyiv", "Budapest"): 6
		}

	def calc_route(self, required: list):
		"""
		Calculates the best possible route to connect given cities
		:return: Shortest path
		"""

		# clearing worthless nodes
		self.__required = required
		self.__clear_unneeded()

		# finding shortest paths
		routes = []
		for i in self.__required:
			temp_routes = []
			shortest = [0, 99]
			for j in self.__required:
				if i == j:
					break

				temp = Dijkstra(i, j, self.places, self.distances).get_shortest_path()
				if temp[1] < shortest[1]:
					temp_routes.append(temp[0])
					shortest = [len(temp_routes) - 1, temp[1]]

			if temp_routes:
				routes.append(temp_routes[shortest[0]])

		# meshing them together into one route
		route = routes[0]
		if len(routes) != 1:
			for r in routes[1:]:
				for p in r:
					route[p] = r[p]

		# calculating the distance
		distance = 0
		for r in route:
			distance += route[r]

		return route, distance

	def __clear_unneeded(self):
		"""
		Clears all nodes from the map that don't need to be loaded
		"""

		# map of which nodes are in which areas
		areas = [
			["Paris", "Frankfurt", "Zurich", "Venezia", "Munchen", "Zagrab", "Wien", "Berlin", "Budapest", "Bucuresti", "Sevastopol", "Rostov"],
			["Edinburgh", "London", "Dieppe", "Bruxelles", "Amsterdam"],
			["Brest"],
			["Pamplona", "Barcelona", "Madrid", "Lisboa", "Cadiz", "Marseille"],
			["Roma", "Brindisi", "Palermo", "Sarajevo", "Sofia", "Athina", "Smyrna", "Constantinople", "Angora", "Erzurum", "Sochi"],
			["Essen", "Kobenhavn", "Stockholm", "Danzic", "Riga", "Petrograd"],
			["Warszawa", "Kharkov", "Moskva", "Smolensk", "Kyiv", "Wilno"]
		]
		areas_required = [0]
		r = list(self.__required)

		# checks which areas are needed
		for i in range(len(areas)):
			for p in range(len(r)):
				if r[p] in areas[i]:
					areas_required.append(i)
					r.pop(p)
					break
				if p > len(r):
					break

		# clears nodes not in the areas that need to be loaded
		i = 0
		while i < len(self.places):
			delete = True
			for a in areas_required:
				if self.places[i] in areas[a]:
					delete = False
					break
			if delete:
				self.__clear_node(i)
			else:
				i += 1

	def __clear_node(self, node: int):
		place = self.places[node]
		self.places.pop(node)
		dists = list(self.distances.items())
		for r in dists:
			if place in r[0]:
				self.distances.pop(r[0])


class Menu(Window):
	def __init__(self):
		Window.__init__(self, "TTR RG MM", "extras/icon.png", True)
		self.speaker.pack()
		self.question.pack()

		# extra windows
		self.__rp_win = Window("TTR Route Picker", "extras/icon.png", False)
		self.__rp_win._window.destroy()

		self.__places_list = []
		self.__required_places = []

		self.show()

	def show(self):
		"""
		Creates the main window
		"""

		title_font = Font(
			family="Fixedsys Excelsior 3.01",
			size=64,
			weight="bold"
		)

		# list of buttons (name, colour, function)
		buttons = [
			["Place Picker", "#00DD00", "place_picker"],
			["Route Map", "#0088EE", "route_map"],
			["Quit", "#CC0000", "quit"]
		]

		# creating screen
		self.question.config(text="TTR Route Generator", fg="red", font=title_font)
		for b in buttons:
			space = tk.Label(self._window, text="", bg=self._bg, fg=self._fg, font=("Consolas", 10))
			space.pack()
			self._spaces.append(space)
			button = self.make_button(b[0], getattr(self, "_" + b[2]), b[1])
			button.pack()
			self._buttons.append(button)

	def _place_picker(self):
		"""
		Creates the window to get tickets from the user
		"""

		try:
			self.__rp_win._window.deiconify()
		except:
			# place picker
			self.__rp_win = Window("TTR Place Picker", "extras/icon.png", False)
			tk.Label(self.__rp_win._window, text="", bg=self._bg).pack()
			tk.Label(self.__rp_win._window, text = 'Type the tickets you have (in the form "{destination1} : {destination2}").', font=self._font, bg=self._bg).pack()
			tk.Label(self.__rp_win._window, text="", bg=self._bg).pack()
			self.__rp_win.entry = tk.Entry(self.__rp_win._window)
			self.__rp_win.entry.pack()
			tk.Label(self.__rp_win._window, text="", bg=self._bg).pack()
			self.__rp_win.make_button("Add", self.__add_ticket, "white").pack()
			tk.Label(self.__rp_win._window, text="", bg=self._bg).pack()
			self.__rp_win.message = tk.Label(self.__rp_win._window, text="", bg=self._bg, font=self._button_font)
			self.__rp_win.message.pack()

			# list of picked places
			lesser_font = Font(
				family="Fixedsys Excelsior 3.01",
				size=24,
				weight="normal"
			)

			if len(self.__places_list) > 0:
				longest = len(max(self.__places_list, key=len))
			else:
				longest = 0

			# aligning the title
			title = "Picked Routes:"
			title_length = int(len(title) / 0.75) - 1
			if longest > title_length:
				list_width = longest
				title2 = title + (" " * int((list_width - title_length) * 0.75))
			else:
				list_width = title_length
				title2 = title

			# making the list of required places
			tk.Label(self.__rp_win._window, text=title2, bg=self._bg, font=self._font).pack()
			scrollbar = ttk.Scrollbar(self.__rp_win._window)
			scrollbar.pack(side="right", fill="y")
			self.__ticket_list = tk.Listbox(self.__rp_win._window, font=lesser_font, width=list_width, height=30, bg=self._bg, activestyle="none", exportselection=0)
			self.__ticket_list.pack(fill="y")

			for i in range(len(self.__places_list)):
				self.__ticket_list.insert("end", self.__places_list[i][0])
				self.__list_formatter(i)

			self.__ticket_list.config(yscrollcommand=scrollbar.set)
			scrollbar.config(command=self.__ticket_list.yview)

	def __list_formatter(self, index: int):
		if self.__places_list[index][1] == 1:
			self.__ticket_list.itemconfig(index, foreground="#0088EE")
		elif self.__places_list[index][1] == 2:
			self.__ticket_list.itemconfig(index, foreground="#00BB00")
		else:
			self.__ticket_list.itemconfig(index, foreground="#BB0000")

	def __add_ticket(self):
		"""
		Checks if the ticket is formatted correctly and adds the locations to the required
		"""
		ticket = self.__rp_win.entry.get()
		try:
			self.__format_ticket(ticket)
		except:
			self.__rp_win.message.config(text="Error. Ticket not written correctly.", fg="#BB0000")

	def __format_ticket(self, ticket: str):
		locations = ticket.split(" : ")
		if len(locations) == 2:
			if locations[0] != locations[1]:
				for location in ticket.split(" : "):
					if location in g.places:
						self.__add_location(location)
					else:
						self.__rp_win.message.config(text="Error. Ticket not written correctly.", fg="#BB0000")
						return
			else:
				self.__rp_win.message.config(text="Error. Ticket not written correctly.", fg="#BB0000")
				return
		else:
			self.__rp_win.message.config(text="Error. Ticket not written correctly.", fg="#BB0000")
			return
		self.__rp_win.entry.delete(0, "end")
		self.__rp_win.message.config(text="Ticket added.", fg="#00BB00")

	def __add_location(self, location):
		"""
		Adds a location to the displayed list
		:param location: Location to add
		"""
		in_list = False
		for i in range(len(self.__places_list)):
			if self.__places_list[i][0] == location:
				in_list = True
				break
		if in_list:
			self.__places_list[i][1] += 1
		else:
			i = len(self.__places_list)
			self.__places_list.append([location, 1])
			self.__required_places.append(location)
			self.__ticket_list.insert("end", location)
		self.__list_formatter(i)

	def _route_map(self):
		"""
		Creates the window that displays shortest route
		"""

		# get route
		route, distance = g.calc_route(self.__required_places)

		try:
			self.__map_win._window.deiconify()
		except:
			self.__map_win = Window("TTR Route Map", "extras/icon.png", False)

			# making the images
			images = []
			image = Image.open("extras/map.png")
			images.append(ImageTk.PhotoImage(image))

			# route display
			loaded_routes = []
			for r in route:
				file_name = (r[0] + "-" + r[1]).lower()
				image = Image.open(f"extras/map_routes/{file_name}.png")

				if file_name not in loaded_routes:
					images.append(ImageTk.PhotoImage(image))
					loaded_routes.append(file_name)

			# making the canvas
			frame = tk.Frame(self.__map_win._window, width=300, height=300)
			frame.pack(expand=True, fill="both")
			scrollbar_x = ttk.Scrollbar(frame, orient="horizontal")
			scrollbar_x.pack(side="bottom", fill="x")
			scrollbar_y = ttk.Scrollbar(frame)
			scrollbar_y.pack(side="right", fill="y")
			canvas = tk.Canvas(frame, width=300, height=300, bg=self._bg, highlightthickness=0, scrollregion=(0, 0, images[0].width() + 20, images[0].height() + 20))
			canvas.pack(fill="both", expand=True)
			canvas.config(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
			scrollbar_x.config(command=canvas.xview)
			scrollbar_y.config(command=canvas.yview)

			for i in images:
				canvas.create_image(20, 20, anchor="nw", image=i)

			tk.Label(self.__map_win._window, text=f'Trains Needed: {distance} / 45', font=self._font, bg=self._bg).pack()
			tk.mainloop()

	def _quit(self):
		quit()


g = GraphEditor()
Menu().start()