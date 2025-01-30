# services/k8s_service.py

from kubernetes import client, config

class K8sService:
    """
    Kubernetes service responsible for interacting with the Kubernetes API.
    """
    def __init__(self):
        # Load Kubernetes configuration (either from local kubeconfig or in-cluster config)
        config.load_kube_config()  # Use config.load_incluster_config() for production
        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
    
    def get_pods(self, namespace):
        """
        Retrieve a list of pods in the specified namespace.
        """
        pods = self.core_api.list_namespaced_pod(namespace)
        return [pod.metadata.name for pod in pods.items]
    
    def get_pod_details(self, namespace, pod_name):
        """
        Retrieve detailed information about a specific pod.
        """
        pod = self.core_api.read_namespaced_pod(pod_name, namespace)
        return pod.to_dict()
    
    def get_namespaces(self):
        """
        Retrieve a list of all namespaces in the cluster.
        """
        namespaces = self.core_api.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]
    
    def get_deployments(self, namespace):
        """
        Retrieve a list of deployments in the specified namespace.
        """
        deployments = self.apps_api.list_namespaced_deployment(namespace)
        return [deployment.metadata.name for deployment in deployments.items]
