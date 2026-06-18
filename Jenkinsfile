pipeline {
    agent any

    environment {
        IMAGE_NAME = "jainambarbhaya15/user-service"
        IMAGE_TAG  = "${BUILD_NUMBER}"

        GITOPS_REPO = "https://github.com/jainambarbhaya1509/gitops.git"
        GIT_BRANCH  = "main"
    }

    stages {

        stage('Checkout Application Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Clone GitOps Repository') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh '''
                        rm -rf gitops

                        git clone \
                        https://$GIT_USER:$GIT_TOKEN@github.com/jainambarbhaya1509/gitops.git \
                        gitops
                    '''
                }
            }
        }

        stage('Update Dev Helm Values') {
            steps {
                sh """
                    sed -i 's/tag:.*/tag: "${IMAGE_TAG}"/' \
                    gitops/charts/user-service/values-prod.yaml

                    echo "Updated dev-values.yaml"
                    cat gitops/charts/user-service/values-prod.yaml
                """
            }
        }

        stage('Commit And Push GitOps Changes') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh """
                        cd gitops

                        git config user.email "jenkins@local"
                        git config user.name "Jenkins"

                        git add .

                        git commit -m "Deploy build ${IMAGE_TAG} to dev" || true

                        git remote set-url origin \
                        https://\$GIT_USER:\$GIT_TOKEN@github.com/jainambarbhaya1509/gitops.git

                        git push origin main
                    """
                }
            }
        }
    }

    post {

        success {
            echo "Docker image built and pushed"
            echo "GitOps repository updated"
            echo "ArgoCD will deploy DEV automatically"
        }

        failure {
            echo "Pipeline failed"
        }
    }
}