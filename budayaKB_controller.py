#!/usr/bin/env python3
"""

TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)
Hugo Irwanto


Last update: 26 November 2019

"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template
# from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()


#merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")

	if request.method == "POST":
		f = request.files['file']
		global databasefilename
		databasefilename=f.filename
		isImport= True
		try:
			budayaData.importFromCSV(f.filename)
		except:
			isImport= False
		n_data = len(budayaData.koleksi)
		return render_template("imporBudaya.html", result=n_data, fname=f.filename, isImport=isImport)


# Bagian ini adalah implementasi fitur Tambah Budaya, yaitu:
# - merender tampilan saat menu Tambah Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Tambah Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil ditambahkan 	
@app.route('/tambahBudaya', methods=['GET', 'POST'])
def tambahData():
	if request.method == "GET":
		return render_template("tambahBudaya.html")

	elif request.method == "POST":
		nama= request.form['nama']
		tipe= request.form['tipe']
		provinsi= request.form['provinsi']
		url= request.form['url']
		
		isImport= True
		if len(budayaData.koleksi) == 0:
			isImport = False
			return render_template("tambahBudaya.html", result=nama, isImport=isImport)
		elif isImport:
			val = budayaData.tambah(nama,tipe,provinsi,url)
			budayaData.exportToCSV(databasefilename)
			return render_template("tambahBudaya.html", result=nama, value=val, isImport=isImport)

# Bagian ini adalah implementasi fitur Ubah Budaya, yaitu:
# - merender tampilan saat menu Ubah Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Ubah Data" diklik
# - menampilkan notifikasi bahwa data berhasil atau tidak diubah
@app.route('/ubahBudaya', methods=['GET', 'POST'])
def ubahData():
	if request.method == "GET":
		return render_template("ubahBudaya.html")

	elif request.method == "POST":
		nama= request.form['nama']
		tipe= request.form['tipe']
		provinsi= request.form['provinsi']
		url= request.form['url']

		isImport= True
		if len(budayaData.koleksi) == 0:
			isImport = False
			return render_template("ubahBudaya.html", result=nama, isImport=isImport)
		elif isImport:
			val = budayaData.ubah(nama,tipe,provinsi,url)
			budayaData.exportToCSV(databasefilename)
			return render_template("ubahBudaya.html", result=nama, value=val, isImport=isImport)


# Bagian ini adalah implementasi fitur Hapus Budaya, yaitu:
# - merender tampilan saat menu Hapus Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Hapus Data" diklik
# - menampilkan notifikasi bahwa data berhasil atau tidak diubah
@app.route('/hapusBudaya', methods=['GET', 'POST'])
def hapusData():
	if request.method == "GET":
		return render_template("hapusBudaya.html")

	elif request.method == "POST":
		nama= request.form['nama']
		isImport= True
		if len(budayaData.koleksi) == 0:
			isImport = False
			return render_template("hapusBudaya.html", result=nama, isImport=isImport)
		elif isImport:
			val = budayaData.hapus(nama)
			budayaData.exportToCSV(databasefilename)
			return render_template("hapusBudaya.html", result=nama, value=val, isImport=isImport)



# Bagian ini adalah implementasi fitur Cari Budaya, yaitu:
# - merender tampilan saat menu Cari Budaya diklik	
# - melakukan pemrosesan terhadap dropdown button dan form yang telah diisikan
# - menampilkan notifikasi bahwa data berhasil dicari atau tidak
# - menampilkan opsi yang telah dipilih dalam bentuk tabel
@app.route('/cariBudaya', methods=['GET', 'POST'])
def cariData():
	if request.method == "GET":
		return render_template("cariBudaya.html")
	elif request.method == "POST":
		cariapa= request.form['CariApa']
		item= request.form['item']
		isImport= True
		if len(budayaData.koleksi) == 0:
			isImport = False
		if cariapa == 'All':
			x= budayaData.cariByNama('')
			return render_template("cariBudaya.html", result=item, datas=x, jumlah=len(x) , All='All', isImport=isImport)
		elif cariapa == 'cariNama':
			x= budayaData.cariByNama(item)
			return render_template("cariBudaya.html", result=item, datas=x, jumlah=len(x), apa='Nama Budaya', isImport=isImport)
		elif cariapa == 'cariTipe':
			x= budayaData.cariByTipe(item)
			return render_template("cariBudaya.html", result=item, datas=x, jumlah=len(x), apa='Tipe Budaya', isImport=isImport)
		elif cariapa == 'cariProv':
			x= budayaData.cariByProv(item)
			return render_template("cariBudaya.html", result=item, datas=x, jumlah=len(x), apa='Asal Provinsi Budaya', isImport=isImport)


# Bagian ini adalah implementasi fitur Stats Budaya, yaitu:
# - merender tampilan saat menu Stats Budaya diklik	
# - melakukan pemrosesan terhadap dropdown button yang telah dipilih
# - menampilkan opsi 'All'  yang telah dipilih dalam bentuk teks
# - menampilkan opsi 'Tipe Budaya' dan 'Asal Provinsi Budaya' yang telah dipilih dalam bentuk tabel
# - menampilkan notifikasi bahwa data berhasil ditampilkan atau tidak
@app.route('/statsBudaya', methods=['GET', 'POST'])
def statsData():
	if request.method == "GET":
		return render_template('statsBudaya.html')
	elif request.method == "POST":
		opsi = request.form['opsi']
		if opsi == 'All':
			jumlah= budayaData.stat()
			return render_template('statsBudaya.html', dicAda=jumlah)
		elif opsi == 'Tipe Budaya':
			dic= budayaData.statByTipe()
			return render_template('statsBudaya.html', dic=dic, dicAda=len(dic))
		elif opsi== 'Asal Provinsi Budaya':
			dic= budayaData.statByProv()
			return render_template('statsBudaya.html', dic=dic, dicAda=len(dic))



# run main app
if __name__ == "__main__":
	app.run(debug=True)


