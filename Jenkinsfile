pipeline {
    agent {
        kubernetes {
            yaml """
            apiVersion: v1
            kind: Pod
            metadata:
              annotations:
                kubernetes.jenkins.io/last-refresh: "1720108736492"
                buildUrl: "http://jenkins.jenkins.svc.cluster.local:8080/job/Final%20Project/job/feature/5/"
                runUrl: "job/Final%20Project/job/feature/5/"
              labels:
                jenkins/jenkins-jenkins-agent: "true"
                jenkins/label-digest: "2f8ba26ef296f27bb7ec234acbb2e65c4e883fa1"
                jenkins/label: "Final_Project_feature_5-vw0s0"
                kubernetes.jenkins.io/controller: "http___jenkins_jenkins_svc_cluster_local_8080x"
            spec:
              containers:
              - name: jnlp
                image: jenkins/inbound-agent:3248.v65ecb_254c298-2
                env:
                  - name: JENKINS_SECRET
                    value: "********"
                  - name: JENKINS_TUNNEL
                    value: "jenkins-agent.jenkins.svc.cluster.local:50000"
                  - name: JENKINS_AGENT_NAME
                    value: "final-project-feature-5-vw0s0-t6w3c-01t4w"
                  - name: REMOTING_OPTS
                    value: "-noReconnectAfter 1d"
                  - name: JENKINS_NAME
                    value: "final-project-feature-5-vw0s0-t6w3c-01t4w"
                  - name: JENKINS_AGENT_WORKDIR
                    value: "/home/jenkins/agent"
                  - name: JENKINS_URL
                    value: "http://jenkins.jenkins.svc.cluster.local:8080/"
                resources:
                  requests:
                    memory: "256Mi"
                    cpu: "100m"
                volumeMounts:
                  - mountPath: "/home/jenkins/agent"
                    name: workspace-volume
                    readOnly: false
              - name: domyduda
                image: your-docker-image  # Replace with your actual image
                command: ['cat']
                tty: true
                resources:
                  requests:
                    memory: "256Mi"
                    cpu: "100m"
                volumeMounts:
                  - mountPath: "/home/jenkins/agent"
                    name: workspace-volume
                    readOnly: false
              nodeSelector:
                kubernetes.io/os: "linux"
              restartPolicy: Never
              volumes:
              - emptyDir:
                  medium: ""
                name: workspace-volume
            """
        }
    }
    environment {
        DOCKER_CREDS = credentials('docker_credentials')
        GITHUB_CREDS = credentials('github_credentials')
    }
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Check Kubernetes Connection') {
            steps {
                container('domyduda') {
                    sh 'kubectl get nodes'
                }
            }
        }
        stage('Get Helm') {
            steps {
                container('domyduda') {
                    sh 'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3'
                    sh 'chmod 700 get_helm.sh'
                    sh './get_helm.sh'
                }
            }
        }
        stage('Get MongoDB') {
            steps {
                container('domyduda') {
                    sh 'helm add repo https://charts.bitnami.com/bitnami'
                    sh 'helm repo update'
                    sh 'helm install mongodb bitnami/mongodb'
                }
            }
        }
        stage('Get DoMyDuda') {
            steps {
                container('domyduda') {
                    sh 'helm install domyduda ./domyduda'
                }
            }
        }
        stage('Login to Docker Hub and GitHub') {
            steps {
                container('domyduda') {
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    }
                    withCredentials([usernamePassword(credentialsId: 'github-credentials-id', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_PASS')]) {
                        sh 'echo $GITHUB_PASS | docker login docker.pkg.github.com -u $GITHUB_USER --password-stdin'
                    }
                }
            }
        }
        stage('Say when done') {
            steps {
                echo 'Build completed'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        failure {
            mail to: 'razasraf7@gmail.com',
                 subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                 body: "Something is wrong with ${env.BUILD_URL}"
        }
    }
}
