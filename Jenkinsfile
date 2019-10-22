pipeline {
         agent {
                docker {
                image 'python:3.7.4-alpine3.9'
                args  '-v /tmp:/tmp'
            }
        }
        environment {
            PROD_DATABRICKS_SHARD = credentials('PROD_DATABRICKS_SHARD')
            PROD_DATABRICKS_TOKEN = credentials('PROD_DATABRICKS_TOKEN')

        }
         stages {
                 stage('Install Depedancies') {
                 steps {
                     sh 'pip install databricks-cli'
                    }
                 }

                 stage('Set .databrickscfg') {
                 steps {
                    sh 'echo "[DEFAULT]" >> ~/.databrickscfg'
                    sh 'echo "host=$PROD_DATABRICKS_SHARD" >> ~/.databrickscfg'
                    sh 'echo "username=viren.patel@databricks.com" >> ~/.databrickscfg'
                    sh 'echo "token=$PROD_DATABRICKS_TOKEN" >> ~/.databrickscfg'
                    sh 'cat ~/.databrickscfg'
            }
        }
    }
}