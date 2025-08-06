'''
DevOps is about automating and improving the process of building, testing, releasing, and deploying software — faster and more reliably.
CI/CD (Continuous Integration / Continuous Deployment)
'''

'''
2. Tools
Version Control: Git, GitHub, GitLab
CI/CD Tools: Jenkins, GitHub Actions, GitLab CI, CircleCI
Containers: Docker
Orchestration: Kubernetes, Helm
Infrastructure as Code: Terraform, Ansible
Monitoring: Prometheus, Grafana
Cloud Providers: AWS, Azure, GCP
'''
#lint
'''
    In programming, lint (or linter) refers to a tool that analyzes your code for potential errors, 
    bugs, stylistic issues, or suspicious constructs.
    A linter checks your code for:

        Syntax errors
        Code style violations (e.g., indentation, naming conventions)
        Potential bugs (e.g., unused variables, unreachable code)
        Best practices (e.g., avoiding deprecated functions)
    Python	pylint, flake8, black (formatter)
    
    flake8 my_script.py
    my_script.py:3:1: F401 'os' imported but unused
    my_script.py:5:80: E501 line too long (82 > 79 characters)

'''

#code coverage
'''
    In SonarQube, code coverage refers to the percentage of your source code that is tested by automated tests (like unit tests). It helps you understand how much of your code is being exercised during testing, which is a key indicator of code quality and test effectiveness.

    What Code Coverage Measures:
    Lines covered: How many lines of code were executed during tests.
    Branches covered: Whether all possible paths (like if/else conditions) were tested.
    Conditions covered: Whether all boolean expressions were evaluated both true and false.'''

'''
Version control is a system that tracks changes to files over time, allowing multiple people to collaborate,
 experiment, and manage different versions of a project — especially in software development.

 GitHub is a web-based platform that helps developers store, manage, and collaborate on code using the Git version control system.
 
 '''
import git,os
import subprocess

def pull_latest_code():
    print('pulling latest code from repository')
    REPO_NAME,BRANCH='flask_demo','main'
    REPO_URL=f"https://github.com/viswavisan/{REPO_NAME}.git"
    if os.path.exists(REPO_NAME):
        repo = git.Repo(REPO_NAME)
        repo.git.checkout(BRANCH)
        repo.remotes.origin.pull()
    else:
        git.Repo.clone_from(REPO_URL,REPO_NAME, branch=BRANCH)

# pull_latest_code()

#build image
'''
Building an image means packaging your app into a single, 
portable file that can run consistently anywhere — on your machine, server, or cloud.
'''

#docker
'''
Docker is a tool that helps you run applications in isolated, portable environments called containers. 
It's like a lightweight, faster version of virtual machines.
'''

#ECS
'''
Amazon ECS (Elastic Container Service) is a fully managed container orchestration service provided by AWS.
It lets you easily run, stop, and scale Docker containers on a cluster of virtual machines or serverless infrastructure (like Fargate).
'''
import docker
def build_image():
    d_client = docker.from_env()
    REPO_NAME='flask_demo'
    container_path="ghcr.io/viswavisan/"
    image_name=f'{container_path}{REPO_NAME}:latest'
    print('building image...')
    try:
        image, build_logs = d_client.images.build(path='./' + REPO_NAME, tag=image_name)
        for log in build_logs:print(log)
        print(image)
    except Exception as e: print(str(e))



#ECR
'''
ECR (Elastic Container Registry) is a fully managed Docker image registry provided by AWS.
It allows you to store, manage, and share Docker container images securely in the cloud.
'''

'''
GitHub Container Registry (GHCR) — ghcr.io — which is GitHub's own Docker image registry, 
similar to AWS ECR, but tightly integrated with GitHub repositories.'''

def ecr_push():
    username = 'viswavisan'
    token = 'get token from git'
    repo = 'flask_demo'
    registry = 'ghcr.io'
    image_tag = f'{registry}/{username}/{repo}:latest'
    d_client = docker.from_env()

    try:
        d_client.login(username=username, password=token, registry=registry)
        push_logs = d_client.images.push(image_tag, stream=True, decode=True)
        for log in push_logs:
            if 'status' in log:print(f"{log.get('status')} {log.get('progress', '')}")
            elif 'error' in log:print(f"Error: {log['error']}")
    except Exception as e:
        print(f"Push failed: {e}")
    #check packages in https://github.com/viswavisan?tab=packages


#Kubernetes
'''
Kubernetes (often abbreviated as K8s) is an open-source container orchestration platform. 
It automates the deployment, scaling,  and management of containerized applications — like those built with Docker.
'''

from kubernetes import client, config
from datetime import datetime
import time

config.load_kube_config()
apps_v1 = client.AppsV1Api()
core_v1 = client.CoreV1Api()

namespace = "flaskdemo-namespace"
deployment_name = "flaskdemo-deployment"
service_name = "flaskdemo-service"
app_name = "flask_demo"
image_name = 'ghcr.io/viswavisan/flask_demo:latest'
port = 8000
container_name = 'flaskdemo-container'
expose_port=8000
ingress_name = "flaskdemo-ingress"

def create_namespace():
    print('checking namespace')
    existing_ns=[ns.metadata.name for ns in core_v1.list_namespace().items]
    if namespace not in existing_ns:
        print('creating namespace')
        namespace_body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
        core_v1.create_namespace(body=namespace_body)

def create_deployment():
    existing_deployments = [d.metadata.name for d in apps_v1.list_namespaced_deployment(namespace).items]
    if deployment_name in existing_deployments:
        print('updating deployment')
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
        deployment.spec.template.spec.containers[0].image = image_name
        apps_v1.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

        #restart
        # pod_list = core_v1.list_namespaced_pod(namespace, label_selector=f'app={app_name}')
        # for pod in pod_list.items:
        #     core_v1.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace)

        #restart
        deployment.spec.template.metadata.annotations = {"kubectl.kubernetes.io/restartedAt": datetime.utcnow().isoformat()}    
        apps_v1.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

    else:
        print('creating deployment')
        container = client.V1Container(name=container_name,image=image_name,ports=[client.V1ContainerPort(container_port=port)],image_pull_policy='Always')
        template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"app": app_name}),spec=client.V1PodSpec(containers=[container]))
        spec = client.V1DeploymentSpec(replicas=1,template=template,selector=client.V1LabelSelector(match_labels={"app": app_name}))
        deployment = client.V1Deployment(api_version="apps/v1",kind="Deployment",metadata=client.V1ObjectMeta(name=deployment_name),spec=spec)
        apps_v1.create_namespaced_deployment(namespace=namespace, body=deployment)

def create_service():
    existing_services=[service.metadata.name for service in core_v1.list_namespaced_service(namespace).items]
    if service_name not in existing_services:
        print('creating service')
        service = client.V1Service(api_version="v1",
                                kind="Service",
                                metadata=client.V1ObjectMeta(name=service_name),
                                spec=client.V1ServiceSpec(selector={"app":app_name},
                                                            ports=[client.V1ServicePort( name="http", port=port, target_port=expose_port)],
                                                            type="NodePort"))
        core_v1.create_namespaced_service(namespace=namespace, body=service)


# build_image() #when ever change required
# ecr_push()#when ever change required
# create_namespace()#onetime
# create_deployment()#when ever change required/restart
# create_service()#onetime

#port forwarding

'''
Port forwarding is a way to temporarily forward traffic from a port on your local machine 
(like localhost:8000) to a port inside a Kubernetes pod or service (like 5000 inside a Flask container).

# subprocess.Popen(["kubectl", "port-forward", "svc/flaskdemo-service", "8000:8000", "-n", "flaskdemo-namespace"])
'''

#load balancer
'''
A Load Balancer is a component that:
Distributes incoming traffic across multiple backend services (or pods) to ensure no single one is overwhelmed.
Kubernetes tells the cloud provider (e.g., AWS, GCP, Azure) to:

Provision a public IP address
Create a load balancer that routes traffic to your Kubernetes pods behind the scenes

'''
#ingress
'''
What is Ingress in Kubernetes?
An Ingress is a Kubernetes object that manages external access to services within your cluster, typically via HTTP or HTTPS.

Think of Ingress as a receptionist at the front door of your company — they listen at one entrance (like yourdomain.com) 
and route visitors to the right office (service) based on where they want to go (/login, /api, etc.).
'''

#minikube tunneling
#minikube service flaskdemo-service -n flaskdemo-namespace --url

#run in docker
def deploy_in_docker():
    d_client = docker.from_env()
    print('deployment started in docker')

    try:
        existing_container = d_client.containers.get(container_name)
        if existing_container:existing_container.remove(force=True)
    
        for container in d_client.containers.list():
            if container.attrs['NetworkSettings']['Ports']:
                port_mapping = f"{port}/tcp"
                if port_mapping in container.attrs['NetworkSettings']['Ports']:
                    container.stop()
                    container.remove(force=True)
    except:pass

    d_client.containers.run(image_name, detach=True, name=container_name, ports={f'{port}/tcp': expose_port})

# deploy_in_docker()
'''
| Feature              | Docker                    | Kubernetes                            |
| -------------------- | ------------------------- | ------------------------------------- |
| **Scope**            | Single host               | Cluster of machines                   |
| **Deployment style** | Imperative (`docker run`) | Declarative (`kubectl apply`)         |
| **Scaling**          | Manual                    | Automatic                             |
| **Self-healing**     | ❌ No automatic restart  | ✅ Automatically restarts failed pods |
| **Load balancing**   | Manual or limited         | Built-in via Services                 |
| **Rolling updates**  | Manual                    | Automatic with zero downtime          |
| **Networking**       | Simple port mapping       | Service discovery across pods         |
| **Resource limits**  | Not built-in              | Enforced via YAML                     |
| **Use case**         | Dev, small apps           | Prod, large-scale distributed systems |
'''

#Grafana

#node exporter

#prometheus
