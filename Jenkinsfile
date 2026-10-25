pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t secure-ci-pipeline .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm secure-ci-pipeline'
            }
        }
    }
}