pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins/jenkins-jenkins-agent: "true"
    jenkins/label-digest: "ee3d95fc3ecb6e9df327abda36df6716d619ddfd"
    jenkins/label: "Final_Project_feature_21-g4sgs"
    kubernetes.jenkins.io/controller: "http___jenkins_jenkins_svc_cluster_local_8080x"
  name: "final-project-feature-21-g4sgs-kpksj-3lbsb"
  namespace: "jenkins"
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent
    args: ["-url", "http://jenkins.jenkins.svc.cluster.local:8080", "$(JENKINS_SECRET)", "$(JENKINS_NAME)", "-workDir=/home/jenkins/agent"]
    env:
    - name: JENKINS_SECRET
      valueFrom:
        secretKeyRef:
          name: jenkins-agent-secret
          key: jenkins-agent-secret
    - name: JENKINS_NAME
      value: "final-project-feature-21-g4sgs-kpksj-3lbsb"
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
