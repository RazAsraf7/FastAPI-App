pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: helm
    image: alpine/helm:3.9.0
    command:
    - cat
    tty: true
  - name: kubectl
    image: bitnami/kubectl:1.21.3
    command:
    - cat
    tty: true
"""
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Package and Deploy Application') {
            steps {
                container('helm') {
                    script {
                        def chartDir = "/home/jenkins/agent/workspace/Final_Project_new_chart/domyduda"
                        dir(chartDir) {
                            sh 'helm dependency update'
                            sh 'helm install my-app .'
                        }
                    }
                }
            }
        }

        stage('Port Forward and Health Check') {
            steps {
                container('kubectl') {
                    script {
                        // Add debug logs
                        echo "Starting Port Forwarding and Health Check"
                        sh '''
                            set -x
                            POD_NAME=$(kubectl get pods --namespace jenkins -l "app.kubernetes.io/name=domyduda,app.kubernetes.io/instance=my-app" -o jsonpath="{.items[0].metadata.name}")
                            echo "POD_NAME: $POD_NAME"
                            CONTAINER_PORT=$(kubectl get pod --namespace jenkins $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
                            echo "CONTAINER_PORT: $CONTAINER_PORT"
                            kubectl --namespace jenkins port-forward $POD_NAME 8000:$CONTAINER_PORT &
                            PORT_FORWARD_PID=$!
                            sleep 10
                            curl -s http://localhost:8000/health || (echo "Health check failed!" && kill $PORT_FORWARD_PID && exit 1)
                            kill $PORT_FORWARD_PID
                            echo "Port Forwarding and Health Check completed"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            container('helm') {
                script {
                    // Clean up the Helm release
                    sh 'helm uninstall my-app || true'
                }
            }
        }
    }
}
