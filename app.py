import os
import shutil
import yaml

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from kubernetes import client, config
from werkzeug.utils import secure_filename
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"  # Replace with your private key
UPLOAD_FOLDER = "kubeconfigs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def add_default_config():
    default_path = os.path.expanduser("~/.kube/config")
    destination = os.path.join(UPLOAD_FOLDER, "default_kube_config")
    if os.path.exists(default_path) and not os.path.exists(destination):
        try:
            shutil.copy(default_path, destination)
            print("Default kubeconfig successfully copied")
        except Exception as e:
            print("Error copying default kubeconfig:", e)
    else:
        print("Default kubeconfig not found or already copied.")


def extract_clusters_info(file_path):
    clusters_info = []
    try:
        with open(file_path, "r") as stream:
            config_data = yaml.safe_load(stream)
    except Exception as e:
        clusters_info.append({"Cluster Name": "YAML parsing error", "Server": str(e)})
        return clusters_info

    clusters = config_data.get("clusters", [])
    if clusters:
        for cluster in clusters:
            name = cluster.get("name", "N/A")
            server = cluster.get("cluster", {}).get("server", "N/A")
            clusters_info.append({"Cluster Name": name, "Server": server})
    else:
        clusters_info.append({"Cluster Name": "No clusters found", "Server": ""})
    return clusters_info


# ---- Functions for getting resources ----


def get_pods(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    v1 = client.CoreV1Api()
    try:
        if namespace == "ALL":
            pod_list = v1.list_pod_for_all_namespaces()
            return pod_list.items
        else:
            pod_list = v1.list_namespaced_pod(namespace)
            return pod_list.items
    except Exception as e:
        print("Error fetching pods:", e)
        return []


def get_deployments(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            dpl_list = apps_v1.list_deployment_for_all_namespaces()
            return dpl_list.items
        else:
            dpl_list = apps_v1.list_namespaced_deployment(namespace)
            return dpl_list.items
    except Exception as e:
        print("Error fetching deployments:", e)
        return []


def get_daemonsets(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            ds_list = apps_v1.list_daemon_set_for_all_namespaces()
            return ds_list.items
        else:
            ds_list = apps_v1.list_namespaced_daemon_set(namespace)
            return ds_list.items
    except Exception as e:
        print("Error fetching daemonsets:", e)
        return []


def get_statefulsets(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            sts_list = apps_v1.list_stateful_set_for_all_namespaces()
            return sts_list.items
        else:
            sts_list = apps_v1.list_namespaced_stateful_set(namespace)
            return sts_list.items
    except Exception as e:
        print("Error fetching statefulsets:", e)
        return []


def get_replicasets(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            rs_list = apps_v1.list_replica_set_for_all_namespaces()
            return rs_list.items
        else:
            rs_list = apps_v1.list_namespaced_replica_set(namespace)
            return rs_list.items
    except Exception as e:
        print("Error fetching replicasets:", e)
        return []


def get_replicationcontrollers(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    core_v1 = client.CoreV1Api()
    try:
        if namespace == "ALL":
            rc_list = core_v1.list_replication_controller_for_all_namespaces()
            return rc_list.items
        else:
            rc_list = core_v1.list_namespaced_replication_controller(namespace)
            return rc_list.items
    except Exception as e:
        print("Error fetching replication controllers:", e)
        return []


def get_jobs(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    batch_v1 = client.BatchV1Api()
    try:
        if namespace == "ALL":
            job_list = batch_v1.list_job_for_all_namespaces()
            return job_list.items
        else:
            job_list = batch_v1.list_namespaced_job(namespace)
            return job_list.items
    except Exception as e:
        print("Error fetching jobs:", e)
        return []


def get_cronjobs(namespace="default", kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    batch_v1 = client.BatchV1Api()
    try:
        if namespace == "ALL":
            cj_list = batch_v1.list_cron_job_for_all_namespaces()
            return cj_list.items
        else:
            cj_list = batch_v1.list_namespaced_cron_job(namespace)
            return cj_list.items
    except Exception as e:
        print("Error fetching cronjobs:", e)
        return []


def get_namespaces(kubeconfig_file=None):
    try:
        if kubeconfig_file:
            config.load_kube_config(config_file=kubeconfig_file)
        else:
            config.load_kube_config()
    except Exception as e:
        print("Error loading kubeconfig:", e)
        return []
    core_v1 = client.CoreV1Api()
    try:
        ns_list = core_v1.list_namespace()
        return [ns.metadata.name for ns in ns_list.items]
    except Exception as e:
        print("Error fetching namespaces:", e)
        return []


# -------------------------- ROUTES --------------------------


@app.route("/", methods=["GET", "POST"])
def main_page():
    """
    Home page: kubeconfig download and cluster list
    """
    add_default_config()
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "warning")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if os.path.exists(file_path):
            flash(f"The file '{filename}' already exists.", "warning")
        else:
            try:
                file.save(file_path)
                flash(f"Configuration '{filename}' successfully loaded!", "success")
            except Exception as e:
                flash(f"Error while uploading file: {e}", "danger")
        return redirect(url_for("main_page"))

    # Get a list of clusters from the downloaded files
    cluster_list = []
    config_files = os.listdir(UPLOAD_FOLDER)
    for config_file in config_files:
        abs_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, config_file))
        clusters_info = extract_clusters_info(abs_path)
        for info in clusters_info:
            if info.get("Cluster Name") not in [
                "YAML parsing error",
                "No clusters found",
            ]:
                cluster_list.append(
                    {
                        "Cluster Name": info["Cluster Name"],
                        "Server": info["Server"],
                        "config": config_file,
                        "abs_path": abs_path,
                    }
                )

    return render_template("main.html", clusters=cluster_list)


@app.route("/detail")
def detail_page():
    """
    Detail page: Left column with sections (Pods, Deployments, ...),
    Right part with resource table, ability to change namespace.
    """
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    namespace = request.args.get("namespace", "default")
    changed = request.args.get("changed", "false")
    resource_type = request.args.get("resource_type", None)

    if not cluster_name or not config_file:
        flash("No cluster or kubeconfig file specified.", "danger")
        return redirect(url_for("main_page"))

    if changed.lower() == "true":
        if namespace == "ALL":
            flash("Namespace successfully changed to ALL.", "success")
        else:
            flash(f"Namespace successfully changed to '{namespace}'.", "success")

    abs_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, config_file))

    # Reading kubeconfig to get data about the selected cluster
    try:
        with open(abs_path, "r") as stream:
            config_data = yaml.safe_load(stream)
    except Exception as e:
        flash(f"Error reading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    clusters_list = config_data.get("clusters", [])
    cluster_data = next(
        (c for c in clusters_list if c.get("name") == cluster_name), None
    )
    if not cluster_data:
        flash("Cluster information not found in configuration.", "warning")
        return redirect(url_for("main_page"))

    server = cluster_data.get("cluster", {}).get("server", "N/A")

    # Getting Kubernetes resources
    pods = get_pods(namespace, abs_path)
    deployments = get_deployments(namespace, abs_path)
    daemonsets = get_daemonsets(namespace, abs_path)
    statefulsets = get_statefulsets(namespace, abs_path)
    replicasets = get_replicasets(namespace, abs_path)
    replicationcontrollers = get_replicationcontrollers(namespace, abs_path)
    jobs = get_jobs(namespace, abs_path)
    cronjobs = get_cronjobs(namespace, abs_path)

    # We form a workloads dictionary
    def age_str(creation_ts):
        """
        Forming a line "Age" (for example, 2d 5h, 35m, etc.)
        """
        if not creation_ts:
            return ""
        now_dt = datetime.now(creation_ts.tzinfo or timezone.utc)
        delta = now_dt - creation_ts
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    # Example of an enriched Pods list
    pods_data = []
    for p in pods:
        restarts = 0
        if p.status and p.status.container_statuses:
            restarts = sum(cs.restart_count for cs in p.status.container_statuses)
        containers_count = 0
        if p.spec and p.spec.containers:
            containers_count = len(p.spec.containers)
        controlled_by = ""
        if p.metadata.owner_references:
            owner = p.metadata.owner_references[0]
            controlled_by = f"{owner.kind}/{owner.name}"
        node = p.spec.node_name if p.spec else ""
        qos = p.status.qos_class if p.status and p.status.qos_class else ""
        creation_ts = p.metadata.creation_timestamp
        pods_data.append(
            {
                "name": p.metadata.name,
                "namespace": p.metadata.namespace,
                "containers": containers_count,
                "restarts": restarts,
                "controlled_by": controlled_by,
                "node": node,
                "qos": qos,
                "age": age_str(creation_ts),
                "status": p.status.phase if p.status else "",
            }
        )

    deployments_data = []
    for d in deployments:
        # Total number of replicas
        replicas = d.status.replicas if d.status and d.status.replicas else 0
        # Number of available (already ready) replicas
        available = (
            d.status.available_replicas
            if d.status and d.status.available_replicas
            else 0
        )

        # Pods: suppose, we display in the format "available/replicas"
        pods_str = f"{available}/{replicas}"

        # Age: how many Deployments exist (from creationTimestamp)
        creation_ts = d.metadata.creation_timestamp
        age = age_str(creation_ts)

        # Conditions: Let's collect the conditions in one line.
        # Deployment can have a d.status.conditions (list) object.
        conditions_str = ""
        if d.status and d.status.conditions:
            # conditions is a list of elements with type, status, reason, message, etc.
            # We can just take type + status, or whatever we need
            cond_list = []
            for c in d.status.conditions:
                cond_list.append(f"{c.type}={c.status}")
            conditions_str = ", ".join(cond_list)

        deployments_data.append(
            {
                "name": d.metadata.name,
                "namespace": d.metadata.namespace,
                "pods_str": pods_str,  # "available/replicas"
                "replicas": replicas,  # or you can not duplicate
                "age": age,
                "conditions": conditions_str,
            }
        )

    ds_data = []
    for ds in daemonsets:
        desired = ds.status.desired_number_scheduled if ds.status else 0
        current = ds.status.current_number_scheduled if ds.status else 0
        ready = ds.status.number_ready if ds.status else 0

        # For example, "Pods" = "current/desired (ready)"
        # You can display it however you want; here's one option:
        pods_str = f"{current}/{desired} (ready: {ready})"

        # Node Selector is stored in ds.spec.template.spec.node_selector (dict)
        node_selector_dict = {}
        if ds.spec and ds.spec.template and ds.spec.template.spec:
            if ds.spec.template.spec.node_selector:
                node_selector_dict = ds.spec.template.spec.node_selector

        # Convert to key=values ​​separated by commas
        if node_selector_dict:
            node_selector_str = ", ".join(
                [f"{k}={v}" for k, v in node_selector_dict.items()]
            )
        else:
            node_selector_str = "—"  # if there is nothing

        # Age
        creation_ts = ds.metadata.creation_timestamp
        ds_age = age_str(creation_ts)

        ds_data.append(
            {
                "name": ds.metadata.name,
                "namespace": ds.metadata.namespace,
                "desired": desired,
                "current": current,
                "ready": ready,
                "pods_str": pods_str,
                "node_selector": node_selector_str,
                "age": ds_age,
            }
        )

    sts_data = []
    for sts in statefulsets:
        replicas = sts.status.replicas or 0
        ready = sts.status.ready_replicas or 0
        current = sts.status.current_replicas or 0
        updated = sts.status.updated_replicas or 0

        # For example, "pods_str" = "ready/replicas"
        pods_str = f"{ready}/{replicas}"

        # Age (with creation_timestamp)
        creation_ts = sts.metadata.creation_timestamp
        sts_age = age_str(creation_ts)

        sts_data.append(
            {
                "name": sts.metadata.name,
                "namespace": sts.metadata.namespace,
                "replicas": replicas,
                "current_replicas": current,
                "ready_replicas": ready,
                "updated_replicas": updated,
                "pods_str": pods_str,
                "age": sts_age,
            }
        )

    replicasets_data = []
    for rs in replicasets:
        # Desired = rs.spec.replicas
        desired = rs.spec.replicas if rs.spec and rs.spec.replicas else 0

        # Current = rs.status.replicas (how many are actually launched Pod'ів)
        current = rs.status.replicas if rs.status and rs.status.replicas else 0

        # Ready Replicas
        ready = (
            rs.status.ready_replicas if rs.status and rs.status.ready_replicas else 0
        )

        # Age = creation_timestamp
        creation_ts = rs.metadata.creation_timestamp
        rs_age = age_str(creation_ts)

        replicasets_data.append(
            {
                "name": rs.metadata.name,
                "namespace": rs.metadata.namespace,
                "desired": desired,
                "current": current,
                "ready": ready,
                "age": rs_age,
            }
        )

    replicationcontrollers = get_replicationcontrollers(namespace, abs_path)

    rc_data = []
    for rc in replicationcontrollers:
        # Replicas, which ones now Running
        replicas = rc.status.replicas if rc.status and rc.status.replicas else 0

        # Desired Replicas (specified in spec)
        desired_replicas = rc.spec.replicas if rc.spec and rc.spec.replicas else 0

        # Selector
        # rc.spec.selector — this is a dict type {"app": "my-app"}
        selector_str = ""
        if rc.spec and rc.spec.selector:
            sel_dict = rc.spec.selector
            # Convert to a string "key=value, key2=value2"
            selector_str = ", ".join([f"{k}={v}" for k, v in sel_dict.items()])

        rc_data.append(
            {
                "name": rc.metadata.name,
                "namespace": rc.metadata.namespace,
                "replicas": replicas,
                "desired_replicas": desired_replicas,
                "selector": selector_str,
            }
        )

    jobs_data = []
    for j in jobs:
        # Completions
        completions = j.spec.completions if j.spec and j.spec.completions else 0

        # Parallelism
        parallelism = j.spec.parallelism if j.spec and j.spec.parallelism else 0

        # Succeeded
        succeeded = j.status.succeeded if j.status and j.status.succeeded else 0

        # Failed
        failed = j.status.failed if j.status and j.status.failed else 0

        # Age (from creation_timestamp)
        creation_ts = j.metadata.creation_timestamp
        job_age = age_str(creation_ts)

        # Conditions
        # j.status.conditions can be a list of objects with type, status, reason, message, lastProbeTime, lastTransitionTime
        # For example, let's create a short string: "Complete=True, Failed=False" etc.
        cond_str = ""
        if j.status and j.status.conditions:
            cond_list = []
            for c in j.status.conditions:
                # For example: "<type>=<status>"
                cond_list.append(f"{c.type}={c.status}")
            cond_str = ", ".join(cond_list)

        jobs_data.append(
            {
                "name": j.metadata.name,
                "namespace": j.metadata.namespace,
                "completions": completions,
                "parallelism": parallelism,
                "succeeded": succeeded,
                "failed": failed,
                "age": job_age,
                "conditions": cond_str,
            }
        )

    cronjobs_data = []
    for cj in cronjobs:
        # Name
        name = cj.metadata.name
        # Namespace
        namespace_cj = cj.metadata.namespace

        # Schedule
        schedule = cj.spec.schedule if cj.spec and cj.spec.schedule else ""

        # Successful
        successful = (
            cj.spec.successful_jobs_history_limit
            if (cj.spec and cj.spec.successful_jobs_history_limit is not None)
            else 0
        )

        # Failed
        failed = (
            cj.spec.failed_jobs_history_limit
            if (cj.spec and cj.spec.failed_jobs_history_limit is not None)
            else 0
        )

        # Suspend
        suspend = (
            cj.spec.suspend if (cj.spec and cj.spec.suspend is not None) else False
        )

        # Active = number of active Job'ів
        active_count = 0
        if cj.status and cj.status.active:
            active_count = len(cj.status.active)

        # Last Schedule
        last_schedule = "Never"
        if cj.status and cj.status.last_schedule_time:
            last_schedule = cj.status.last_schedule_time.isoformat()

        # Age
        creation_ts = cj.metadata.creation_timestamp
        cj_age = age_str(creation_ts)

        cronjobs_data.append(
            {
                "name": name,
                "namespace": namespace_cj,
                "schedule": schedule,
                "successful": successful,
                "failed": failed,
                "suspend": suspend,
                "active": active_count,
                "last_schedule_time": last_schedule,
                "age": cj_age,
            }
        )

    workloads = {
        "pods": pods_data,
        "deployments": deployments_data,
        "daemonsets": ds_data,
        "statefulsets": sts_data,
        "replicasets": replicasets_data,
        "replicationcontrollers": rc_data,
        "jobs": jobs_data,
        "cronjobs": cronjobs_data,
    }

    # -- ADDING A BLOCK FOR OVERVIEW --
    # For example, let's count:
    # - totalPodsCount
    # - runningPodsCount
    # - deploymentsCount
    # - daemonsetsCount
    # - jobsCount
    # ...
    # You can count any metrics you need for the overview.

    total_pods = len(pods)
    running_pods = sum(1 for p in pods if p.status and p.status.phase == "Running")
    deployments_count = len(deployments)
    daemonsets_count = len(daemonsets)
    statefulsets_count = len(statefulsets)
    replicasets_count = len(replicasets)
    jobs_count = len(jobs)
    cronjobs_count = len(cronjobs)
    # You can calculate something else.

    workloads["overview"] = {
        "total_pods": total_pods,
        "running_pods": running_pods,
        "deployments_count": deployments_count,
        "daemonsets_count": daemonsets_count,
        "statefulsets_count": statefulsets_count,
        "replicasets_count": replicasets_count,
        "jobs_count": jobs_count,
        "cronjobs_count": cronjobs_count,
        # If desired, some more fields (e.g. ReplicaSets, RC, etc.)
    }

    # Get a list of Namespaces
    namespaces_list = get_namespaces(abs_path)

    return render_template(
        "detail.html",
        cluster_name=cluster_name,
        server=server,
        config_file=config_file,
        namespace=namespace,
        namespaces=namespaces_list,
        workloads=workloads,
        resource_type=resource_type,
    )


# ----------------- Detailed pages for each resource -----------------


@app.route("/pod_detail")
def pod_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    pod_name = request.args.get("pod")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not pod_name:
        flash("Not all necessary data is provided for Pod.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    v1 = client.CoreV1Api()
    try:
        if namespace == "ALL":
            all_pods = v1.list_pod_for_all_namespaces().items
            pod_obj = next((p for p in all_pods if p.metadata.name == pod_name), None)
        else:
            pod_obj = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
    except Exception as e:
        flash(f"Error while receiving Pod: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
                resource_type="pods",
            )
        )

    if not pod_obj:
        flash("Pod not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
                resource_type="pods",
            )
        )

    pod_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(pod_obj),
        default_flow_style=False,
        sort_keys=False,
    )
    return render_template(
        "pod_detail.html",
        cluster_name=cluster_name,
        pod_name=pod_name,
        pod_yaml=pod_yaml,
        config_file=config_file,
        namespace=namespace,
    )


@app.route("/deployment_detail")
def deployment_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    deployment_name = request.args.get("deployment")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not deployment_name:
        flash("Not all necessary data is provided for Deployment.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loadingі kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            all_depls = apps_v1.list_deployment_for_all_namespaces().items
            dpl_obj = next(
                (d for d in all_depls if d.metadata.name == deployment_name), None
            )
        else:
            dpl_obj = apps_v1.read_namespaced_deployment(
                name=deployment_name, namespace=namespace
            )
    except Exception as e:
        flash(f"Error while receiving Deployment: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
                resource_type="deployments",
            )
        )

    if not dpl_obj:
        flash("Deployment not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
                resource_type="deployments",
            )
        )

    dpl_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(dpl_obj),
        default_flow_style=False,
        sort_keys=False,
    )
    return render_template(
        "deployment_detail.html",
        cluster_name=cluster_name,
        deployment_name=deployment_name,
        deployment_yaml=dpl_yaml,
        config_file=config_file,
        namespace=namespace,
    )


@app.route("/daemonset_detail")
def daemonset_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    ds_name = request.args.get("daemonset")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not ds_name:
        flash("Not all necessary data is provided for DaemonSet.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            all_ds = apps_v1.list_daemon_set_for_all_namespaces().items
            ds_obj = next((d for d in all_ds if d.metadata.name == ds_name), None)
        else:
            ds_obj = apps_v1.read_namespaced_daemon_set(
                name=ds_name, namespace=namespace
            )
    except Exception as e:
        flash(f"Error while receiving DaemonSet: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
                resource_type="daemonsets",
            )
        )

    if not ds_obj:
        flash("DaemonSet not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
                resource_type="daemonsets",
            )
        )

    ds_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(ds_obj),
        default_flow_style=False,
        sort_keys=False,
    )
    return render_template(
        "daemonset_detail.html",
        cluster_name=cluster_name,
        daemonset_name=ds_name,
        daemonset_yaml=ds_yaml,
        config_file=config_file,
        namespace=namespace,
    )


@app.route("/statefulset_detail")
def statefulset_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    statefulset_name = request.args.get("statefulset")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not statefulset_name:
        flash("Not all necessary data is provided for StatefulSet.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            all_sts = apps_v1.list_stateful_set_for_all_namespaces().items
            sts_obj = next(
                (st for st in all_sts if st.metadata.name == statefulset_name), None
            )
        else:
            sts_obj = apps_v1.read_namespaced_stateful_set(
                name=statefulset_name, namespace=namespace
            )
    except Exception as e:
        flash(f"Error while receiving StatefulSet: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    if not sts_obj:
        flash("StatefulSet not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    statefulset_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(sts_obj),
        default_flow_style=False,
        sort_keys=False,
    )

    return render_template(
        "statefulset_detail.html",
        cluster_name=cluster_name,
        statefulset_name=statefulset_name,
        statefulset_yaml=statefulset_yaml,
        config_file=config_file,
        namespace=namespace,
    )


@app.route("/replicaset_detail")
def replicaset_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    replicaset_name = request.args.get("replicaset")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not replicaset_name:
        flash("Not all necessary data is provided for ReplicaSet.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    apps_v1 = client.AppsV1Api()
    try:
        if namespace == "ALL":
            all_rs = apps_v1.list_replica_set_for_all_namespaces().items
            rs_obj = next(
                (rs for rs in all_rs if rs.metadata.name == replicaset_name), None
            )
        else:
            rs_obj = apps_v1.read_namespaced_replica_set(
                name=replicaset_name, namespace=namespace
            )
    except Exception as e:
        flash(f"Error while receiving ReplicaSet: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    if not rs_obj:
        flash("ReplicaSet not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    replicaset_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(rs_obj),
        default_flow_style=False,
        sort_keys=False,
    )

    return render_template(
        "replicaset_detail.html",
        cluster_name=cluster_name,
        replicaset_name=replicaset_name,
        replicaset_yaml=replicaset_yaml,
        config_file=config_file,
        namespace=namespace,
    )


@app.route("/replicationcontroller_detail")
def replicationcontroller_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    rc_name = request.args.get("replicationcontroller")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not rc_name:
        flash("Not all necessary data is provided for ReplicationController.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    core_v1 = client.CoreV1Api()
    try:
        if namespace == "ALL":
            all_rc = core_v1.list_replication_controller_for_all_namespaces().items
            rc_obj = next((r for r in all_rc if r.metadata.name == rc_name), None)
        else:
            rc_obj = core_v1.read_namespaced_replication_controller(
                name=rc_name, namespace=namespace
            )
    except Exception as e:
        flash(f"Error while receiving ReplicationController: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    if not rc_obj:
        flash("ReplicationController not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    rc_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(rc_obj),
        default_flow_style=False,
        sort_keys=False,
    )

    return render_template(
        "replicationcontroller_detail.html",
        cluster_name=cluster_name,
        replicationcontroller_name=rc_name,
        replicationcontroller_yaml=rc_yaml,
        config_file=config_file,
        namespace=namespace,
    )


@app.route("/job_detail")
def job_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    job_name = request.args.get("job")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not job_name:
        flash("Not all necessary data is provided for Job.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    batch_v1 = client.BatchV1Api()
    try:
        if namespace == "ALL":
            all_jobs = batch_v1.list_job_for_all_namespaces().items
            job_obj = next(
                (jb for jb in all_jobs if jb.metadata.name == job_name), None
            )
        else:
            job_obj = batch_v1.read_namespaced_job(name=job_name, namespace=namespace)
    except Exception as e:
        flash(f"Error while receiving Job: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    if not job_obj:
        flash("Job not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    job_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(job_obj),
        default_flow_style=False,
        sort_keys=False,
    )

    return render_template(
        "job_detail.html",
        cluster_name=cluster_name,
        job_name=job_name,
        job_yaml=job_yaml,
        config_file=config_file,
        namespace=namespace,
    )


@app.route("/cronjob_detail")
def cronjob_detail():
    cluster_name = request.args.get("cluster")
    config_file = request.args.get("config")
    cronjob_name = request.args.get("cronjob")
    namespace = request.args.get("namespace", "default")

    if not cluster_name or not config_file or not cronjob_name:
        flash("Not all necessary data is provided for CronJob.", "danger")
        return redirect(url_for("main_page"))

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        flash(f"Error while loading kubeconfig: {e}", "danger")
        return redirect(url_for("main_page"))

    batch_v1 = client.BatchV1Api()
    try:
        if namespace == "ALL":
            all_cj = batch_v1.list_cron_job_for_all_namespaces().items
            cj_obj = next(
                (cj for cj in all_cj if cj.metadata.name == cronjob_name), None
            )
        else:
            cj_obj = batch_v1.read_namespaced_cron_job(
                name=cronjob_name, namespace=namespace
            )
    except Exception as e:
        flash(f"Error while receiving CronJob: {e}", "danger")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    if not cj_obj:
        flash("CronJob not found", "warning")
        return redirect(
            url_for(
                "detail_page",
                cluster=cluster_name,
                config=config_file,
                namespace=namespace,
            )
        )

    cronjob_yaml = yaml.dump(
        client.ApiClient().sanitize_for_serialization(cj_obj),
        default_flow_style=False,
        sort_keys=False,
    )

    return render_template(
        "cronjob_detail.html",
        cluster_name=cluster_name,
        cronjob_name=cronjob_name,
        cronjob_yaml=cronjob_yaml,
        config_file=config_file,
        namespace=namespace,
    )


# ----------------- Additional routes for Sidebar -----------------


@app.route("/pod_details", methods=["GET"])
def pod_details():
    """
    Route to get Pod details in JSON format.
    Used for sidebar.
    """
    cluster = request.args.get("cluster")
    config_file = request.args.get("config")
    namespace = request.args.get("namespace")
    pod_name = request.args.get("pod_name")

    if not all([cluster, config_file, namespace, pod_name]):
        return jsonify({"error": "Not enough parameters."}), 400

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        return jsonify({"error": f"Upload error kubeconfig: {e}"}), 500

    v1 = client.CoreV1Api()
    try:
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        pod_dict = pod.to_dict()
        return jsonify(pod_dict)
    except client.exceptions.ApiException as e:
        return jsonify({"error": f"Error API: {e}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete_pod", methods=["POST"])
def delete_pod():
    """
    Route to remove Pod.
    Expects JSON with: cluster, config, namespace, pod_name
    """
    data = request.get_json()
    cluster = data.get("cluster")
    config_file = data.get("config")
    namespace = data.get("namespace")
    pod_name = data.get("pod_name")

    if not all([cluster, config_file, namespace, pod_name]):
        return jsonify({"error": "Not enough parameters."}), 400

    abs_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], config_file))
    try:
        config.load_kube_config(config_file=abs_path)
    except Exception as e:
        return jsonify({"error": f"Upload error kubeconfig: {e}"}), 500

    v1 = client.CoreV1Api()
    try:
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        return jsonify({"success": True}), 200
    except client.exceptions.ApiException as e:
        return jsonify({"error": f"Error API: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=8000, debug=True)
