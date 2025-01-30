from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.services.k8s_service import K8sService

details_bp = Blueprint("details", __name__)
k8s_service = K8sService()

@details_bp.route("/detail")
def detail_page():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file:
        flash("No cluster or kubeconfig file specified.", "danger")
        return redirect(url_for("main.main_page"))

    workloads = k8s_service.get_all_resources(config_file, namespace)

    return render_template(
        "detail.html",
        cluster_name=cluster_name,
        config_file=config_file,
        namespace=namespace,
        workloads=workloads,
    )
