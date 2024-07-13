pipeline {
    agent {
        kubernetes {
            defaultContainer 'helm-kubectl'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: helm-kubectl
      image: razasraf7/helm_and_kubectl
      command:
        - cat
      tty: true
      resources:
        requests:
          memory: '512Mi'
          cpu: '500m'
        limits:
          memory: '1Gi'
          cpu: '1'
      env:
        - name: KUBECONFIG
          value: /home/jenkins/.kube/config
  volumes:
    - name: workspace-volume
      emptyDir: {}
  volumeMounts:
    - name: workspace-volume
      mountPath: /home/jenkins/agent
"""
        }
    }

    environment {
        DOCKER_IMAGE = 'razasraf7/domyduda'
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_REPO = 'RazAsraf7/FastAPI-App'
        GITHUB_TOKEN = credentials('github_credentials')
    }

    stages {
        stage("Checkout code") {
            steps {
                checkout scm
            }
        }

        stage("Build Helm Chart") {
            steps {
                sh """
                    cd domyduda
                    helm dependency update
                    helm upgrade --install domyduda ./domyduda
                """
            }
        }

        stage("Check if Application Works") {
            steps {
                sh """kubectl port-forward svc/domyduda 8000:8000 & sleep 5
                curl -s http://localhost:8000/health"""
            }
        }

        stage("Build Docker Image") {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker_credentials') {
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('Create Merge Request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'github_credentials', variable: 'GITHUB_TOKEN')]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into main"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName}"

                        sh """
                            curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "main" }' \
                            ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                        """
                    }
                }
            }
        }
    }
}
