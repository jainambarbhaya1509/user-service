pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify') {
            steps {
                sh '''
                pwd
                ls -la
                docker --version
                '''
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                docker build -t user-service:test .
                '''
            }
        }
    }
}