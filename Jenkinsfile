pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent'
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: slave
spec:
  containers:
  - name: helm
    image: 'alpine/helm:3.9.0'
    command:
    - cat
    tty: true
  - name: kubectl
    image: 'bitnami/kubectl:1.21.3'
    command:
    - cat
    tty: true
  - name: docker
    image: 'docker:latest'
    command:
    - cat
    tty: true
  - name: jnlp
    image: 'jenkins/inbound-agent:4.10-1'
    args: '${computer.jnlpmac} ${computer.name}'
            """
        }
    environment{
        DOCKER_IMAGE = 'razasraf7/domyduda'
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_REPO = 'RazAsraf7/FastAPI-App'
        GITHUB_TOKEN = credentials('github-credentials')
    }

    stages{
        stage("Checkout code"){
            steps {
                checkout scm
            }
        }

        stage("Install dependencies"){
            steps {
                sh 'helm upgrade --install domyduda domyduda'
            }
        }
        stage("Build docker image"){
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                }
            }
        }

        stage('Push Docker image') {
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

        stage('Create merge request'){
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'github-creds', variable: 'GITHUB_TOKEN')]) {
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
}
