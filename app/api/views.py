from flask import Blueprint, request, jsonify, flash
from kubernetes import client, config
import os
import yaml

api_bp = Blueprint("api", __name__)

UPLOAD_FOLDER = "kubeconfigs"

def load_kube_config(config_file):
    try:
        abs_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, config_file))
        config.load_kube_config(config_file=abs_path)
        return True, None
    except Exception as e:
        return False, str(e)


@api_bp.route("/pod_details", methods=["GET"])
def pod_details():
    cluster = request.args.get("cluster")
    config_file = request.args.get("config")
    namespace = request.args.get("namespace")
    pod_name = request.args.get("pod_name")

    if not all([cluster, config_file, namespace, pod_name]):
        return jsonify({"error": "Not enough parameters."}), 400

    success, error = load_kube_config(config_file)
    if not success:
        return jsonify({"error": f"Error loading kubeconfig: {error}"}), 500

    v1 = client.CoreV1Api()
    try:
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        pod_dict = pod.to_dict()
        return jsonify(pod_dict)
    except client.exceptions.ApiException as e:
        return jsonify({"error": f"API Error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/delete_pod", methods=["POST"])
def delete_pod():
    data = request.get_json()
    cluster = data.get("cluster")
    config_file = data.get("config")
    namespace = data.get("namespace")
    pod_name = data.get("pod_name")

    if not all([cluster, config_file, namespace, pod_name]):
        return jsonify({"error": "Not enough parameters."}), 400

    success, error = load_kube_config(config_file)
    if not success:
        return jsonify({"error": f"Error loading kubeconfig: {error}"}), 500

    v1 = client.CoreV1Api()
    try:
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        return jsonify({"success": True}), 200
    except client.exceptions.ApiException as e:
        return jsonify({"error": f"API Error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
