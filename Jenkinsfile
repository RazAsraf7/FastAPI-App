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
    image: 'jenkins/inbound-agent:4.10-1'
    args: '${computer.jnlpmac} ${computer.name}'
            """
        }
    }
    environment {
        RELEASE_NAME = 'domyduda'
        CHART_NAME = 'domyduda'
        DOCKER_IMAGE = 'razasraf7/domyduda'
        NAMESPACE = 'default'
        HELM_VALUES = 'values.yaml' // Use if you have a values file
    }
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Helm Lint') {
            steps {
                container('helm') {
                    sh 'helm lint $CHART_NAME'
                }
            }
        }
        stage('Helm Package') {
            steps {
                container('helm') {
                    sh 'helm package $CHART_NAME'
                }
            }
        }
        stage('Helm Deploy') {
            steps {
                container('kubectl') {
                    sh '''
                        helm upgrade --install $RELEASE_NAME ./$CHART_NAME \
                        --set image.repository=$DOCKER_IMAGE \
                        --namespace $NAMESPACE
                    '''
                }
            }
        }
        stage('Port Forward and Health Check') {
            steps {
                container('kubectl') {
                    script {
                        sh '''
                            kubectl port-forward svc/$RELEASE_NAME 8000:8000 &
                            sleep 10
                        '''
                        def response = sh(script: "curl -s http://localhost:8000/health", returnStdout: true).trim()
                        if (response == 'OK') {
                            echo 'Health check passed.'
                        } else {
                            error('Health check failed.')
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            node('jenkins-agent') {
                container('kubectl') {
                    script {
                        sh 'kubectl delete pod $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath={.items..metadata.name}) || true'
                    }
                }
                cleanWs()
            }
        }
    }
}
