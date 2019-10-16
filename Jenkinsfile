pipeline {
         agent {
                docker {
                image 'python:3.7.4-alpine3.9'
                args  '-v /tmp:/tmp'
            }
        }
        environment {
            NEIL_SECRET = credentials('neil_secret')

        }
         stages {
                 stage('One Echo') {
                 steps {
                     echo 'Hi, this is Neil'
                    }
                 }

                 stage('Two ls') {
                 steps {
                    sh 'ls -l'
                    echo '$PWD'
                    echo '$NEIL_SECRET'
            }
        }
    }
}