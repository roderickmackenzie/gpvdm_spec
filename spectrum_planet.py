# -*- coding: utf-8 -*-
#    General-purpose Photovoltaic Device Model - a drift diffusion base/Shockley-Read-Hall
#    model for 1st, 2nd and 3rd generation solar cells.
#    Copyright (C) 2017 Edward Grant  eayeg3 at nottingham.ac.uk
#    Copyright (C) 2017 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#	https://www.gpvdm.com
#	Room B86 Coates, University Park, Nottingham, NG7 2RD, UK
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License v2.0, as published by
#    the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import unicode_literals

import os
import sys
from PyQt5.QtWidgets import QToolBar,QAction,QWidget,QLabel,QComboBox,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from decimal import Decimal

import io

from spectrum_pref import checkBoxInput
from spectrum_model import earthModel
from spectrum_info import infoBox
from spectrum_model import mercury_calc
from spectrum_model import venus_calc
from spectrum_model import mars_calc
from spectrum_model import ceres_calc
from spectrum_model import europa_calc
from spectrum_model import halley_calc
from spectrum_model import pluto_calc
from spectrum_model import earth_calc

from math import pi

#unicode indexes
degree_sign= u'\N{DEGREE SIGN}'

# GUI

class planet(QWidget):
	def __init__(self):
		self.enable_earthattr = False
		self.enable_mercuryattr = False
		self.enable_marsattr = False
		self.enable_venusattr = False
		self.enable_halleyattr = False
		self.enable_ceresattr = False
		self.enable_europaattr = False
		self.enable_plutoattr = False
		self.enable_orbitalpoint = False
		super().__init__()


	def init(self):

		if self.enable_earthattr==True:
			userInput = earthModel('53', '-1', '1.42', '1013.25', '15/06/2014', '12:00', '0.27', '0')
			london = earthModel('51.5074', '-0.1278', '2.13', '1013', '15/06/2014', '12:00', '0.43', '0')
			beijing = earthModel('39.9042', '116.4074', '2.98', '1013', '15/06/2014', '12:00', '0.97', '+8')
			losangeles = earthModel('34.0522', '-118.2437', '1.54', '1013', '15/06/2014', '12:00', '0.10', '-8')
			newyork = earthModel('40.7128', '-74.0059', '2.74', '1013', '15/06/2014', '12:00', '0.15', '-5')
			freiburg = earthModel('47.9990', '7.8421', '1.91', '1013', '15/06/2014', '12:00', '0.13', '+1')
			sydney = earthModel('-33.8688', '151.2093', '1.72', '1013', '15/06/2014', '12:00', '0.04', '+10')
			self.models = {"User Input": userInput, "London": london, "Beijing": beijing, "Los Angeles": losangeles,
							"New York": newyork, "Freiburg": freiburg, "Sydney": sydney}
			self.selectedModel = userInput

		self.states = [True, True, True, True, True, True, True]

		#TOOLBAR WIDGET
		self.toolbar = QToolBar()

		plotPreferencesAction = QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'prefs.png')), 'Plot Preferences', self)
		plotPreferencesAction.triggered.connect(self.setPlotPreferences)

		saveFigureAction =  QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'save.png')), 'Save Figure', self)
		saveFigureAction.triggered.connect(self.save)

		copyFigureAction = QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'copy.png')), 'Copy Figure', self)
		copyFigureAction.triggered.connect(self.copy2clip)

		calcSolarConstAction = QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'calc.png')), 'Calculate Solar Constant', self)
		calcSolarConstAction.triggered.connect(self.solar_const_calc)

		infoAction = QAction(QIcon(os.path.join(os.getcwd(), 'icons', 'info.png')), 'Information', self)
		infoAction.triggered.connect(self.showInfo)

		self.toolbar.addAction(plotPreferencesAction)
		self.toolbar.addAction(saveFigureAction)
		self.toolbar.addAction(copyFigureAction)
		self.toolbar.addAction(calcSolarConstAction)
		self.toolbar.addAction(infoAction)



		#DEFINING EARTH WIDGETS
		if self.enable_earthattr==True:
			self.arbitraryWidget = QLabel(self)  #Arbitrary
			self.arbitraryWidget.setText('')

			self.InstructionLabel = QLabel(self)
			self.InstructionLabel.setText('Please choose city or User Input.')

			# drop down menu
			self.DropDown = QComboBox(self)
			self.DropDown.addItem("User Input")
			self.DropDown.addItem("London")
			self.DropDown.addItem("Beijing")
			self.DropDown.addItem("Los Angeles")
			self.DropDown.addItem("New York")
			self.DropDown.addItem("Freiburg")
			self.DropDown.addItem("Sydney")
			self.DropDown.activated[str].connect(self.onActivated)

			# Latitude
			self.LatitudeLabel = QLabel(self)
			self.LatitudeLabel.setText('Latitude')
			self.LatitudeInput = QLineEdit(self)
			self.LatitudeUnit = QLabel(self)
			self.LatitudeUnit.setText(degree_sign)

			# Longitude
			self.LongitudeLabel = QLabel(self)
			self.LongitudeLabel.setText('Longitude')
			self.LongitudeInput = QLineEdit(self)
			self.LongitudeUnit = QLabel(self)
			self.LongitudeUnit.setText(degree_sign)

			# Date
			self.DateLabel = QLabel(self)
			self.DateLabel.setText('Date (dd/mm/yyyy)')
			self.DateInput = QLineEdit(self)

			# Time
			self.TimeLabel = QLabel(self)
			self.TimeLabel.setText('Local Time (hh:mm)')
			self.TimeInput = QLineEdit(self)

			# Timezone
			self.TimezoneLabel = QLabel(self)
			self.TimezoneLabel.setText('Timezone (UTC-11 - UTC+12)')
			self.TimezoneInput = QLineEdit(self)

			# Pressure
			self.pLabel = QLabel(self)
			self.pLabel.setText('Ground Pressure')
			self.pInput = QLineEdit(self)
			self.PressureUnit = QLabel(self)
			self.PressureUnit.setText('mb')

			# Precipitable Water Vapour
			self.WLabel = QLabel(self)
			self.WLabel.setText('Precipitable Water Vapour')
			self.WInput = QLineEdit(self)
			self.WaterUnit = QLabel(self)
			self.WaterUnit.setText('cm')

			# Aerosol Optical Depth
			self.AODLabel = QLabel(self)
			self.AODLabel.setText('Aerosol Optical Depth')
			self.AODInput = QLineEdit(self)

			# Input valid/not valid
			self.ValidityLabel = QLabel(self)
			self.ValidityLabel.setText('Please choose city or User Input.')

			#notes
			self.notesLabel = QLabel(self)
			self.notesLabel.setWordWrap(True)
			self.notesLabel.setText(
				'Note: Data for the different cities is consistent with average conditions in June 2014.\n\n'
				'Please verify Timezone is consistent with Latitude and Longitude or the results will be invalid.')

		#mars Widgets
		if self.enable_marsattr==True:
			# Aerosol Optical Depth
			self.AODLabel = QLabel(self)
			self.AODLabel.setText('Aerosol Optical Depth')
			self.AODInput = QLineEdit(self)
			self.AODInput.setText('0.2')

			self.arbitraryWidget = QLabel(self)  # Arbitrary
			self.arbitraryWidget.setText('(0-1)')

		# Apply Button
		self.button = QPushButton('Apply')
		self.button.clicked.connect(self.Apply)

		# setting canvas for plot
		self.fig = Figure(figsize=(2.5, 2), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.figure.patch.set_facecolor('white')
		self.axes = self.fig.add_subplot(111)
		self.axes.set_xlabel('Wavelength ($\mu m$)')
		self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
		self.axes.set_xlim(0.3, 3)
		self.axes.set_ylim(0, 2200)
		self.axes.legend()


		if self.enable_earthattr==True:
			self.LatitudeInput.setText(self.selectedModel.Latitude)
			self.LongitudeInput.setText(self.selectedModel.Longitude)
			self.DateInput.setText(self.selectedModel.Date)
			self.TimeInput.setText(self.selectedModel.Time)
			self.pInput.setText(self.selectedModel.p)
			self.WInput.setText(self.selectedModel.W)
			self.AODInput.setText(self.selectedModel.AOD)
			self.TimezoneInput.setText(self.selectedModel.Timezone)

		#Orbital Point widgets and plot
		if self.enable_orbitalpoint==True:
			self.OrbitalPointLabel = QLabel(self)
			self.OrbitalPointLabel.setText('Orbital Point')
			self.OrbitalPointInput = QLineEdit(self)
			self.OrbitalPointInput.setText("0")
			self.OrbitalPointUnit = QLabel(self)
			self.OrbitalPointUnit.setText('(0-1)')

			self.notesLabel = QLabel(self)
			self.notesLabel.setWordWrap(True)
			self.notesLabel.setText(
				'Note: Orbital Point is Perihelion = 0, Aphelion = 0.5, and back to Perihelion = 1.')

			fig_orbit_size = 4
			self.fig_orbit = Figure(figsize=(fig_orbit_size, fig_orbit_size), dpi=100)
			self.canvas_orbit = FigureCanvas(self.fig_orbit)
			self.canvas_orbit.figure.patch.set_facecolor('white')
			self.fig_orbit_axes = self.fig.add_subplot(111, projection='polar')

		#Solar Constant widgets
		self.solar_const_label = QLabel()
		self.solar_const_label.setText('')
		self.solar_const = QLabel()
		self.solar_const.setText('')

		self.hbox = QHBoxLayout()
		self.hbox.addWidget(self.solar_const_label)
		self.hbox.addWidget(self.solar_const)

		#LAYOUT

		self.inputsLayout = QHBoxLayout()

		self.vbox = QVBoxLayout()
		if self.enable_earthattr==True:
			self.vbox.addWidget(self.InstructionLabel)
			self.vbox.addWidget(self.LatitudeLabel)
			self.vbox.addWidget(self.LongitudeLabel)
			self.vbox.addWidget(self.DateLabel)
			self.vbox.addWidget(self.TimeLabel)
			self.vbox.addWidget(self.TimezoneLabel)
			self.vbox.addWidget(self.pLabel)
			self.vbox.addWidget(self.WLabel)
			self.vbox.addWidget(self.AODLabel)

		if self.enable_marsattr==True:
			self.vbox.addWidget(self.AODLabel)

		if self.enable_orbitalpoint==True:
			self.vbox.addWidget(self.OrbitalPointLabel)

		self.inputsLayout.addLayout(self.vbox)

		self.vbox = QVBoxLayout()
		if self.enable_earthattr==True:
			self.vbox.addWidget(self.DropDown)
			self.vbox.addWidget(self.LatitudeInput)
			self.vbox.addWidget(self.LongitudeInput)
			self.vbox.addWidget(self.DateInput)
			self.vbox.addWidget(self.TimeInput)
			self.vbox.addWidget(self.TimezoneInput)
			self.vbox.addWidget(self.pInput)
			self.vbox.addWidget(self.WInput)
			self.vbox.addWidget(self.AODInput)

		if self.enable_marsattr==True:
			self.vbox.addWidget(self.AODInput)

		if self.enable_orbitalpoint==True:
			self.vbox.addWidget(self.OrbitalPointInput)

		self.inputsLayout.addLayout(self.vbox)

		self.vbox = QVBoxLayout()
		if self.enable_earthattr==True:
			self.vbox.addWidget(self.arbitraryWidget)
			self.vbox.addWidget(self.LatitudeUnit)
			self.vbox.addWidget(self.LongitudeUnit)
			self.vbox.addWidget(self.arbitraryWidget)
			self.vbox.addWidget(self.arbitraryWidget)
			self.vbox.addWidget(self.arbitraryWidget)
			self.vbox.addWidget(self.PressureUnit)
			self.vbox.addWidget(self.WaterUnit)
			self.vbox.addWidget(self.arbitraryWidget)

		if self.enable_marsattr==True:
			self.vbox.addWidget(self.arbitraryWidget)

		if self.enable_orbitalpoint==True:
			self.vbox.addWidget(self.OrbitalPointUnit)

		self.inputsLayout.addLayout(self.vbox)


		self.grid = QGridLayout(self)

		# self.grid.addWidget()
		self.grid.addWidget(self.toolbar, 0,0)
		self.grid.addLayout(self.inputsLayout, 1,0)
		if self.enable_earthattr==True:
			self.grid.addWidget(self.ValidityLabel, 2, 0)
		self.grid.addWidget(self.notesLabel, 3, 0)
		if self.enable_orbitalpoint==True:
			self.grid.addWidget(self.canvas_orbit, 4, 0)
		self.grid.addLayout(self.hbox,5,0)
		self.grid.addWidget(self.button, 6, 0)
		self.grid.addWidget(self.canvas, 0, 1, 7, 1)

		self.setLayout(self.grid)


		self.Apply()

	def Apply(self):
		lam=0.0
		I_direct=0.0
		I_diffuse=0.0
		I_total=0.0
		lam_bb=0.0
		sol=0.0
		ext_ter_spec=0.0
		solar_const=0.0
		
		self.fig = Figure(figsize=(12, 8), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.figure.patch.set_facecolor('white')

		self.grid.addWidget(self.canvas, 0, 1, 7, 1)

		self.fig.clf()
		self.axes = self.fig.add_subplot(111)

		#For Orbital Plot
		if self.enable_orbitalpoint==True:
			self.fig_orbit = Figure(figsize=(4,4), dpi=100)
			self.canvas_orbit = FigureCanvas(self.fig_orbit)
			self.canvas_orbit.figure.patch.set_facecolor('white')

			self.grid.addWidget(self.canvas_orbit, 4, 0)

			self.fig_orbit.clf()
			self.fig_orbit_axes = self.fig_orbit.add_subplot(111, projection='polar')

		#For Earth
		if self.enable_earthattr==True:
			print("Calling earth!")
			Latitude = float(self.LatitudeInput.text())
			Longitude = float(self.LongitudeInput.text())
			W = float(self.WInput.text())
			p = float(self.pInput.text())
			Date = self.DateInput.text()
			Time = self.TimeInput.text()
			timezone = float(self.TimezoneInput.text())
			AOD = float(self.AODInput.text())
			lam, I_direct, I_diffuse, I_total, lam_bb, sol, ext_ter_spec, solar_const = earth_calc(Latitude, Longitude, W, p, Date, Time,
																				AOD, timezone)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[3]:
				self.axes.plot(lam, I_direct, label='Direct Irradiance')
			if self.states[4]:
				self.axes.plot(lam, I_diffuse, label='Diffuse Irradiance')
			if self.states[5]:
				self.axes.plot(lam, I_total, label='Total Irradiance')
			if self.states[6]:
				self.axes.legend()


			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 2200)

			self.ValidityLabel.setText('')


		#For Mercury
		if self.enable_mercuryattr == True:
			orbitalpoint = float(self.OrbitalPointInput.text())
			sol, lam_bb, maximum, r, solar_const, r_plot, theta, ext_ter_spec, lam = mercury_calc(orbitalpoint)

			self.plot_orbit(r, r_plot, theta, orbitalpoint)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[6]:
				self.axes.legend()
			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 1.1 * maximum)

		# For Mars
		if self.enable_marsattr == True:
			AOD = float(self.AODInput.text())
			orbitalpoint = float(self.OrbitalPointInput.text())
			sol, lam_bb, maximum, r, solar_const, r_plot, theta, ext_ter_spec, lam, total = mars_calc(orbitalpoint, AOD)

			self.plot_orbit(r, r_plot, theta, orbitalpoint)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[5]:
				self.axes.plot(lam, total, label='Total')
			if self.states[6]:
				self.axes.legend()
			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 1.1 * maximum)


		#For Venus
		if self.enable_venusattr==True:
			orbitalpoint = float(self.OrbitalPointInput.text())
			sol, lam_bb, maximum, r, solar_const, r_plot, theta, ext_ter_spec, lam, total = venus_calc(orbitalpoint)

			self.plot_orbit(r, r_plot, theta, orbitalpoint)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[5]:
				self.axes.plot(lam, total, label="Total")
			if self.states[6]:
				self.axes.legend()
			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 1.1*maximum)

		#For Halley
		if self.enable_halleyattr==True:
			orbitalpoint = float(self.OrbitalPointInput.text())
			sol, lam_bb, maximum, r, solar_const, r_plot, theta, r2, ext_ter_spec, lam = halley_calc(orbitalpoint)

			self.fig_orbit_axes.plot(theta, r_plot)
			self.fig_orbit_axes.plot(0, 0, c='y', marker='o', markersize=10)
			self.fig_orbit_axes.plot(orbitalpoint*2*pi, r2, c='r', marker='o', markersize=5)
			self.fig_orbit_axes.set_title('Orbital Position', fontsize=10)
			self.fig_orbit_axes.yaxis.grid(False)
			self.fig_orbit_axes.xaxis.grid(False)
			self.fig_orbit_axes.get_xaxis().set_visible(False)
			self.fig_orbit_axes.get_yaxis().set_visible(False)
			self.fig_orbit_axes.spines['polar'].set_visible(False)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[6]:
				self.axes.legend()
			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 1.1*maximum)

		# For Europa
		if self.enable_europaattr == True:
			orbitalpoint = float(self.OrbitalPointInput.text())
			sol, lam_bb, maximum, r, solar_const, r_plot, theta, ext_ter_spec, lam = europa_calc(orbitalpoint)

			self.plot_orbit(r, r_plot, theta, orbitalpoint)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[6]:
				self.axes.legend()
			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 1.1 * maximum)

		# For Ceres
		if self.enable_ceresattr == True:
			orbitalpoint = float(self.OrbitalPointInput.text())
			sol, lam_bb, maximum, r, solar_const, r_plot, theta, ext_ter_spec, lam = ceres_calc(orbitalpoint)

			self.plot_orbit(r, r_plot, theta, orbitalpoint)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[6]:
				self.axes.legend()
			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 1.1 * maximum)

		# For Ceres
		if self.enable_plutoattr == True:
			orbitalpoint = float(self.OrbitalPointInput.text())
			sol, lam_bb, maximum, r, solar_const, r_plot, theta, ext_ter_spec, lam = pluto_calc(orbitalpoint)

			self.plot_orbit(r, r_plot, theta, orbitalpoint)

			if self.states[0]:
				self.axes.set_title('Solar Spectrum')
			if self.states[1]:
				self.axes.plot(lam_bb * 10 ** 6, sol * 10 ** 3, label='Black body at 5800K')
			if self.states[2]:
				self.axes.plot(lam, ext_ter_spec, label='Extraterrestrial Spectrum')
			if self.states[6]:
				self.axes.legend()
			self.axes.set_xlabel('Wavelength ($\mu m$)')
			self.axes.set_ylabel('Irradiance ($W/m^2/\mu m$)')
			self.axes.set_xlim(0.3, 3)
			self.axes.set_ylim(0, 1.1 * maximum)



		self.solar_const_label.setText('')
		self.solar_const.setText('')
		return solar_const


	def save(self):
		fname = QFileDialog.getSaveFileName(self, 'Save file', '', '.png')

		self.fig.savefig(fname[0] + fname[1])

	def copy2clip(self):
		buf = io.BytesIO()
		self.fig.savefig(buf)
		QApplication.clipboard().setImage(QImage.fromData(buf.getvalue()))

	def solar_const_calc(self, solar_const):
		solar_const = self.Apply()
		solar_const = round(Decimal(solar_const),2)
		self.solar_const_label.setText('Solar Constant (W/m^2):')
		self.solar_const.setText(str(solar_const))
		self.newfont = QFont("Times", 10)
		self.solar_const.setFont(self.newfont)

	def showInfo(self):
		popup = infoBox(self)
		popup.show()

	def setPlotPreferences(self):
		dialog = checkBoxInput(self)
		dialog.show()

	def onActivated(self, modelName):
		if modelName != "User Input":
			self.LatitudeInput.setDisabled(True)
			self.LongitudeInput.setDisabled(True)
			self.DateInput.setDisabled(True)
			self.TimeInput.setDisabled(True)
			self.TimezoneInput.setDisabled(True)
			self.pInput.setDisabled(True)
			self.WInput.setDisabled(True)
			self.AODInput.setDisabled(True)
		else:
			self.LatitudeInput.setDisabled(False)
			self.LongitudeInput.setDisabled(False)
			self.DateInput.setDisabled(False)
			self.TimeInput.setDisabled(False)
			self.TimezoneInput.setDisabled(False)
			self.pInput.setDisabled(False)
			self.WInput.setDisabled(False)
			self.AODInput.setDisabled(False)

		# remembers inputs
		self.selectedModel.Latitude = self.LatitudeInput.text()
		self.selectedModel.Longitude = self.LongitudeInput.text()
		self.selectedModel.Date = self.DateInput.text()
		self.selectedModel.Time = self.TimeInput.text()
		self.selectedModel.Timezone = self.TimezoneInput.text()
		self.selectedModel.p = self.pInput.text()
		self.selectedModel.W = self.WInput.text()
		self.selectedModel.AOD = self.AODInput.text()

		self.selectedModel = self.models[modelName]
		self.LatitudeInput.setText(self.selectedModel.Latitude)
		self.LongitudeInput.setText(self.selectedModel.Longitude)
		self.DateInput.setText(self.selectedModel.Date)
		self.TimeInput.setText(self.selectedModel.Time)
		self.TimezoneInput.setText(self.selectedModel.Timezone)
		self.pInput.setText(self.selectedModel.p)
		self.WInput.setText(self.selectedModel.W)
		self.AODInput.setText(self.selectedModel.AOD)

	def plot_orbit(self, r, r_plot, theta, orbitalpoint):
		self.fig_orbit_axes.plot(theta, r_plot)
		self.fig_orbit_axes.plot(0, 0, c='y', marker='o', markersize=10)
		self.fig_orbit_axes.plot(orbitalpoint * 2 * pi, r, c='r', marker='o', markersize=5)
		self.fig_orbit_axes.set_title('Orbital Position', fontsize=10)
		self.fig_orbit_axes.yaxis.grid(False)
		self.fig_orbit_axes.xaxis.grid(False)
		self.fig_orbit_axes.get_xaxis().set_visible(False)
		self.fig_orbit_axes.get_yaxis().set_visible(False)
		self.fig_orbit_axes.spines['polar'].set_visible(False)

	#functions to enable 'planet' specific GUI items
	def set_earth(self, data):
		self.enable_earthattr = data

	def set_mercury(self,data):
		self.enable_mercuryattr = data

	def set_mars(self, data):
		self.enable_marsattr = data

	def set_venus(self, data):
		self.enable_venusattr = data

	def set_halley(self, data):
		self.enable_halleyattr = data

	def set_europa(self, data):
		self.enable_europaattr = data

	def set_ceres(self,data):
		self.enable_ceresattr = data

	def set_pluto(self,data):
		self.enable_plutoattr = data

	#common widget functions
	def set_orbitalpoint(self, data):
		self.enable_orbitalpoint = data
