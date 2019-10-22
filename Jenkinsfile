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
                 stage('Copy Notebooks to Prod') {
                 steps {
                    sh 'databricks workspace rm -r /git-notebooks/'
                    sh 'databricks workspace import_dir -o ./git-notebooks /git-notebooks'
                    }
                 }
                 stage('Databricks Job Create/Update') {
                 steps {
                    sh 'cd ./deploy-scripts'
                    sh 'ls -l'
                    sh 'python job-deploy.py'
                    }             
                 }
        }
    }