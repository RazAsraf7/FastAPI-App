pipeline {
    agent {
        kubernetes {
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: helm-kubectl
                image: razasraf7/helm_and_kubectl
                command:
                - cat
                tty: true
                volumeMounts:
                - name: docker-socket
                  mountPath: /var/run/docker.sock
              - name: docker
                image: docker:19.03.12
                command:
                - cat
                tty: true
                volumeMounts:
                - name: docker-socket
                  mountPath: /var/run/docker.sock
              volumes:
              - name: docker-socket
                hostPath:
                  path: /var/run/docker.sock
            """
        }
    }
    stages {
        stage('Build Helm Chart') {
            steps {
                container('helm-kubectl') {
                    sh '''
                    cd domyduda
                    helm dependency update
                    cd ..
                    helm upgrade --install domyduda ./domyduda
                    '''
                }
            }
        }
        stage('Check if Application Works') {
            steps {
                container('helm-kubectl') {
                    sh '''
                    sleep 5
                    kubectl port-forward svc/domyduda 8000:8000 &
                    sleep 5
                    curl -s http://localhost:8000/health
                    '''
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh 'docker build -t razasraf7/domyduda:latest --no-cache .'
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                container('docker') {
                    withDockerRegistry([credentialsId: 'docker_credentials', url: 'https://index.docker.io/v1/']) {
                        sh 'docker push razasraf7/domyduda:latest'
                    }
                }
            }
        }
    }
}
