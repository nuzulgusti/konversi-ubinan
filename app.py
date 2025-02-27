from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Simpan data sementara
data_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    global data_list
    hasil_ubinan = float(request.form['hasil_ubinan'])
    luas_lahan = float(request.form['luas_lahan'])

    # Konversi
    gkp_per_ha = hasil_ubinan * 1600  # GKP per hektar
    gkg_per_ha = gkp_per_ha * 0.8  # GKG per hektar
    gkg_per_plot = gkg_per_ha / 2000
    ton_gkp = gkp_per_ha * luas_lahan / 1000
    ton_gkg = gkg_per_ha * luas_lahan / 1000
    ton_beras = ton_gkg * 0.65

    # Simpan hasil ke dalam list
    entry = {
        "hasil_ubinan": hasil_ubinan,
        "luas_lahan": luas_lahan,
        "gkp_per_ha": gkp_per_ha,
        "gkg_per_ha": gkg_per_ha,
        "gkg_per_plot": round(gkg_per_plot, 2),
        "ton_gkp": round(ton_gkp, 2),
        "ton_gkg": round(ton_gkg, 2),
        "ton_beras": round(ton_beras, 3)
    }
    data_list.append(entry)
    return jsonify(data_list)

@app.route('/delete', methods=['POST'])
def delete():
    global data_list
    index = int(request.form['index'])
    if 0 <= index < len(data_list):
        del data_list[index]
    return jsonify(data_list)

@app.route('/download', methods=['GET'])
def download():
    if not data_list:
        return jsonify({"status": "error", "message": "Tidak ada data untuk diunduh!"})

    df = pd.DataFrame(data_list)
    file_path = "hasil_konversi.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True, download_name="hasil_konversi.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
