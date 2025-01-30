from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import yaml

main_bp = Blueprint("main", __name__)
UPLOAD_FOLDER = "kubeconfigs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_clusters_info(file_path):
    clusters_info = []
    try:
        with open(file_path, "r") as stream:
            config_data = yaml.safe_load(stream)
    except Exception as e:
        clusters_info.append({"Cluster Name": "YAML parsing error", "Server": str(e)})
        return clusters_info

    clusters = config_data.get("clusters", [])
    for cluster in clusters:
        name = cluster.get("name", "N/A")
        server = cluster.get("cluster", {}).get("server", "N/A")
        clusters_info.append({"Cluster Name": name, "Server": server})
    return clusters_info


@main_bp.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "warning")
            return redirect(request.url)
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            flash(f"The file '{filename}' already exists.", "warning")
        else:
            try:
                file.save(file_path)
                flash(f"Configuration '{filename}' successfully loaded!", "success")
            except Exception as e:
                flash(f"Error while uploading file: {e}", "danger")
        return redirect(url_for("main.main_page"))

    cluster_list = []
    config_files = os.listdir(UPLOAD_FOLDER)
    for config_file in config_files:
        abs_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, config_file))
        clusters_info = extract_clusters_info(abs_path)
        for info in clusters_info:
            if info.get("Cluster Name") not in ["YAML parsing error", "No clusters found"]:
                cluster_list.append(
                    {
                        "Cluster Name": info["Cluster Name"],
                        "Server": info["Server"],
                        "config": config_file,
                        "abs_path": abs_path,
                    }
                )

    return render_template("main.html", clusters=cluster_list)
