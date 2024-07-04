pipeline {
    agent {
        kubernetes {
            defaultContainer 'domyduda-ffb7fd-bxqsw'
        }
    }
    environment {
        DOCKER_CREDS = credentials('docker_credentials')
        GITHUB_CREDS = credentials('github_credentials')
        DOCKER_IMAGE = 'razasraf7/domyduda'
        GITHUB_REPOSITORY = 'FastAPI-App'
        USERNAME = 'root'
        ROOT_PASSWORD = '212928139'
        HOST = 'mongodb'
        PORT = '27017'
    }
    stages {
        stage('Check Kubernetes Connection') {
            steps {
                sh 'kubectl get nodes'
            }
        }
        stage('Get Helm') {
            steps {
                sh 'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3'
                sh 'chmod 700 get_helm.sh'
                sh './get_helm.sh'
            }
        }
        stage('Get MongoDB') {
            steps {
                sh 'helm repo add mongodb https://mongodb.github.io/helm-charts'
                sh 'helm repo update'
                sh 'helm install mongodb mongodb/mongodb -f mongodb-architecture.yaml'
            }
        }
        stage('Get DoMyDuda') {
            steps {
                sh 'helm install domyduda domyduda'
            }
        }
        stage('Login to Docker Hub and GitHub') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDS) {
                        // Docker Hub login happens automatically
                    }
                    withCredentials([usernamePassword(credentialsId: 'github_credentials', passwordVariable: 'GITHUB_PASSWORD', usernameVariable: 'GITHUB_USERNAME')]) {
                        sh 'echo "${GITHUB_PASSWORD}" | docker login ghcr.io -u "${GITHUB_USERNAME}" --password-stdin'
                    }
                }
            }
        }
        stage('Say when done') {
            steps {
                sh 'echo "Done!"'
            }
        }
    }
}
