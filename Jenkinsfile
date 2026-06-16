pipeline {
    agent any

    stages {
        stage('Debug') {
            steps {
                sh '''
                whoami
                pwd
                which docker || true
                docker --version || true
                '''
            }
        }
    }
}