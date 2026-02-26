pipeline {
    agent any

    stages {
        stage('Pull') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/pavle0x10f2c-cloud/IoT-project.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }
}
