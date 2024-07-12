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
  - name: jnlp
    image: 'jenkins/inbound-agent:3248.v65ecb_254c298-2'
    args: '${computer.jnlpmac} ${computer.name}'
            """
        }
    }
    environment {
        GIT_CREDENTIALS_ID = 'github_credentials' // Replace with your actual credentials ID
    }
    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/RazAsraf7/FastAPI-App',
                            credentialsId: env.GIT_CREDENTIALS_ID
                        ]]
                    ])
                }
            }
        }
        stage('Helm Lint') {
            steps {
                container('helm') {
                    sh 'helm lint ./domyduda'
                }
            }
        }
        stage('Helm Package') {
            steps {
                container('helm') {
                    sh 'helm package ./domyduda'
                }
            }
        }
        stage('Helm Deploy') {
            steps {
                container('kubectl') {
                    sh 'helm upgrade --install domyduda ./domyduda'
                }
            }
        }
    }
    post {
        always {
            container('kubectl') {
                script {
                    // Clean up resources
                    sh 'helm uninstall domyduda || true'
                }
            }
        }
    }
}
