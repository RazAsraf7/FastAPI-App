pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: "v1"
kind: "Pod"
metadata:
  annotations:
    kubernetes.jenkins.io/last-refresh: "1720282518318"
    buildUrl: "http://jenkins.jenkins.svc.cluster.local:8080/job/Final%20Project/job/feature/18/"
    runUrl: "job/Final%20Project/job/feature/18/"
  labels:
    jenkins/jenkins-jenkins-agent: "true"
    jenkins/label-digest: "ee3d95fc3ecb6e9df327abda36df6716d619ddfd"
    jenkins/label: "Final_Project_feature_18-htk2p"
    kubernetes.jenkins.io/controller: "http___jenkins_jenkins_svc_cluster_local_8080x"
  name: "final-project-feature-18-htk2p-f93p6-zqdt3"
  namespace: "jenkins"
spec:
  containers:
  - command:
    - "cat"
    image: "alpine/helm:latest"
    name: "helm"
    tty: true
    volumeMounts:
    - mountPath: "/home/jenkins/agent"
      name: "workspace-volume"
      readOnly: false
  - command:
    - "cat"
    image: "bitnami/kubectl:1.21.3"
    name: "kubectl"
    tty: true
    volumeMounts:
    - mountPath: "/home/jenkins/agent"
      name: "workspace-volume"
      readOnly: false
  - env:
    - name: "JENKINS_SECRET"
      value: "********"
    - name: "JENKINS_TUNNEL"
      value: "jenkins-agent.jenkins.svc.cluster.local:50000"
    - name: "JENKINS_AGENT_NAME"
      value: "final-project-feature-18-htk2p-f93p6-zqdt3"
    - name: "REMOTING_OPTS"
      value: "-noReconnectAfter 1d"
    - name: "JENKINS_NAME"
      value: "final-project-feature-18-htk2p-f93p6-zqdt3"
    - name: "JENKINS_AGENT_WORKDIR"
      value: "/home/jenkins/agent"
    - name: "JENKINS_URL"
      value: "http://jenkins.jenkins.svc.cluster.local:8080/"
    image: "jenkins/inbound-agent:3248.v65ecb_254c298-2"
    name: "jnlp"
    resources:
      requests:
        memory: "256Mi"
        cpu: "100m"
    volumeMounts:
    - mountPath: "/home/jenkins/agent"
      name: "workspace-volume"
      readOnly: false
  nodeSelector:
    kubernetes.io/os: "linux"
  restartPolicy: "Never"
  volumes:
  - emptyDir:
      medium: ""
    name: "workspace-volume"
"""
        }
    }
    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Download and Lint MongoDB Chart') {
            steps {
                container('helm') {
                    script {
                        sh """
                            rm -rf mongodb
                            helm repo add bitnami https://charts.bitnami.com/bitnami
                            helm repo update
                            helm pull bitnami/mongodb --untar
                            helm lint mongodb -f mongodb-architecture.yaml --debug
                        """
                    }
                }
            }
        }
        stage('Deploy MongoDB') {
            steps {
                container('helm') {
                    script {
                        sh """
                            helm install my-mongodb ./mongodb -f mongodb-architecture.yaml --set auth.usernames[0]=root,auth.databases[0]=DMD
                        """
                    }
                }
            }
        }
        stage('Package and Deploy Application') {
            steps {
                container('helm') {
                    script {
                        sh """
                            # Package and deploy your application
                        """
                    }
                }
            }
        }
        stage('Check Application') {
            steps {
                container('helm') {
                    script {
                        sh """
                            # Check your application
                        """
                    }
                }
            }
        }
    }
    post {
        always {
            container('helm') {
                script {
                    sh """
                        helm uninstall my-app || true
                        helm uninstall my-mongodb || true
                    """
                }
            }
        }
    }
}
