pipeline {

    agent any

    environment {

        APP_NAME = "user-service"

        IMAGE_REPO = "jainambarbhaya/user-service"

        GITOPS_REPO = "git@github.com:jainambarbhaya1509/gitops.git"

        BUILD_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Application') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                -t ${IMAGE_REPO}:${BUILD_TAG} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''
                    echo $DOCKER_PASS | docker login \
                    -u $DOCKER_USER \
                    --password-stdin

                    docker push ${IMAGE_REPO}:${BUILD_TAG}
                    '''
                }
            }
        }

        stage('Clone GitOps Repo') {
            steps {

                sshagent(['github-ssh']) {

                    sh '''
                    rm -rf gitops

                    git clone ${GITOPS_REPO}

                    cd gitops

                    git config user.email "jenkins@company.com"
                    git config user.name "Jenkins"
                    '''
                }
            }
        }

        stage('Deploy To DEV') {

            steps {

                sshagent(['github-ssh']) {

                    sh '''
                    cd gitops

                    sed -i.bak \
                    "s/tag:.*/tag: \\"${BUILD_TAG}\\"/" \
                    environments/dev/user-service-values.yaml

                    rm -f environments/dev/*.bak

                    git add .

                    git commit -m "Deploy DEV ${BUILD_TAG}" || true

                    git push
                    '''
                }
            }
        }

        stage('Wait For DEV Validation') {

            steps {

                input(
                    message: "Promote ${BUILD_TAG} to PROD?",
                    ok: "Deploy"
                )
            }
        }

        stage('Deploy To PROD') {

            steps {

                sshagent(['github-ssh']) {

                    sh '''
                    cd gitops

                    sed -i.bak \
                    "s/tag:.*/tag: \\"${BUILD_TAG}\\"/" \
                    environments/prod/user-service-values.yaml

                    rm -f environments/prod/*.bak

                    git add .

                    git commit -m "Deploy PROD ${BUILD_TAG}" || true

                    git push
                    '''
                }
            }
        }
    }

    post {

        success {

            echo "Deployment Successful"
        }

        failure {

            echo "Deployment Failed"
        }
    }
}