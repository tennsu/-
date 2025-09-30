from flask import Flask, render_template, request, redirect, send_from_directory
import os, json

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DATA_FILE = "data.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# データを読み書きする関数
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 紹介ページ
@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", items=data)

# 管理画面
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        title = request.form.get("title")
        url = request.form.get("url")

        # ファイルがあれば保存
        file = request.files.get("file")
        if file and file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            url = f"/uploads/{file.filename}"

        # データ追加
        data = load_data()
        data.append({"title": title, "url": url})
        save_data(data)
        return redirect("/admin")

    data = load_data()
    return render_template("admin.html", items=data)

# アップロードファイルの配信
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
